#!/usr/bin/env python3
"""Shared deterministic helpers for repository validation and installation."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SKILL_NAME = "repository-operational-truth-audit"
SKILL_DIR = ROOT / "skills" / SKILL_NAME
RECEIPT_NAME = f".{SKILL_NAME}-install.json"


def read_version(root: Path = ROOT) -> str:
    return (root / "VERSION").read_text(encoding="utf-8").strip()


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def directory_digest(path: Path) -> str:
    """Hash relative paths, executable bits, and bytes; reject symlinks."""

    if not path.is_dir():
        raise ValueError(f"not a directory: {path}")

    digest = hashlib.sha256()
    files = sorted(
        (item for item in path.rglob("*") if item.is_file() or item.is_symlink()),
        key=lambda item: item.relative_to(path).as_posix(),
    )
    for item in files:
        relative = item.relative_to(path).as_posix()
        if item.is_symlink():
            raise ValueError(f"skill payload must not contain symlinks: {relative}")
        mode = stat.S_IMODE(item.stat().st_mode) & 0o111
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(str(mode).encode("ascii"))
        digest.update(b"\0")
        digest.update(item.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def git_identity(root: Path = ROOT) -> dict[str, Any]:
    def run(*args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", "-C", str(root), *args],
            check=False,
            capture_output=True,
            text=True,
        )

    head_result = run("rev-parse", "HEAD")
    if head_result.returncode != 0:
        return {"commit": None, "dirty": None}

    status_result = run("status", "--porcelain=v1", "--untracked-files=all")
    if status_result.returncode != 0:
        return {"commit": head_result.stdout.strip(), "dirty": None}
    return {
        "commit": head_result.stdout.strip(),
        "dirty": bool(status_result.stdout.strip()),
    }


def atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    temporary = path.with_name(f".{path.name}.tmp-{os.getpid()}")
    temporary.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)
