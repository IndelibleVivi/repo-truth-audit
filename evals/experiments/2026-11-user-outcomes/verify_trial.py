#!/usr/bin/env python3
"""Independently observe the November user-outcome trial deliverables.

Known, trusted local subjects only. Checks run in disposable copies. The
evaluator fetches no dependencies and makes no agent call; it is not an OS
sandbox or network control. This is not a general repair
grader, report-keyword grader, or a tool that authenticates trial provenance.
The summary case still needs an independent reading of the audit report.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[3]


def module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def portable(value, paths: dict[str, str]):
    if isinstance(value, str):
        for original, replacement in paths.items():
            value = value.replace(original, replacement)
        return value
    if isinstance(value, list):
        return [portable(item, paths) for item in value]
    if isinstance(value, dict):
        return {key: portable(item, paths) for key, item in value.items()}
    return value


def run(cwd: Path, argv: list[str], paths: dict[str, str]) -> dict:
    result = subprocess.run(argv, cwd=cwd, text=True, capture_output=True, timeout=60)
    return portable({"argv": argv, "exit_code": result.returncode,
                     "stdout": result.stdout, "stderr": result.stderr},
                    {str(Path(sys.executable)): "python3", **paths})


def check_mitt(candidate: Path, seed: Path) -> dict:
    """Use the selected package, but never use a candidate-provided compiler."""
    probe = module("mitt_field_probe", ROOT / "evals/field/probe_mitt.py")
    compiler = seed.resolve() / "node_modules/typescript"
    require(json.loads((compiler / "package.json").read_text())["version"] == "4.9.5",
            "the independent compiler must be the pinned TypeScript 4.9.5")
    selected = candidate / "consumer/node_modules/mitt"
    require(selected.is_dir(), "the actual application's mitt package is missing")
    with tempfile.TemporaryDirectory(prefix="rta-trial-mitt-") as raw:
        work = Path(raw)
        package = work / "node_modules/mitt"
        shutil.copytree(selected, package)
        (work / "src").mkdir()
        shutil.copy2(candidate / "src/index.ts", work / "src/index.ts")
        (work / "task.ts").write_text(probe.TASK, encoding="utf-8")
        (work / "controls.ts").write_text(probe.CONTROL, encoding="utf-8")
        (work / "source-task.ts").write_text(
            probe.TASK.replace("from 'mitt'", "from './src/index'"), encoding="utf-8")
        (work / "runtime.cjs").write_text(probe.RUNTIME, encoding="utf-8")
        paths = {str(work): "<temporary>", str(seed.resolve()): "<consumer-seed>"}
        def compile_file(name):
            return run(work, ["node", str(compiler / "bin/tsc"), name, "--noEmit",
                              "--strict", "--lib", "es2015", "--moduleResolution", "node"], paths)
        checks = {"consumer_types": compile_file("task.ts"),
                  "type_preservation": compile_file("controls.ts"),
                  "source_types": compile_file("source-task.ts"),
                  "selected_runtime": run(work, ["node", "runtime.cjs"], paths)}
        for label, observation in checks.items():
            require(observation["exit_code"] == 0, f"{label} failed: {observation}")
        generated = run(work, ["node", str(compiler / "bin/tsc"), "src/index.ts",
                              "--declaration", "--emitDeclarationOnly", "--strict",
                              "--lib", "es2015", "--outDir", "generated"], paths)
        require(generated["exit_code"] == 0, "source declaration generation failed")
        require((work / "generated/index.d.ts").read_bytes() == (package / "index.d.ts").read_bytes(),
                "the consumer declaration differs from freshly generated source declarations")
        checks["fresh_source_declarations"] = generated
        return {"checks": checks, "compiler": "TypeScript 4.9.5 from evaluator seed",
                "consumer_declaration_sha256": digest(selected / "index.d.ts"),
                "source_sha256": digest(candidate / "src/index.ts"),
                "runtime_entry_sha256": digest(selected / "dist/mitt.js"),
                "scope": "source, actual package types, rejected invalid types and selected CJS runtime"}


def check_cedar(candidate: Path) -> dict:
    checker = ROOT / "evals/intent-lab/check_intent_subject.py"
    result = run(ROOT, [sys.executable, str(checker), "--verify-operate", "task-export-handoff",
                        "--candidate", str(candidate)], {str(ROOT): "<rta-repo>", str(candidate): "<candidate>"})
    require(result["exit_code"] == 0, f"Cedar receiver verification failed: {result}")
    return {"command": result, "recipient_evidence": json.loads(result["stdout"])}


def check_summary(candidate: Path) -> dict:
    fixture = module("cedar_trial_fixture", ROOT / "evals/intent-lab/task_subjects.py")
    originals = fixture.files("summary")
    for name, expected in originals.items():
        require((candidate / name).read_bytes() == expected.encode("utf-8"),
                f"read-only task changed an original product file: {name}")
    extras = sorted(p.relative_to(candidate).as_posix() for p in candidate.rglob("*")
                    if p.is_file() and ".git" not in p.relative_to(candidate).parts
                    and p.relative_to(candidate).as_posix() not in originals)
    require(extras == ["INTENT-AUDIT.md", "TASK.md"], f"unexpected Audit-mode additions: {extras}")
    with tempfile.TemporaryDirectory(prefix="rta-trial-summary-") as raw:
        base = Path(raw)
        source = base / "source"
        shutil.copytree(candidate, source, ignore=shutil.ignore_patterns(".git"))
        fixture.check(source, "summary")
        recipient = base / "recipient"
        recipient.mkdir()
        shutil.copy2(source / "app.py", recipient / "app.py")
        packet = base / "packet.json"
        export = fixture.call(source, "export", "--store", source / "store.json", "--output", packet)
        require(export.returncode == 0, "summary export failed")
        packet_bytes = packet.read_bytes()
        shutil.rmtree(source)
        packet.unlink()
        (recipient / "packet.json").write_bytes(packet_bytes)
        result = run(recipient, [sys.executable, "-B", "app.py", "read", "--packet", "packet.json"],
                     {str(base): "<temporary>"})
        expected = [{"id": row["id"], "text": row["text"]} for row in fixture.STORE["claims"]]
        require(result["exit_code"] == 0 and json.loads(result["stdout"]) == expected,
                "summary recipient cannot read exact delivered summaries")
        require((recipient / "packet.json").read_bytes() == packet_bytes, "summary read mutated packet")
    return {"original_product_bytes_unchanged": True, "allowed_additions": extras,
            "fresh_recipient": result, "report_sha256": digest(candidate / "INTENT-AUDIT.md"),
            "report_review_required": True,
            "scope": "technical contract and read-only boundary; audit judgment requires independent reading"}


def reexport_only(path: Path) -> bool:
    """Recognize the observed harmless shim; do not claim general reachability."""
    body = ast.parse(path.read_text(encoding="utf-8")).body
    if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) and isinstance(body[0].value.value, str):
        body = body[1:]
    return (len(body) == 1 and isinstance(body[0], ast.ImportFrom)
            and body[0].module == "runner" and body[0].level == 0
            and len(body[0].names) == 1 and body[0].names[0].name == "process"
            and body[0].names[0].asname is None)


def check_direct_order(product: Path, workspace: Path) -> dict:
    """Check explicit exception order without using candidate-authored tests."""
    script = '''import importlib, json, pathlib, sys
root = pathlib.Path(sys.argv[1])
sys.path.insert(0, str(root))
selected = json.loads((root / 'delivery.json').read_text())['module']
module = importlib.import_module(selected)
rows = json.loads(sys.argv[2])
try:
    value = module.process(rows, pathlib.Path(sys.argv[4]), sys.argv[3])
    print(json.dumps({'returned': value}))
except Exception as exc:
    print(json.dumps({'exception': type(exc).__name__, 'message': str(exc)}))
'''
    cases = [
        ("shape_before_format_or_io", {}, "unsupported",
         {"exception": "ValueError", "message": "records must be a list"}),
        ("record_before_format_or_io", [{"name": "x", "amount": True}], "unsupported",
         {"exception": "ValueError", "message": "invalid record"}),
        ("format_before_io", [{"name": "x", "amount": 3}], "unsupported",
         {"exception": "ValueError", "message": "unknown format"}),
        ("empty_skips_io", [], "json", {"returned": "[]\n"}),
    ]
    results = {}
    for name, rows, mode, expected in cases:
        observation = run(workspace, [sys.executable, "-I", "-B", "-c", script, str(product),
                                     json.dumps(rows), mode, str(workspace)],
                          {str(workspace): "<temporary>"})
        require(observation["exit_code"] == 0 and json.loads(observation["stdout"]) == expected,
                f"direct ordering check failed: {name}: {observation}")
        results[name] = json.loads(observation["stdout"])
    return results


def check_resume(candidate: Path, delivered_zip: Path | None) -> dict:
    fixture = module("operation_trial_fixture", ROOT / "evals/operation-lab/run_operation_lab.py")
    preparer = module("user_outcomes_prepare", Path(__file__).with_name("prepare_trial.py"))
    require((candidate / "TASK.md").read_text(encoding="utf-8") == preparer.RESUME_TASK,
            "the continuation task differs from the task used to scope these checks")
    owner = fixture.BASELINE["owner-notes.txt"] + "Later owner edit: keep the French launch wording pending review.\n"
    require((candidate / "owner-notes.txt").read_bytes() == owner.encode("utf-8"), "later owner work changed")
    require((candidate / "entry.py").read_bytes() == fixture.ENTRY.encode("utf-8"), "entry CLI contract changed")
    with tempfile.TemporaryDirectory(prefix="rta-trial-resume-") as raw:
        base = Path(raw)
        source = base / "source"
        shutil.copytree(candidate, source, ignore=shutil.ignore_patterns(".git", "__pycache__"))
        source_behavior = fixture.characterize(source)
        source_order = check_direct_order(source, base)
        try:
            fixture.assert_structure(source)
            original_structure = {"status": "passed"}
        except AssertionError as exc:
            original_structure = {"status": "failed", "error": str(exc)}
        members = json.loads((source / "bundle.json").read_text())
        require("legacy.py" not in members, "the legacy implementation remains in the declared artifact")
        artifact = base / "artifact"
        fixture.build_artifact(source, artifact)
        artifact_behavior = fixture.characterize(artifact)
        artifact_order = check_direct_order(artifact, base)
        # The task asks for retirement from selected CLI and declared bundle.
        # The original lab separately requires deleting every legacy.py and
        # scans unrelated root-level scripts. Record that stricter check, but
        # apply it to the declared operational graph for this actual task.
        fixture.assert_structure(artifact)
        legacy = source / "legacy.py"
        if legacy.exists():
            require(reexport_only(legacy), "unselected legacy code needs independent responsibility review")
        delivered = {"status": "not supplied", "note": "No claim about an existing ZIP; --artifact enables that observation."}
        if delivered_zip is not None:
            delivered_zip = delivered_zip.resolve()
            require(delivered_zip.is_file(), "the reported delivered ZIP does not exist")
            receiver = base / "delivered-zip-recipient"
            receiver.mkdir()
            with zipfile.ZipFile(delivered_zip) as package:
                require(sorted(package.namelist()) == sorted(members), "delivered ZIP members differ from the manifest")
                for name in members:
                    content = package.read(name)
                    require(content == (source / name).read_bytes(), f"delivered ZIP has stale content: {name}")
                    (receiver / name).write_bytes(content)
            fixture.assert_structure(receiver)
            delivered = {"status": "passed", "sha256": digest(delivered_zip),
                         "members_and_source_bytes_match": True,
                         "behavior": fixture.characterize(receiver),
                         "direct_order": check_direct_order(receiver, base)}
        return {"source_behavior": source_behavior, "fresh_artifact_behavior": artifact_behavior,
                "source_direct_order": source_order, "fresh_artifact_direct_order": artifact_order,
                "reported_delivered_zip": delivered,
                "original_lab_structure": original_structure,
                "task_contract_structure": {"status": "passed", "selected_module": "runner",
                    "bundle_members": members, "unselected_legacy_reexport": legacy.exists(),
                    "obligation": "Retire legacy.py from the selected CLI and the declared bundle.",
                    "adjudication": "The original fixture's file-deletion rule is stricter than this task. "
                                    "The delivered graph has separate owners; any retained legacy file is only a runner re-export. "
                                    "Unselected build and verification scripts are outside the durable runtime state-owner check."},
                "owner_later_edit_preserved": True, "entry_cli_bytes_preserved": True,
                "probe_count_per_surface": len(fixture.PROBES),
                "scope": "fixed independent behavior probes, actual selected source, freshly assembled declared artifact and owner edits"}


def verify(case: str, candidate: Path, consumer_seed: Path | None = None,
           delivered_zip: Path | None = None) -> dict:
    candidate = candidate.resolve()
    require(candidate.is_dir(), "candidate directory does not exist")
    if case == "mitt":
        require(consumer_seed is not None, "mitt requires --consumer-seed with an independent compiler")
        observation = check_mitt(candidate, consumer_seed)
    elif case == "cedar":
        observation = check_cedar(candidate)
    elif case == "summary":
        observation = check_summary(candidate)
    elif case == "resume":
        observation = check_resume(candidate, delivered_zip)
    else:
        raise ValueError(f"unknown case: {case}")
    return {"schema_version": 1, "case": case, "status": "passed", "observation": observation,
            "target_model_invocations": 0, "os_isolation": False}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case", choices=("mitt", "cedar", "summary", "resume"))
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--consumer-seed", type=Path)
    parser.add_argument("--artifact", type=Path, help="resume: the actual ZIP reported delivered by the target")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.output:
        output = args.output.resolve()
        protected_roots = [args.candidate, *([args.consumer_seed] if args.consumer_seed else [])]
        if any(output.is_relative_to(root.resolve()) for root in protected_roots) or (
                args.artifact and output == args.artifact.resolve()):
            parser.error("--output must not overwrite an observed subject, seed or artifact")
    try:
        result = verify(args.case, args.candidate, args.consumer_seed, args.artifact)
    except (AssertionError, OSError, ValueError, subprocess.SubprocessError) as exc:
        result = {"schema_version": 1, "case": args.case, "status": "failed", "error": str(exc),
                  "target_model_invocations": 0, "os_isolation": False}
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if result["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
