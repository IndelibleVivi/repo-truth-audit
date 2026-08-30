#!/usr/bin/env python3
"""Validate the standalone repository and Skill package contract."""

from __future__ import annotations

import csv
import json
from pathlib import Path
import re
import sys
from typing import Iterable

from common import ROOT, SKILL_DIR, SKILL_NAME, file_sha256, read_version

SUL_SHA256 = "c6d0dde0f0463c800e542d7d64237ffef37f43b17004975a558604f17b5d1af1"

PUBLIC_DOC_PAIRS = {
    "README.md": "README.zh-CN.md",
    "CHANGELOG.md": "CHANGELOG.zh-CN.md",
    "LICENSE-DOCUMENTATION.md": "LICENSE-DOCUMENTATION.zh-CN.md",
    "LICENSING.md": "LICENSING.zh-CN.md",
    "docs/product-spec.md": "docs/product-spec.zh-CN.md",
    "docs/evidence-model.md": "docs/evidence-model.zh-CN.md",
    "docs/research-basis.md": "docs/research-basis.zh-CN.md",
    "docs/current-state.md": "docs/current-state.zh-CN.md",
    "docs/architecture/README.md": "docs/architecture/README.zh-CN.md",
    "docs/releases/v0.1.0.md": "docs/releases/v0.1.0.zh-CN.md",
}

EXPECTED_CASES = {
    "authority-drift",
    "false-green-ordering",
    "intentional-multiplicity",
    "no-decision-stop",
    "source-artifact-split",
    "unobserved-restore-dependency",
}

REQUIRED_FILES = {
    ".github/workflows/validate.yml",
    ".gitignore",
    "AGENTS.md",
    "CHANGELOG.md",
    "CHANGELOG.zh-CN.md",
    "LICENSE",
    "LICENSE-DOCUMENTATION.md",
    "LICENSE-DOCUMENTATION.zh-CN.md",
    "LICENSING.md",
    "LICENSING.zh-CN.md",
    "NOTICE.md",
    "README.md",
    "README.zh-CN.md",
    "VERSION",
    "docs/current-state.md",
    "docs/architecture/audit-runtime-model.json",
    "docs/architecture/README.md",
    "docs/architecture/README.zh-CN.md",
    "docs/current-state.zh-CN.md",
    "docs/evidence-model.md",
    "docs/evidence-model.zh-CN.md",
    "docs/product-spec.md",
    "docs/product-spec.zh-CN.md",
    "docs/research-basis.md",
    "docs/research-basis.zh-CN.md",
    "docs/releases/v0.1.0.md",
    "docs/releases/v0.1.0.zh-CN.md",
    "evals/README.md",
    "evals/activation-prompts.csv",
    "fieldlab-pack.json",
    "scripts/common.py",
    "scripts/install_skill.py",
    "scripts/selftest.py",
    "scripts/validate_architecture.py",
    "scripts/validate_repository.py",
    "skills/repository-operational-truth-audit/SKILL.md",
    "skills/repository-operational-truth-audit/LICENSE.txt",
    "skills/repository-operational-truth-audit/NOTICE.md",
    "skills/repository-operational-truth-audit/agents/openai.yaml",
    "tests/test_fixtures.py",
    "tests/test_architecture.py",
    "tests/test_install_skill.py",
    "tests/test_repository.py",
}


def read(relative: str, errors: list[str]) -> str:
    path = ROOT / relative
    if not path.is_file():
        errors.append(f"missing required file: {relative}")
        return ""
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        errors.append(f"file is not valid UTF-8: {relative}")
        return ""


def text_files() -> Iterable[Path]:
    for path in ROOT.rglob("*"):
        if ".git" in path.parts or not path.is_file() or path.is_symlink():
            continue
        if path.suffix.lower() in {
            ".md",
            ".yaml",
            ".yml",
            ".json",
            ".csv",
            ".py",
            ".sh",
            ".svg",
            ".txt",
        }:
            yield path


def validate_markdown_links(errors: list[str]) -> None:
    link_pattern = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
    for path in ROOT.rglob("*.md"):
        if ".git" in path.parts or path.is_symlink():
            continue
        content = path.read_text(encoding="utf-8")
        for match in link_pattern.finditer(content):
            target = match.group(1).strip().strip("<>")
            if not target or target.startswith(("#", "http://", "https://", "mailto:")):
                continue
            target_path = target.split("#", 1)[0]
            if not target_path:
                continue
            resolved = (path.parent / target_path).resolve()
            if resolved != ROOT and ROOT not in resolved.parents:
                errors.append(
                    f"{path.relative_to(ROOT)} contains repository-escaping link: {target!r}"
                )
            elif not resolved.exists():
                errors.append(
                    f"{path.relative_to(ROOT)} contains missing relative link: {target!r}"
                )


def validate() -> list[str]:
    errors: list[str] = []
    for required in sorted(REQUIRED_FILES):
        if not (ROOT / required).is_file():
            errors.append(f"missing required file: {required}")

    version = read("VERSION", errors).strip()
    if version != "0.1.0":
        errors.append(f"VERSION must be the public release version '0.1.0', got {version!r}")

    readme = read("README.md", errors)
    readme_zh = read("README.zh-CN.md", errors)
    current_state = read("docs/current-state.md", errors)
    current_state_zh = read("docs/current-state.zh-CN.md", errors)
    for relative, content in (
        ("README.md", readme),
        ("README.zh-CN.md", readme_zh),
        ("docs/current-state.md", current_state),
        ("docs/current-state.zh-CN.md", current_state_zh),
    ):
        if version and f"`{version}`" not in content and f"`v{version}`" not in content:
            errors.append(f"{relative} is not aligned with VERSION {version}")

    readme_requirements = {
        "README.md": (
            "[简体中文](README.zh-CN.md)",
            "```mermaid",
            "flowchart TB",
            "source-available, not OSI open source",
            "--ref v0.1.0",
            "Sustainable Use License 1.0",
            "CC BY-NC-SA 4.0",
        ),
        "README.zh-CN.md": (
            "[English](README.md)",
            "```mermaid",
            "flowchart TB",
            "source-available，不是 OSI open source",
            "--ref v0.1.0",
            "Sustainable Use License 1.0",
            "CC BY-NC-SA 4.0",
        ),
    }
    for relative, phrases in readme_requirements.items():
        content = read(relative, errors)
        for phrase in phrases:
            if phrase not in content:
                errors.append(f"{relative} lost public contract phrase: {phrase!r}")

    for english, chinese in PUBLIC_DOC_PAIRS.items():
        if not (ROOT / english).is_file() or not (ROOT / chinese).is_file():
            errors.append(f"localized documentation pair is incomplete: {english} / {chinese}")

    root_license = ROOT / "LICENSE"
    skill_license = SKILL_DIR / "LICENSE.txt"
    if root_license.is_file() and file_sha256(root_license) != SUL_SHA256:
        errors.append("root LICENSE is not the exact pinned SUL-1.0 text")
    if skill_license.is_file() and file_sha256(skill_license) != SUL_SHA256:
        errors.append("Skill LICENSE.txt is not the exact pinned SUL-1.0 text")
    if root_license.is_file() and skill_license.is_file():
        if root_license.read_bytes() != skill_license.read_bytes():
            errors.append("root and Skill SUL-1.0 license texts differ")

    documentation_license = read("LICENSE-DOCUMENTATION.md", errors)
    for phrase in (
        "Creative Commons Attribution-NonCommercial-ShareAlike 4.0",
        "https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode.en",
        "This notice does not apply the Creative Commons license to the Skill",
    ):
        if phrase not in documentation_license:
            errors.append(f"LICENSE-DOCUMENTATION.md lost scope phrase: {phrase!r}")

    licensing = read("LICENSING.md", errors)
    licensing_lower = licensing.lower()
    for phrase in (
        "source-available, not OSI open source",
        "skills/repository-operational-truth-audit/**",
        "README.md` and `README.zh-CN.md",
        "docs/**",
        "No external Skill text",
    ):
        if phrase.lower() not in licensing_lower:
            errors.append(f"LICENSING.md lost path or provenance phrase: {phrase!r}")

    stale_publication_phrases = (
        "no public license",
        "no remote release",
        "publication: not authorized",
        "publication acceptance is not part of the current authorization",
    )
    for path in (
        ROOT / "README.md",
        ROOT / "README.zh-CN.md",
        ROOT / "AGENTS.md",
        ROOT / "docs" / "product-spec.md",
        ROOT / "docs" / "current-state.md",
        ROOT / "docs" / "current-state.zh-CN.md",
    ):
        if not path.is_file():
            continue
        content = path.read_text(encoding="utf-8").lower()
        for phrase in stale_publication_phrases:
            if phrase in content:
                errors.append(f"{path.relative_to(ROOT)} retains stale phrase: {phrase!r}")

    skill = read(f"skills/{SKILL_NAME}/SKILL.md", errors)
    match = re.match(r"^---\n(.*?)\n---\n", skill, re.DOTALL)
    if not match:
        errors.append("SKILL.md has invalid frontmatter boundaries")
    else:
        frontmatter = match.group(1)
        name_match = re.search(r"^name:\s*([a-z0-9-]+)\s*$", frontmatter, re.MULTILINE)
        description_match = re.search(
            r'^description:\s*"([^"]+)"\s*$', frontmatter, re.MULTILINE
        )
        if not name_match or name_match.group(1) != SKILL_NAME:
            errors.append(f"SKILL.md name must be {SKILL_NAME}")
        if not description_match:
            errors.append("SKILL.md must have one quoted description")
        else:
            description = description_match.group(1)
            for phrase in (
                "re-entry",
                "migration",
                "current operational truth",
                "Do not use for code review",
                "generic repo hygiene",
            ):
                if phrase not in description:
                    errors.append(f"SKILL.md description lost routing phrase: {phrase!r}")

    if len(skill.splitlines()) > 360:
        errors.append("SKILL.md exceeds the 360-line context budget")
    if len(skill.split()) > 3600:
        errors.append("SKILL.md exceeds the 3600-word context budget")

    agent_yaml = read(f"skills/{SKILL_NAME}/agents/openai.yaml", errors)
    for phrase in (
        'display_name: "Repository Operational Truth Audit"',
        f"${SKILL_NAME}",
        "allow_implicit_invocation: true",
    ):
        if phrase not in agent_yaml:
            errors.append(f"agents/openai.yaml lost required value: {phrase!r}")

    cases_root = ROOT / "evals" / "cases"
    actual_cases = {path.name for path in cases_root.iterdir() if path.is_dir()} if cases_root.is_dir() else set()
    if actual_cases != EXPECTED_CASES:
        errors.append(
            "eval case set differs: "
            f"expected={sorted(EXPECTED_CASES)} actual={sorted(actual_cases)}"
        )
    for case_id in sorted(EXPECTED_CASES):
        case_root = cases_root / case_id
        for relative in ("case.json", "prompt.md", "expected/AUDIT.md"):
            if not (case_root / relative).is_file():
                errors.append(f"{case_id} missing {relative}")
        if not (case_root / "fixture").is_dir():
            errors.append(f"{case_id} missing fixture directory")
        case_path = case_root / "case.json"
        if case_path.is_file():
            try:
                payload = json.loads(case_path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, UnicodeDecodeError) as exc:
                errors.append(f"{case_id} case.json is invalid: {exc}")
            else:
                if payload.get("case_id") != case_id:
                    errors.append(f"{case_id} case_id field does not match directory")
                if payload.get("sandbox") != "workspace-write":
                    errors.append(f"{case_id} must use workspace-write for its report artifact")
                changed = [
                    assertion.get("paths")
                    for assertion in payload.get("assertions", [])
                    if assertion.get("type") == "changed_files_exact"
                ]
                if changed != [["AUDIT.md"]]:
                    errors.append(f"{case_id} must permit only AUDIT.md as target output")

    activation_path = ROOT / "evals" / "activation-prompts.csv"
    if activation_path.is_file():
        with activation_path.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        positives = sum(row.get("expected") == "activate" for row in rows)
        negatives = sum(row.get("expected") == "do-not-activate" for row in rows)
        if positives < 4 or negatives < 5:
            errors.append("activation prompts need at least 4 positive and 5 negative controls")

    workflow = read(".github/workflows/validate.yml", errors)
    for command in (
        "python3 scripts/validate_architecture.py",
        "python3 scripts/validate_repository.py",
        "python3 -m unittest discover -s tests -p 'test_*.py'",
        "python3 scripts/selftest.py",
    ):
        if command not in workflow:
            errors.append(f"CI workflow does not run required command: {command}")

    forbidden_patterns = {
        "/" + "Users/": "local user path",
        "/home/" + "faye/": "local user path",
        "BEGIN " + "OPENSSH PRIVATE KEY": "private key material",
        "ghp" + "_": "GitHub-token-like material",
    }
    for path in text_files():
        relative = path.relative_to(ROOT).as_posix()
        content = path.read_text(encoding="utf-8")
        for pattern, label in forbidden_patterns.items():
            if pattern in content:
                errors.append(f"{relative} contains forbidden {label}: {pattern!r}")

    validate_markdown_links(errors)

    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("Repository Operational Truth Audit validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("Repository, Skill, docs, eval contracts, and publication boundaries: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
