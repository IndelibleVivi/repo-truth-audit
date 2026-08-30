#!/usr/bin/env python3
"""Prove that controlled cases carry their intended dirty or clean truth."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

from common import ROOT

CASES = ROOT / "evals" / "cases"


def run(argv: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(argv, cwd=cwd, check=False, capture_output=True, text=True)


def check_source_artifact_split(errors: list[str]) -> None:
    fixture = CASES / "source-artifact-split" / "fixture"
    source_test = run([sys.executable, "tests/test_source.py"], fixture)
    if source_test.returncode != 0:
        errors.append(f"source-artifact-split source test did not pass: {source_test.stderr}")
    distribution = json.loads((fixture / "distribution.json").read_text(encoding="utf-8"))
    artifact = run([sys.executable, distribution["entrypoint"]], fixture)
    if artifact.returncode != 0 or artifact.stdout.strip() != "artifact-v1":
        errors.append("source-artifact-split distributed entrypoint is not the intended stale v1")
    source = run([sys.executable, "src/cli.py"], fixture)
    if source.stdout.strip() != "artifact-v2":
        errors.append("source-artifact-split source entrypoint is not v2")
    if "artifact-v2" not in (fixture / "README.md").read_text(encoding="utf-8"):
        errors.append("source-artifact-split README lost the v2 claim")


def check_false_green_ordering(errors: list[str]) -> None:
    fixture = CASES / "false-green-ordering" / "fixture"
    gate = run(["bash", "test_operator_surface.sh"], fixture)
    if gate.returncode != 0 or "PASS" not in gate.stdout:
        errors.append("false-green-ordering presence gate is no longer green")
    trace = run(["bash", "deploy.sh", "--trace"], fixture)
    if trace.returncode != 0 or trace.stdout.splitlines() != ["REMOTE_WRITE", "ROLE_CHECK"]:
        errors.append("false-green-ordering fixture no longer writes before role check")


def check_authority_drift(errors: list[str]) -> None:
    fixture = CASES / "authority-drift" / "fixture"
    agents = (fixture / "AGENTS.md").read_text(encoding="utf-8")
    readme = (fixture / "README.md").read_text(encoding="utf-8")
    status = (fixture / "docs/status.md").read_text(encoding="utf-8")
    head = json.loads((fixture / "CURRENT_HEAD.json").read_text(encoding="utf-8"))
    if "Current MVP" not in agents or "moved beyond the original MVP" not in readme:
        errors.append("authority-drift fixture lost its contradictory current authority")
    if head.get("date") == status.partition("Last updated: ")[2].splitlines()[0].strip():
        errors.append("authority-drift fixture status is no longer stale")


def check_intentional_multiplicity(errors: list[str]) -> None:
    fixture = CASES / "intentional-multiplicity" / "fixture"
    stable = json.loads((fixture / "releases/stable.json").read_text(encoding="utf-8"))
    development = json.loads((fixture / "development/current.json").read_text(encoding="utf-8"))
    readme = (fixture / "README.md").read_text(encoding="utf-8")
    changelog = (fixture / "CHANGELOG.md").read_text(encoding="utf-8")
    if stable.get("install_ref") != "v1.0.0" or "--ref v1.0.0" not in readme:
        errors.append("intentional-multiplicity lost stable install selection")
    if development.get("channel") != "main" or "## Unreleased" not in changelog:
        errors.append("intentional-multiplicity lost isolated development selection")
    stable_result = run(
        [sys.executable, "selector.py", "--channel", "stable", "--ref", "v1.0.0"],
        fixture,
    )
    development_result = run(
        [sys.executable, "selector.py", "--channel", "development"], fixture
    )
    if stable_result.returncode != 0 or stable_result.stdout.strip() != "releases/v1.0.0":
        errors.append("intentional-multiplicity stable artifact selector is not coherent")
    if (
        development_result.returncode != 0
        or development_result.stdout.strip() != "development/main"
    ):
        errors.append("intentional-multiplicity development selector is not coherent")
    for argv in (
        [sys.executable, "selector.py"],
        [sys.executable, "selector.py", "--channel", "stable", "--ref", "main"],
        [
            sys.executable,
            "selector.py",
            "--channel",
            "development",
            "--ref",
            "v1.0.0",
        ],
    ):
        if run(argv, fixture).returncode == 0:
            errors.append("intentional-multiplicity selector accepted a cross-boundary route")


def check_no_decision(errors: list[str]) -> None:
    fixture = CASES / "no-decision-stop" / "fixture"
    if set(path.name for path in fixture.iterdir()) != {"README.md", "app.py"}:
        errors.append("no-decision-stop fixture should remain a small coherent repository")


def check_unobserved_restore(errors: list[str]) -> None:
    fixture = CASES / "unobserved-restore-dependency" / "fixture"
    result = run([sys.executable, "restore.py", "--dry-run"], fixture)
    if result.returncode != 2 or "REMOTE_SCHEMA_VERSION is required" not in result.stderr:
        errors.append("unobserved-restore-dependency no longer exposes the missing schema identity")
    if "one-command restore" not in (fixture / "README.md").read_text(encoding="utf-8"):
        errors.append("unobserved-restore-dependency lost its restore claim")


def run_checks() -> list[str]:
    errors: list[str] = []
    check_source_artifact_split(errors)
    check_false_green_ordering(errors)
    check_authority_drift(errors)
    check_intentional_multiplicity(errors)
    check_no_decision(errors)
    check_unobserved_restore(errors)
    return errors


def main() -> int:
    errors = run_checks()
    if errors:
        print("Controlled fixture self-test failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("Six controlled repository-truth fixtures: PASS")
    print("Target-model invocations: 0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
