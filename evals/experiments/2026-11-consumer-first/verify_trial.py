#!/usr/bin/env python3
"""Independently verify actual consumer-first trial artifacts.

Trusted synthetic fixtures only. The verifier runs in disposable copies, makes
no model or network call, and does not execute evidence locators. This is not a
general repair grader or an OS sandbox.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import zipfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
TASKS = ("migration-recovery", "delivery-adoption", "known-bug", "clean-baseline")

def module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded

def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)

def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def unavailable_measurement(source: str) -> dict:
    return {"status": "unavailable", "value": None, "source": source}

def snapshot(root: Path) -> dict[str, bytes]:
    return {p.relative_to(root).as_posix(): p.read_bytes()
            for p in sorted(root.rglob("*"))
            if p.is_file() and ".git" not in p.relative_to(root).parts}

def run(cwd: Path, argv: list[str], *, timeout: int = 30) -> dict:
    environment = {
        **os.environ,
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "PYTHONUTF8": "1",
        "PYTHONIOENCODING": "utf-8",
    }
    result = subprocess.run(argv, cwd=cwd, text=True, capture_output=True,
                            encoding="utf-8", timeout=timeout, check=False,
                            env=environment)
    return {"argv": argv, "exit_code": result.returncode,
            "stdout": result.stdout, "stderr": result.stderr}

def copy_target(root: Path, task: str, base: Path, language: str = "en") -> tuple[Path, dict[str, bytes]]:
    target = base / "target"
    shutil.copytree(root, target, ignore=shutil.ignore_patterns(".git", "__pycache__"))
    supplied = module("consumer_prepare_verify", HERE / "prepare_trial.py")
    expected = module("consumer_subject_verify", HERE / "subjects.py")
    require((target / "TASK.md").read_text(encoding="utf-8")
            == supplied.prompt(task, language), "candidate Task prompt differs from the registered prompt language")
    if task == "migration-recovery":
        fixture = module("consumer_resume_verify", ROOT / "evals/operation-lab/run_operation_lab.py")
        for name, value in (("owner-notes.txt", supplied.RESUME_OWNER),
                            ("CHECKPOINT.md", supplied.RESUME_CHECKPOINT),
                            ("entry.py", fixture.ENTRY)):
            require((target / name).read_text(encoding="utf-8") == value,
                    f"protected continuation input changed: {name}")
    elif task == "delivery-adoption":
        sourced = module("consumer_cedar_verify", ROOT / "evals/intent-lab/task_subjects.py")
        for name in ("PROGRAM.md", "store.json", "supplied-worksheet.json",
                     "docs/current-use.md"):
            require((target / name).read_text(encoding="utf-8") == sourced.files("revision")[name],
                    f"protected Cedar input changed: {name}")
    elif task == "known-bug":
        # Source, tests and instructions may legitimately change. The frozen TASK
        # check above and selected-entry behavior below carry this task's boundary.
        pass
    else:
        original = expected.CLEAN_FILES
        for name, text in original.items():
            require((target / name).read_bytes() == text.encode("utf-8"),
                    f"supplied control byte changed: {name}")
    return target, snapshot(target)

def selected_range_entry(target: Path) -> str:
    selector = json.loads((target / "launch.json").read_text(encoding="utf-8"))
    entry = selector.get("entry") if isinstance(selector, dict) else None
    require(isinstance(entry, str) and Path(entry).name == entry
            and not Path(entry).is_absolute(), "launch.json has no safe selected entry")
    require((target / entry).is_file(), f"selected range entry is missing: {entry}")
    return entry

def verify_range(target: Path, mode: str, *, ascending: bool = True) -> dict:
    cases = {
        "2-4": ([2, 3, 4], 0, ""),
        "4-2": ([2, 3, 4] if ascending else [], 0, ""),
        "3": ([3], 0, ""),
        "0-2": (None, 2, "invalid range\n"),
        "-2-2": (None, 2, "invalid range\n"),
        "x-2": (None, 2, "invalid range\n"),
    }
    entry = selected_range_entry(target)
    observations = {}
    for value, (expected, code, stderr) in cases.items():
        observed = run(target, [sys.executable, "-I", "-B", entry, value])
        require(observed["exit_code"] == code, f"{mode} {value}: wrong exit {observed}")
        require(observed["stderr"] == stderr, f"{mode} {value}: wrong error {observed}")
        if expected is None:
            require(observed["stdout"] == "", f"{mode} {value}: invalid input wrote stdout")
        else:
            require(json.loads(observed["stdout"]) == expected,
                    f"{mode} {value}: wrong valid expansion {observed}")
        observations[value] = observed
    return observations

def verify_known_bug(target: Path) -> dict:
    behavior = verify_range(target, "source")
    members = json.loads((target / "bundle.json").read_text(encoding="utf-8"))
    require(isinstance(members, list) and all(isinstance(name, str) for name in members),
            "declared bundle must be a string array")
    selected = selected_range_entry(target)
    require(selected in members and selected != "launch.json",
            "declared bundle does not carry the selected application")
    with tempfile.TemporaryDirectory(prefix="consumer-range-") as raw:
        artifact = Path(raw) / "artifact"
        artifact.mkdir()
        for name in members:
            require(Path(name).name == name and not Path(name).is_absolute(),
                    "bundle path escaped")
            require((target / name).is_file(), f"bundle member is missing: {name}")
            shutil.copy2(target / name, artifact / name)
        artifact_behavior = verify_range(artifact, "declared artifact")
    return {"source": behavior, "artifact": artifact_behavior,
            "valid_neighbor": [2, 3, 4], "invalid_neighbor_error_exit": 2}

def clean_expected(task: str) -> dict[str, str]:
    subjects = module("consumer_clean_expected", HERE / "subjects.py")
    return subjects.KNOWN_BUG_FILES if task == "known-bug" else subjects.CLEAN_FILES

def write_migration_zip(root: Path) -> Path:
    members = json.loads((root / "bundle.json").read_text(encoding="utf-8"))
    zip_path = root / "deliverable.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as package:
        for name in members:
            package.write(root / name, arcname=name)
    return zip_path

def verify_clean(target: Path) -> dict:
    expected = clean_expected("clean-baseline")
    report = target / "INTENT-AUDIT.md"
    require(report.is_file(), "clean control has no INTENT-AUDIT.md")
    allowed = set(expected) | {"TASK.md", "INTENT-AUDIT.md"}
    actual = set(snapshot(target))
    require(actual == allowed, f"clean control changed or added product files: {sorted(actual ^ allowed)}")
    for name, text in expected.items():
        require((target / name).read_bytes() == text.encode("utf-8"),
                f"clean-control byte changed: {name}")
    body = report.read_text(encoding="utf-8")
    lead = body.strip().splitlines()[0] if body.strip() else ""
    require(lead.startswith("Decision answer:"), "clean report must lead with Decision answer:")
    behavior = verify_range(target, "clean baseline", ascending=True)
    return {"report_sha256": digest(report), "bytes_unchanged": True,
            "behavior": behavior, "report_review_required": True,
            "scope": "product bytes and behavior; semantic no-change judgment requires independent reading"}

def reexport_only(path: Path) -> bool:
    body = ast.parse(path.read_text(encoding="utf-8")).body
    if (body and isinstance(body[0], ast.Expr)
            and isinstance(body[0].value, ast.Constant)
            and isinstance(body[0].value.value, str)):
        body = body[1:]
    return (len(body) == 1 and isinstance(body[0], ast.ImportFrom)
            and body[0].module == "runner" and body[0].level == 0
            and len(body[0].names) == 1 and body[0].names[0].name == "process"
            and body[0].names[0].asname is None)

def verify_migration(target: Path, artifact_zip: Path | None) -> dict:
    fixture = module("consumer_resume_check", ROOT / "evals/operation-lab/run_operation_lab.py")
    previous = module("consumer_direct_order", ROOT / "evals/experiments/2026-11-user-outcomes/verify_trial.py")
    with tempfile.TemporaryDirectory(prefix="consumer-resume-") as raw:
        base = Path(raw)
        source = base / "source"
        shutil.copytree(target, source, ignore=shutil.ignore_patterns(".git", "__pycache__"))
        source_behavior = fixture.characterize(source)
        source_order = previous.check_direct_order(source, base)
        try:
            fixture.assert_structure(source)
            original_lab_structure = "passed"
        except AssertionError as exc:
            original_lab_structure = f"failed: {exc}"
        members = json.loads((source / "bundle.json").read_text(encoding="utf-8"))
        require("legacy.py" not in members, "legacy remains in declared bundle")
        built = base / "artifact"
        fixture.build_artifact(source, built)
        fixture.assert_structure(built)
        artifact_behavior = fixture.characterize(built)
        artifact_order = previous.check_direct_order(built, base)
        require(json.loads((built / "delivery.json").read_text()) == {"module": "runner"},
                "fresh declared artifact does not select runner")
        legacy = source / "legacy.py"
        if legacy.exists():
            require(reexport_only(legacy),
                    "unselected legacy code needs independent responsibility review")
        actual_zip = artifact_zip
        if actual_zip is None:
            candidate_zip = target / "deliverable.zip"
            require(candidate_zip.is_file(),
                    "migration result must include the requested deliverable.zip")
            actual_zip = candidate_zip
        receiver = base / "receiver"
        receiver.mkdir()
        with zipfile.ZipFile(actual_zip) as package:
            require(sorted(package.namelist()) == sorted(members),
                    "delivered ZIP members differ from final bundle.json")
            for name in members:
                content = package.read(name)
                require(content == (source / name).read_bytes(),
                        f"delivered ZIP has stale content: {name}")
                (receiver / name).write_bytes(content)
        receiver_behavior = fixture.characterize(receiver)
        fixture.assert_structure(receiver)
        receiver_order = previous.check_direct_order(receiver, base)
        require(json.loads((receiver / "delivery.json").read_text()) == {"module": "runner"},
                "delivered ZIP does not select runner")
    return {"source_behavior": source_behavior, "fresh_artifact_behavior": artifact_behavior,
            "source_direct_order": source_order, "artifact_direct_order": artifact_order,
            "receiver_direct_order": receiver_order,
            "delivered_zip_behavior": receiver_behavior,
            "original_lab_structure": original_lab_structure,
            "owner_later_edit_preserved": True, "entry_cli_bytes_preserved": True,
            "declared_artifact_selects_runner": True,
            "deliverable_zip_verified": True,
            "unselected_legacy_reexport": (target / "legacy.py").exists()}

def verify_delivery(target: Path) -> dict:
    result = run(ROOT, [sys.executable, str(ROOT / "evals/intent-lab/check_intent_subject.py"),
                        "--verify-operate", "task-export-handoff", "--candidate", str(target)])
    require(result["exit_code"] == 0, f"Cedar selected-consumer verification failed: {result}")
    receipt = json.loads(result["stdout"])
    require(receipt.get("status") == "passed", f"Cedar receipt not passed: {receipt}")
    return {"receipt": receipt, "independent_packet_recipient": True,
            "source_and_declared_artifact": True,
            "protected_supplied_evidence": True}

def verify(task: str, candidate: Path, artifact_zip: Path | None = None, language: str = "en") -> dict:
    require(language in {"en", "zh-CN"}, "unsupported prompt language")
    candidate = candidate.resolve()
    require(candidate.is_dir(), "candidate directory does not exist")
    if artifact_zip is not None:
        artifact_zip = artifact_zip.resolve()
        require(artifact_zip.is_file(), "reported artifact does not exist")
    with tempfile.TemporaryDirectory(prefix=f"consumer-verify-{task}-") as raw:
        target, _ = copy_target(candidate, task, Path(raw), language)
        if task == "migration-recovery":
            evidence = verify_migration(target, artifact_zip)
        elif task == "delivery-adoption":
            evidence = verify_delivery(target)
        elif task == "known-bug":
            evidence = verify_known_bug(target)
        else:
            evidence = verify_clean(target)
    return {"schema": "rta-consumer-first-verification/1", "task_id": task,
            "status": "passed", "evidence": evidence,
            "agent_tool_calls": unavailable_measurement(
                "Native tool-call counter not supplied by this offline verifier."),
            "agent_input_tokens": unavailable_measurement(
                "Native input-token counter not supplied by this offline verifier."),
            "agent_output_tokens": unavailable_measurement(
                "Native output-token counter not supplied by this offline verifier."),
            "target_model_invocations": 0, "os_isolation": False}

def negative_control(task: str, base: Path) -> dict:
    """Exercise designed invalid and valid-adjacent controls on copies."""
    subjects = module("consumer_negative_subjects", HERE / "subjects.py")
    if task == "known-bug":
        root = base / "known-bug-bad"
        subjects.write_files(root, subjects.KNOWN_BUG_FILES)
        (root / "TASK.md").write_text(
            (HERE / "tasks/en/known-bug.md").read_text(encoding="utf-8"),
            encoding="utf-8")
        try:
            verify_known_bug(root)
        except AssertionError as exc:
            rejected = str(exc)
        else:
            raise AssertionError("known-bug verifier accepted unrepaired parser")
        good = base / "known-bug-good"
        subjects.write_files(good, subjects.KNOWN_BUG_FILES)
        (good / "TASK.md").write_text(
            (HERE / "tasks/en/known-bug.md").read_text(encoding="utf-8"),
            encoding="utf-8")
        subjects.apply_known_range_repair(good)
        verify_known_bug(good)
        return {"invalid_rejected": rejected, "valid_adjacent_accepted": True}
    if task == "clean-baseline":
        root = base / "clean-dirty"
        subjects.write_files(root, subjects.CLEAN_FILES)
        (root / "TASK.md").write_text(
            (HERE / "tasks/en/clean-baseline.md").read_text(encoding="utf-8"),
            encoding="utf-8")
        (root / "INTENT-AUDIT.md").write_text("Decision answer: change it.\n", encoding="utf-8")
        with (root / "app.py").open("a", encoding="utf-8") as handle:
            handle.write("# unauthorized edit\n")
        try:
            verify_clean(root)
        except AssertionError as exc:
            rejected = str(exc)
        else:
            raise AssertionError("clean verifier accepted a product mutation")
        good = base / "clean-good"
        subjects.write_files(good, subjects.CLEAN_FILES)
        (good / "TASK.md").write_text(
            (HERE / "tasks/en/clean-baseline.md").read_text(encoding="utf-8"),
            encoding="utf-8")
        (good / "INTENT-AUDIT.md").write_text(
            "Decision answer: no change is warranted for the stated local use.\n",
            encoding="utf-8")
        verify_clean(good)
        return {"invalid_rejected": rejected, "valid_adjacent_accepted": True}
    if task == "delivery-adoption":
        intent = module("consumer_negative_cedar", ROOT / "evals/intent-lab/prepare_intent_subject.py")
        root = base / "cedar-bad"
        intent.prepare("task-export-handoff", root, operate=True)
        try:
            verify_delivery(root)
        except AssertionError as exc:
            rejected = str(exc)
        else:
            raise AssertionError("Cedar verifier accepted the unrepaired packet")
        good = base / "cedar-good"
        intent.prepare("task-export-handoff", good, operate=True)
        app = good / "app.py"
        code = app.read_text(encoding="utf-8")
        old = '{"claims": summaries(records)}'
        require(code.count(old) == 1, "Cedar valid control precondition moved")
        app.write_text(code.replace(old, '{"claims": records}'), encoding="utf-8")
        verify_delivery(good)
        return {"invalid_rejected": rejected, "valid_adjacent_accepted": True}
    fixture = module("consumer_negative_resume", ROOT / "evals/operation-lab/run_operation_lab.py")
    root = base / "resume-bad"
    fixture.seed(root)
    prepare = module("consumer_negative_prepare", HERE / "prepare_trial.py")
    (root / "TASK.md").write_text(prepare.prompt(task, "en"), encoding="utf-8")
    (root / "CHECKPOINT.md").write_text(prepare.RESUME_CHECKPOINT, encoding="utf-8")
    (root / "owner-notes.txt").write_text(prepare.RESUME_OWNER, encoding="utf-8")
    try:
        verify_migration(root, None)
    except AssertionError as exc:
        rejected = str(exc)
    else:
        raise AssertionError("resume verifier accepted the partial migration")
    good = base / "resume-good"
    fixture.seed(good)
    fixture.complete_fixture(good)
    (good / "CHECKPOINT.md").write_text(prepare.RESUME_CHECKPOINT, encoding="utf-8")
    (good / "owner-notes.txt").write_text(prepare.RESUME_OWNER, encoding="utf-8")
    (good / "TASK.md").write_text(prepare.prompt(task, "en"), encoding="utf-8")
    write_migration_zip(good)
    verify_migration(good, None)
    return {"invalid_rejected": rejected, "valid_adjacent_accepted": True}

def overlaps(candidate: Path, protected: Path) -> bool:
    left, right = candidate.absolute(), protected.absolute()
    if left == right or left.is_relative_to(right) or right.is_relative_to(left):
        return True
    resolved, target = candidate.resolve(strict=False), protected.resolve()
    return (resolved == target or resolved.is_relative_to(target)
            or target.is_relative_to(resolved))

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("task", choices=TASKS)
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--artifact", type=Path)
    parser.add_argument("--language", choices=("en", "zh-CN"), default="en")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--negative-control", action="store_true")
    args = parser.parse_args()
    protected = [args.candidate, HERE, ROOT / "evals" / "intent-lab",
                 ROOT / "evals" / "operation-lab", ROOT / "skills" / "repository-operational-truth-audit"]
    if args.artifact:
        protected.append(args.artifact)
    if args.output and any(overlaps(args.output, item) for item in protected):
        parser.error("--output must not overlap a candidate, fixture, seed, or artifact")
    try:
        if args.negative_control:
            with tempfile.TemporaryDirectory(prefix="consumer-negative-") as raw:
                result = {"schema": "rta-consumer-first-negative/1", "task_id": args.task,
                          "status": "passed", **negative_control(args.task, Path(raw)),
                          "target_model_invocations": 0}
        else:
            result = verify(args.task, args.candidate, args.artifact, args.language)
    except (AssertionError, OSError, ValueError, subprocess.SubprocessError) as exc:
        result = {"schema": "rta-consumer-first-verification/1", "task_id": args.task,
                  "status": "failed", "error": str(exc),
                  "target_model_invocations": 0, "os_isolation": False}
    rendered = json.dumps(result, ensure_ascii=True, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("x", encoding="utf-8") as handle:
            handle.write(rendered)
    print(rendered, end="")
    return 0 if result["status"] == "passed" else 1

if __name__ == "__main__":
    raise SystemExit(main())
