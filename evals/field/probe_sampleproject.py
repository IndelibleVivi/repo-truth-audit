#!/usr/bin/env python3
"""Offline real wheel/editable selection experiment; prepare seed explicitly first."""
from __future__ import annotations

import argparse
import io
import json
import os
from pathlib import Path
import subprocess
import tarfile
import tempfile

PIN = "621e4974ca25ce531773def586ba3ed8e736b3fc"
EXPECTED = {
    "baseline-wheel": (11, "wheel"),
    "source-only": (12, "source"),
    "source-only-installed": (11, "wheel"),
    "delivered-wheel": (12, "wheel"),
    "editable": (12, "editable"),
    "owner-edit-editable": (13, "editable"),
    "owner-edit-frozen-wheel": (12, "wheel"),
    "owner-edit-delivered-wheel": (13, "wheel"),
}
CONSUMER = '''import importlib.metadata as m, json, sys
import sample.simple as s
try:
    d = m.distribution("sampleproject")
    url = json.loads(d.read_text("direct_url.json") or "null")
except m.PackageNotFoundError:
    url = None
print(json.dumps({"value": s.add_one(10), "module_file": s.__file__,
                  "direct_url": url, "prefix": sys.prefix}))
'''


class SetupBlocked(Exception):
    def __init__(self, reason, commands=None):
        super().__init__(reason)
        self.commands = commands or []


def portable_report(report, paths):
    from urllib.parse import quote
    rendered = json.dumps(report)
    for path, label in paths:
        rendered = rendered.replace(quote(str(path)), label).replace(str(path), label)
    return json.loads(rendered)


def consumer_reading(stdout, exit_code):
    if exit_code:
        return {"exit_code": exit_code, "observation_error": "ready consumer exited nonzero"}
    try:
        row = json.loads(stdout)
        if not isinstance(row, dict):
            raise ValueError("expected an object")
        return row
    except ValueError as exc:
        return {"exit_code": exit_code, "observation_error": "invalid consumer JSON: " + str(exc)}


def overlaps(a: Path, b: Path) -> bool:
    a, b = a.resolve(), b.resolve()
    return a.is_relative_to(b) or b.is_relative_to(a)


def protect(source: Path, seed: Path, output: Path | None = None) -> None:
    if overlaps(source, seed):
        raise ValueError("source and seed must be disjoint")
    if output and any(overlaps(output, p) for p in (source, seed)):
        raise ValueError("output must be disjoint from source and seed")


def matrix_matches(rows: dict) -> bool:
    if not isinstance(rows, dict) or set(rows) != set(EXPECTED):
        return False
    for name, (value, kind) in EXPECTED.items():
        row = rows[name]
        if not isinstance(row, dict) or row.get("observation_error") or row.get("value") != value:
            return False
        origin = row.get("module_file", "")
        direct = row.get("direct_url") or {}
        if not isinstance(origin, str) or not isinstance(direct, dict):
            return False
        if kind == "wheel":
            if not origin.startswith("<temporary>/regular/") or "/site-packages/sample/simple.py" not in origin:
                return False
            if "archive_info" not in direct or not direct.get("url", "").endswith(".whl"):
                return False
        else:
            if origin != "<temporary>/source/src/sample/simple.py":
                return False
            info = direct.get("dir_info", {})
            if kind == "editable" and (not isinstance(info, dict) or info.get("editable") is not True
                                       or direct.get("url") != "file://<temporary>/source"):
                return False
    return True


def snapshot(root: Path) -> dict:
    """Detect input writes using names, sizes, nanosecond mtimes and link targets."""
    return {str(p.relative_to(root)): (p.lstat().st_size, p.lstat().st_mtime_ns,
                                      os.readlink(p) if p.is_symlink() else None)
            for p in root.rglob("*") if not p.is_dir() or p.is_symlink()}


def probe(source: Path, seed: Path) -> dict:
    source, seed = source.resolve(), seed.resolve()
    protect(source, seed)
    # Inherited PIP_FIND_LINKS/requirements could otherwise reintroduce URLs.
    env = {key: value for key, value in os.environ.items() if not key.startswith("PIP_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", PIP_NO_INDEX="1",
               PIP_NO_CACHE_DIR="1", PIP_DISABLE_PIP_VERSION_CHECK="1", PIP_CONFIG_FILE=os.devnull,
               PIP_NO_BUILD_ISOLATION="1")
    for key in ("PYTHONPATH", "PYTHONHOME"):
        env.pop(key, None)
    commands = []
    paths = [(source, "<source>"), (seed, "<seed>")]
    def run(argv, cwd=source, require_success=True):
        try:
            cp = subprocess.run([str(x) for x in argv], cwd=cwd, env=env,
                                capture_output=True, text=True, encoding="utf-8", timeout=180)
        except (OSError, subprocess.SubprocessError) as exc:
            commands.append({"argv": [str(x) for x in argv], "exit_code": None,
                             "stdout": "", "stderr": str(exc)})
            safe = portable_report(commands, paths)
            raise SetupBlocked("command could not execute", safe) from exc
        commands.append({"argv": [str(x) for x in argv], "exit_code": cp.returncode,
                         "stdout": cp.stdout, "stderr": cp.stderr})
        if require_success and cp.returncode:
            raise SetupBlocked("setup command failed", portable_report(commands, paths))
        return cp.stdout
    sha = run(["git", "rev-parse", "HEAD"]).strip()
    if sha != PIN or run(["git", "status", "--porcelain"]):
        raise SetupBlocked("Require clean source checkout at " + PIN)
    before_source, before_seed = snapshot(source), snapshot(seed)
    python = seed / "bin/python"
    versions = json.loads(run([python, "-c", 'import sys,json,importlib.metadata as m; print(json.dumps({"python":sys.version, **{n:m.version(n) for n in ("pip","setuptools","wheel","packaging","peppercorn")}}))']))
    with tempfile.TemporaryDirectory(prefix="rta-sampleproject-run-") as raw:
        root = Path(raw).resolve()
        paths.insert(0, (root, "<temporary>"))
        if any(overlaps(root, p) for p in (source, seed)):
            raise SetupBlocked("scratch overlaps protected inputs")
        work = root / "source"
        work.mkdir()
        archive = subprocess.check_output(["git", "archive", PIN], cwd=source)
        with tarfile.open(fileobj=io.BytesIO(archive)) as tf:
            for member in tf:
                dest = work / member.name
                if not dest.resolve().is_relative_to(work) or not (member.isdir() or member.isfile()):
                    raise SetupBlocked("unsupported archive path/type")
                if member.isdir():
                    dest.mkdir(parents=True, exist_ok=True)
                else:
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    dest.write_bytes(tf.extractfile(member).read())
        backend = (work / "pyproject.toml").read_text(encoding="utf-8")
        if 'build-backend = "setuptools.build_meta"' not in backend or 'requires = ["setuptools"]' not in backend:
            raise SetupBlocked("Pinned backend changed")
        target = work / "src/sample/simple.py"
        if target.read_text(encoding="utf-8") != "def add_one(number):\n    return number + 1\n":
            raise SetupBlocked("Pinned mutation target changed")
        regular, editable = root / "regular", root / "editable"
        for venv in (regular, editable):
            run([python, "-m", "venv", "--without-pip", venv], root)
            run([python, "-m", "pip", "--python", venv / "bin/python", "install", "--no-index",
                 "--find-links", seed / "wheelhouse", "setuptools", "wheel", "peppercorn"], root)
        def pip(venv, *args):
            return run([python, "-m", "pip", "--python", venv / "bin/python", *args], root)
        build_count = 0
        def deliver():
            nonlocal build_count
            build_count += 1
            wheels = root / ("wheel-" + str(build_count))
            run([python, "-m", "pip", "wheel", "--no-deps", "--no-index", "--no-build-isolation",
                 "--wheel-dir", wheels, work], root)
            wheel, = wheels.glob("sampleproject-*.whl")
            pip(regular, "install", "--no-index", "--no-deps", "--force-reinstall", wheel)
        rows = {}
        def observe(name, venv):
            stdout = run([venv / "bin/python", "-I", "-B", "-c", CONSUMER], root, require_success=False)
            rows[name] = consumer_reading(stdout, commands[-1]["exit_code"])
        def mutate(number):
            # Different byte lengths avoid stale timestamp/size pyc ambiguity too.
            target.write_text(f"def add_one(number):\n    return number + {number}  # constructed owner value {number}\n", encoding="utf-8")
        deliver()
        observe("baseline-wheel", regular)
        mutate(2)
        source_stdout = run([python, "-I", "-B", "-c",
            "import sys; sys.path.insert(0," + repr(str(work / "src")) + ");" + CONSUMER], root, require_success=False)
        rows["source-only"] = consumer_reading(source_stdout, commands[-1]["exit_code"])
        observe("source-only-installed", regular)
        deliver()
        observe("delivered-wheel", regular)
        pip(editable, "install", "--no-index", "--no-deps", "--no-build-isolation", "--editable", work)
        observe("editable", editable)
        mutate(3)
        observe("owner-edit-editable", editable)
        observe("owner-edit-frozen-wheel", regular)
        deliver()
        observe("owner-edit-delivered-wheel", regular)
        report = {"schema_version": 1, "case": "sampleproject-installed-selection",
                  "source_repository": "https://github.com/pypa/sampleproject", "source_commit": PIN,
                  "source_input": "git archive of exact pin; no working-tree bytes",
                  "versions": versions, "backend": "setuptools.build_meta",
                  "observations": rows, "commands": commands,
                  "source_clean_and_unchanged": snapshot(source) == before_source,
                  "seed_unchanged": snapshot(seed) == before_seed,
                  "input_preservation_evidence": "names/sizes/mtime/link targets unchanged; not byte identity",
                  "network_policy": "pip --no-index; --no-deps for project; --no-build-isolation; explicit preseeded wheelhouse",
                  "network_policy_is_os_isolation": False, "target_model_invocations": 0,
                  "interpretation": "Constructed delivery failure for source-only completion; frozen installed wheel after later owner edit is legitimate."}
        report = portable_report(report, paths)
        report["matrix_matches_expectation"] = matrix_matches(report["observations"])
        report["status"] = "observed" if (report["matrix_matches_expectation"] and
                             report["source_clean_and_unchanged"] and report["seed_unchanged"]) else "expectation-mismatch"
        return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--seed", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    try:
        protect(args.source, args.seed, args.output)
    except ValueError as exc:
        parser.error(str(exc))
    try:
        report = probe(args.source, args.seed)
    except (SetupBlocked, OSError, ValueError, subprocess.SubprocessError) as exc:
        report = {"schema_version": 1, "status": "setup-blocked", "reason": str(exc),
                  "matrix_matches_expectation": False, "commands": getattr(exc, "commands", [])}
    rendered = json.dumps(report, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return {"observed": 0, "expectation-mismatch": 1, "setup-blocked": 2}[report["status"]]


if __name__ == "__main__":
    raise SystemExit(main())
