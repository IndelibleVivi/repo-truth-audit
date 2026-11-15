#!/usr/bin/env python3
"""Probe Viper's selected environment-to-struct path with a real Go consumer.

Requires viper_consumer.go beside this file, a clean pinned Viper checkout, an
actual Go compiler >=1.23 and populated module dependencies. This tool never
downloads, installs, patches Viper, or invokes a model. A missing cache/compiler
is setup-blocked evidence, not a product semantic failure.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile

PIN = "528f7416c4b56a4948673984b190bf8713f0c3c4"
EXPECTED = {
    "automatic-only": [("alpha", "alpha", "", []), ("beta", "beta", "", [])],
    "bound-key": [("alpha", "alpha", "alpha", ["host"]), ("beta", "beta", "beta", ["host"])],
    "default-key": [("alpha", "alpha", "alpha", ["host"]), ("beta", "beta", "beta", ["host"])],
    "experimental-struct": [("alpha", "alpha", "alpha", []), ("beta", "beta", "beta", [])],
    "snapshot-override": [("alpha", "alpha", "alpha", ["host"]), ("beta", "alpha", "alpha", ["host"])],
    "empty-allowed-false": [("", "fallback", "fallback", ["host"])],
    "empty-allowed-true": [("", "", "", ["host"])],
}


def matrix_matches(rows):
    if not isinstance(rows, list) or len(rows) != len(EXPECTED):
        return False
    if len({row.get("variant") for row in rows}) != len(rows):
        return False
    for row in rows:
        values = [(r["environment"], r["direct"], r["decoded"]["host"], r["known_keys"])
                  for r in row["readings"]]
        if values != EXPECTED.get(row["variant"]):
            return False
        if any(r["error"] for r in row["readings"]):
            return False
    return True


def run(command, **kwargs):
    return subprocess.run(command, capture_output=True, text=True, timeout=180, **kwargs)


def probe(args):
    repo = args.repo.resolve()
    go = str(args.go.resolve())
    revision = run(["git", "rev-parse", "HEAD"], cwd=repo)
    clean = run(["git", "status", "--porcelain"], cwd=repo)
    if revision.returncode or revision.stdout.strip() != PIN or clean.returncode or clean.stdout:
        raise ValueError("Require a clean checkout at Viper pin " + PIN)
    env = dict(os.environ, GOTOOLCHAIN="local", GOPROXY="off", GOSUMDB="off",
               GOWORK="off", GOENV="off", GOFLAGS="")
    if args.module_cache:
        env["GOMODCACHE"] = str(args.module_cache.resolve())
    version = run([go, "version"], env=env)
    if version.returncode or not version.stdout.startswith("go version go"):
        raise ValueError("Selected executable is not a working Go compiler: " + version.stderr.strip())
    consumer = Path(__file__).with_name("viper_consumer.go").read_bytes()
    with tempfile.TemporaryDirectory(prefix="rta-viper-") as raw:
        root = Path(raw)
        env["GOCACHE"] = str(args.build_cache.resolve() if args.build_cache else root / "build-cache")
        module = (repo / "go.mod").read_text(encoding="utf-8")
        if module.count("module github.com/spf13/viper\n") != 1:
            raise ValueError("Unexpected pinned module declaration")
        module = module.replace("module github.com/spf13/viper\n",
                                "module example.invalid/rta-viper-consumer\n", 1)
        module += "\nrequire github.com/spf13/viper v0.0.0\n"
        module += "replace github.com/spf13/viper => " + json.dumps(str(repo)) + "\n"
        (root / "go.mod").write_text(module, encoding="utf-8")
        (root / "go.sum").write_bytes((repo / "go.sum").read_bytes())
        (root / "main.go").write_bytes(consumer)
        selection = run([go, "list", "-m", "-json", "github.com/spf13/viper"], cwd=root, env=env)
        binary = root / ("consumer.exe" if os.name == "nt" else "consumer")
        build = run([go, "build", "-mod=readonly", "-o", str(binary), "."], cwd=root, env=env)
        result = None
        observation_error = ""
        if build.returncode == 0:
            try:
                result = run([str(binary)], cwd=root, env=env)
            except (OSError, subprocess.SubprocessError) as exc:
                observation_error = str(exc)
        scrub = lambda value: value.replace(str(root), "<temporary>").replace(str(repo), "<repo>")
        selected = json.loads(selection.stdout) if selection.returncode == 0 else {}
        selection_matches = selected.get("Replace", {}).get("Dir") == str(repo)
        rows = []
        matched = False
        if result is not None:
            try:
                rows = json.loads(result.stdout)
                matched = result.returncode == 0 and selection_matches and matrix_matches(rows)
            except (ValueError, KeyError, TypeError, AttributeError) as exc:
                observation_error = "Consumer returned invalid observations: " + str(exc)
        after = run(["git", "status", "--porcelain"], cwd=repo)
        unchanged = after.returncode == 0 and after.stdout == clean.stdout
        return {
            "schema_version": 1, "case": "viper-environment-struct-selection",
            "source_repository": "https://github.com/spf13/viper", "source_commit": PIN,
            "source_clean_and_unchanged": unchanged,
            "source_file_sha256": {name: hashlib.sha256((repo / name).read_bytes()).hexdigest()
                                   for name in ("go.mod", "go.sum", "viper.go", "experimental.go",
                                                "internal/features/bind_struct_default.go")},
            "go_version": version.stdout.strip(),
            "consumer_sha256": hashlib.sha256(consumer).hexdigest(),
            "module_selection": json.loads(scrub(selection.stdout)) if selection.returncode == 0 else None,
            "module_selection_matches_pin": selection_matches,
            "module_selection_stderr": scrub(selection.stderr),
            "build": {
                "command": ["<go>", "build", "-mod=readonly", "-o", "<temporary>/consumer", "."],
                "exit_code": build.returncode, "stdout": scrub(build.stdout), "stderr": scrub(build.stderr),
            },
            "execution": {
                "command": ["<temporary>/consumer"], "attempted": build.returncode == 0,
                "exit_code": result.returncode if result is not None else None,
            },
            "network_policy": "GOPROXY=off; GOSUMDB=off; GOTOOLCHAIN=local; GOWORK=off",
            "network_policy_is_os_isolation": False,
            "stdout": result.stdout if result is not None else "",
            "stderr": scrub(result.stderr) if result is not None else "",
            "observation_error": scrub(observation_error), "observations": rows,
            "matrix_matches_expectation": matched,
            "status": "observed" if matched and unchanged else (
                "setup-blocked" if build.returncode else "expectation-mismatch"),
            "interpretation": "Default limitation and valid selected alternatives; no blanket library-defect or release-compatibility claim.",
        }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--go", type=Path, required=True, help="explicit Go compiler executable")
    parser.add_argument("--module-cache", type=Path)
    parser.add_argument("--build-cache", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    # Reject before even writing an error receipt: that output could itself
    # overwrite an observed source file. Resolve existing symlink ancestors.
    repo = args.repo.resolve()
    for name in ("output", "build_cache"):
        candidate = getattr(args, name)
        if candidate and candidate.resolve().is_relative_to(repo):
            parser.error("--" + name.replace("_", "-") + " must resolve outside the observed repository")
    try:
        report = probe(args)
    except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError) as exc:
        report = {"schema_version": 1, "case": "viper-environment-struct-selection",
                  "status": "setup-blocked", "reason": str(exc),
                  "matrix_matches_expectation": False}
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if report["status"] == "observed" else (2 if report["status"] == "setup-blocked" else 1)


if __name__ == "__main__":
    raise SystemExit(main())
