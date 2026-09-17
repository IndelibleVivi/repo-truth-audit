#!/usr/bin/env python3
"""Shared deterministic helpers for repository validation and installation."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import stat
import subprocess
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
SKILL_NAME = "repository-operational-truth-audit"
SKILL_DIR = ROOT / "skills" / SKILL_NAME
RECEIPT_NAME = f".{SKILL_NAME}-install.json"

#: Exact declared payload of the installable Skill, as normalized POSIX
#: relative paths below ``SKILL_DIR``. This is the single source of truth for
#: source hashing, staging/copying, installed comparison, and receipt identity.
#: Everything else below the Skill directory is either runtime residue or an
#: undeclared entry that the source contract rejects.
SKILL_PAYLOAD_FILES: tuple[str, ...] = (
    "LICENSE.txt",
    "NOTICE.md",
    "SKILL.md",
    "agents/openai.yaml",
    "references/audit.md",
    "references/operation.md",
    "references/recovery.md",
    "scripts/check_evidence.py",
)

#: Interpreter and OS residue that local tooling can leave inside a Skill tree.
#: It is ignored by the payload contract instead of counting as content.
RUNTIME_RESIDUE_DIR_NAMES = frozenset({"__pycache__"})
RUNTIME_RESIDUE_FILE_SUFFIXES = frozenset({".pyc", ".pyo"})
RUNTIME_RESIDUE_FILE_NAMES = frozenset({".DS_Store"})


def is_runtime_residue(relative: PurePosixPath) -> bool:
    """True for local runtime residue that is not declared Skill payload."""

    if any(part in RUNTIME_RESIDUE_DIR_NAMES for part in relative.parts):
        return True
    if relative.name in RUNTIME_RESIDUE_FILE_NAMES:
        return True
    return relative.suffix in RUNTIME_RESIDUE_FILE_SUFFIXES


def _resolve_payload_file(root: Path, relative: str) -> Path:
    """Resolve one declared payload file, rejecting symlinked path components."""

    current = root
    for part in PurePosixPath(relative).parts:
        current = current / part
        if current.is_symlink():
            raise ValueError(f"skill payload must not contain symlinks: {relative}")
    if not current.is_file():
        raise ValueError(f"skill payload file is missing: {relative}")
    return current


def read_version(root: Path = ROOT) -> str:
    return (root / "VERSION").read_text(encoding="utf-8").strip()


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def directory_digest(path: Path, files: Iterable[str]) -> str:
    """Hash exactly ``files`` below ``path``: relative path, exec bits, bytes.

    Callers pass the explicit payload file list, so nothing else below ``path``
    is read and runtime residue such as ``__pycache__`` cannot change the
    digest. Declared files that are missing or symlinked are rejected.
    """

    if not path.is_dir():
        raise ValueError(f"not a directory: {path}")

    digest = hashlib.sha256()
    for relative in sorted(files):
        item = _resolve_payload_file(path, relative)
        mode = stat.S_IMODE(item.stat().st_mode) & 0o111
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(str(mode).encode("ascii"))
        digest.update(b"\0")
        digest.update(item.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def undeclared_payload_entries(
    root: Path, files: Iterable[str] = SKILL_PAYLOAD_FILES
) -> list[str]:
    """Return files below ``root`` that the payload contract does not declare.

    Runtime residue is skipped. Directories are summarized by the undeclared
    files they contain; symlinks are reported directly because the payload
    contract never follows them.
    """

    declared = set(files)
    undeclared: list[str] = []
    for item in root.rglob("*"):
        relative = PurePosixPath(item.relative_to(root).as_posix())
        if is_runtime_residue(relative):
            continue
        if item.is_symlink():
            if relative.as_posix() not in declared:
                undeclared.append(relative.as_posix())
            continue
        if item.is_dir():
            continue
        if relative.as_posix() not in declared:
            undeclared.append(relative.as_posix())
    return sorted(undeclared)


def payload_matches(
    source: Path, target: Path, files: Iterable[str] = SKILL_PAYLOAD_FILES
) -> bool:
    """True when ``target`` holds exactly the declared payload of ``source``.

    Runtime residue in ``target`` is ignored. Extra, missing, or symlinked
    declared files make the trees differ instead of matching a partial payload.
    """

    file_list = tuple(files)
    if not target.is_dir():
        return False
    if undeclared_payload_entries(target, file_list):
        return False
    try:
        return directory_digest(target, file_list) == directory_digest(source, file_list)
    except (OSError, ValueError):
        return False


def copy_payload(
    source: Path, target: Path, files: Iterable[str] = SKILL_PAYLOAD_FILES
) -> None:
    """Copy exactly the declared payload files from ``source`` into ``target``."""

    target.mkdir(parents=True, exist_ok=True)
    for relative in sorted(files):
        origin = _resolve_payload_file(source, relative)
        destination = target / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(origin, destination)


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
