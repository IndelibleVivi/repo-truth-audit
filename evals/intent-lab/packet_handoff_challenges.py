"""Evaluator-only Cedar repairs and counterexamples; never copied to a subject.

These are trusted synthetic candidates, not hostile code. The challenges test
whether only the exported packet is sufficient after a real information handoff.
They exercise the acceptance oracle and make no model-performance claim.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from unittest.mock import patch

import task_subjects as task
from prepare_intent_subject import prepare


def candidate(root: Path, variant: str) -> None:
    """Apply a named, evaluator-owned candidate to a freshly prepared Cedar."""
    app = root / "app.py"
    code = app.read_text(encoding="utf-8")
    if variant in {"complete", "alternate-layout", "stale-artifact"}:
        if variant == "stale-artifact":
            (root / "dist").mkdir()
            (root / "dist/app.py").write_text(code, encoding="utf-8")
            (root / "launch.json").write_text('{"entry": "dist/app.py"}\n', encoding="utf-8")
            (root / "bundle.json").write_text('["dist/app.py"]\n', encoding="utf-8")
        if variant == "alternate-layout":
            code = code.replace('records = payload["claims"]',
                                'records = payload.get("claims", payload.get("arguments"))')
            code = code.replace('{"claims": summaries(records)}', '{"arguments": records}')
        else:
            code = code.replace('{"claims": summaries(records)}', '{"claims": records}')
    elif variant in {"xdg-data-cache", "appdata-cache"}:
        # A keyed cache survives crossed packet histories if producer and
        # recipient accidentally inherit the same application-data directory.
        # The challenge runner always supplies private disposable ambient paths.
        variable = "XDG_DATA_HOME" if variant == "xdg-data-cache" else "APPDATA"
        cache_root = f'Path(__import__("os").environ["{variable}"]) / "cedar-packet-cache"'
        code = code.replace('        args.output.write_text(json.dumps(',
                            f'        cache = {cache_root}\n'
                            '        cache.mkdir(parents=True, exist_ok=True)\n'
                            '        cache_key = __import__("uuid").uuid4().hex\n'
                            '        (cache / cache_key).write_text(json.dumps({"claims": records}), encoding="utf-8")\n'
                            '        args.output.write_text(json.dumps(')
        code = code.replace('{"claims": summaries(records)}',
                            '{"claims": summaries(records), "cache_key": cache_key}')
        code = code.replace('        if any("references" not in row for row in records):',
                            '        if any("references" not in row for row in records):\n'
                            f'            cache = {cache_root}\n'
                            '            records = json.loads((cache / payload["cache_key"]).read_text(encoding="utf-8"))["claims"]\n'
                            '        if any("references" not in row for row in records):')
    elif variant in {"relative-producer-cache", "absolute-producer-cache", "packet-sidecar",
                     "home-cache", "temporary-cache", "artifact-cache-fallback"}:
        # Keep the exported packet summary-only. A same-directory round trip can
        # hide the missing relation by using another file the recipient never gets.
        cache = {
            "relative-producer-cache": 'Path(".producer-cache.json")',
            "absolute-producer-cache": 'Path(__file__).resolve().with_name(".producer-cache.json")',
            "packet-sidecar": 'args.output.with_suffix(".citations.json")',
            "home-cache": 'Path.home() / ".producer-cache.json"',
            "temporary-cache": 'Path(__import__("tempfile").gettempdir()) / ".producer-cache.json"',
            "artifact-cache-fallback": 'Path(".producer-cache.json")',
        }[variant]
        cache = f"({cache})"
        read_cache = 'args.packet.with_suffix(".citations.json")' if variant == "packet-sidecar" else cache
        code = code.replace('        args.output.write_text(json.dumps(',
                            f'        {cache}.write_text(json.dumps({{"claims": records}}), encoding="utf-8")\n'
                            '        args.output.write_text(json.dumps(')
        code = code.replace('        if any("references" not in row for row in records):',
                            '        if any("references" not in row for row in records):\n'
                            f'            records = json.loads({read_cache}.read_text(encoding="utf-8"))["claims"]\n'
                            '        if any("references" not in row for row in records):')
        if variant == "artifact-cache-fallback":
            # Source correctly includes citations through configuration. The
            # declared artifact omits that configuration and falls back to a
            # producer cache. The final gate must reach and reject that surface.
            (root / "packet-policy.json").write_text('{"include_citations": true}\n', encoding="utf-8")
            code = code.replace('{"claims": summaries(records)}',
                '{"claims": records if Path("packet-policy.json").is_file() else summaries(records)}')
    elif variant == "absolute-cache-pointer":
        # The packet points back to the producer by absolute path. Moving just
        # the packet is insufficient if the evaluator leaves that producer alive.
        code = code.replace('{"claims": summaries(records)}',
                            '{"claims": summaries(records), "cache": str(Path(".producer-cache.json").resolve())}')
        code = code.replace('        args.output.write_text(json.dumps(',
                            '        Path(".producer-cache.json").write_text(json.dumps({"claims": records}), encoding="utf-8")\n'
                            '        args.output.write_text(json.dumps(')
        code = code.replace('        if any("references" not in row for row in records):',
                            '        if any("references" not in row for row in records):\n'
                            '            records = json.loads(Path(payload["cache"]).read_text(encoding="utf-8"))["claims"]\n'
                            '        if any("references" not in row for row in records):')
    elif variant == "input-sidecar-pointer":
        # A cache beside the supplied input survives a check that merely unlinks
        # input.json; the producer's entire data directory must be unavailable.
        code = code.replace('{"claims": summaries(records)}',
                            '{"claims": summaries(records), "cache": str(path.with_suffix(".cache.json").resolve())}')
        code = code.replace('        args.output.write_text(json.dumps(',
                            '        path.with_suffix(".cache.json").write_text(json.dumps({"claims": records}), encoding="utf-8")\n'
                            '        args.output.write_text(json.dumps(')
        code = code.replace('        if any("references" not in row for row in records):',
                            '        if any("references" not in row for row in records):\n'
                            '            records = json.loads(Path(payload["cache"]).read_text(encoding="utf-8"))["claims"]\n'
                            '        if any("references" not in row for row in records):')
    elif variant == "unchanged":
        pass
    else:
        raise ValueError(f"unknown packet candidate: {variant}")
    app.write_text(code, encoding="utf-8")


VARIANTS = {
    "complete": True,
    "alternate-layout": True,
    "unchanged": False,
    "relative-producer-cache": False,
    "absolute-producer-cache": False,
    "packet-sidecar": False,
    "home-cache": False,
    "temporary-cache": False,
    "xdg-data-cache": False,
    "appdata-cache": False,
    "artifact-cache-fallback": False,
    "absolute-cache-pointer": False,
    "input-sidecar-pointer": False,
    "stale-artifact": False,
}


def private_application_data(root: Path) -> dict[str, str]:
    """Private ambient paths make cache challenges independent of host homes."""
    values = {}
    for variable in ("XDG_DATA_HOME", "APPDATA"):
        path = root / variable.lower()
        path.mkdir(parents=True)
        values[variable] = str(path)
    return values


def local_roundtrip(root: Path) -> bool:
    """Verify a false repair really works locally, rather than merely crashing."""
    with tempfile.TemporaryDirectory(prefix="cedar-local-roundtrip-") as raw:
        work = Path(raw)
        product = work / "producer"
        shutil.copytree(root, product, ignore=shutil.ignore_patterns(".git", "__pycache__"))
        env = task._role_environment(work / "environment")
        store = task.probe_stores()[0]
        source, packet = work / "unseen.json", work / "packet.json"
        source.write_text(task.encode(store), encoding="utf-8")
        def invoke(*args):
            return subprocess.run([sys.executable, "-B", str(product / "cedar"), *map(str, args)],
                                  cwd=product, env=env, capture_output=True, encoding="utf-8", timeout=20)
        exported = invoke("export", "--store", source, "--output", packet)
        if exported.returncode != 0:
            return False
        source.unlink()
        result = invoke("affected", "--packet", packet, "--source", "lab-z", "--revision", 4)
        return result.returncode == 0 and json.loads(result.stdout) == task.expected_affected(store, "lab-z", 4)


def run_challenges() -> dict:
    results = []
    for variant, expected in VARIANTS.items():
        with tempfile.TemporaryDirectory(prefix="cedar-challenge-") as raw:
            root = Path(raw) / "candidate"
            prepare("task-export-handoff", root)
            candidate(root, variant)
            # Every cache counterexample must first demonstrate its deceptive
            # local success. A syntax/setup failure is not a valid challenge.
            needs_local_pass = "cache" in variant or "sidecar" in variant
            local_pass = local_roundtrip(root) if needs_local_pass else None
            # The inherited data directories must also be private before an
            # oracle is fixed: never exercise a challenge in the user's home.
            with patch.dict(os.environ, private_application_data(Path(raw) / "ambient")):
                try:
                    task.assert_repair(root)
                except (AssertionError, OSError, ValueError) as exc:
                    accepted, reason = False, str(exc).splitlines()[0]
                else:
                    accepted, reason = True, None
            results.append({"candidate": variant, "expected_acceptance": expected,
                            "observed_acceptance": accepted,
                            "matched": accepted == expected and (not needs_local_pass or local_pass),
                            "same_workspace_success": local_pass,
                            "failure_surface": ("declared_artifact" if reason and "artifact-received" in reason
                                                else "selected_source" if reason else None),
                            "rejection": reason})
    return {"schema": "rta-packet-handoff-challenges/1",
            "status": "passed" if all(row["matched"] for row in results) else "failed",
            "results": results, "target_model_invocations": 0,
            "boundary": "trusted disposable producer/recipient directories; only packet bytes transfer",
            "not_observed": ["OS-enforced isolation", "hostile-code containment", "human review time"]}
