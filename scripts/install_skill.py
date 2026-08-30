#!/usr/bin/env python3
"""Transactionally install the standalone Skill into a user Skill root."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import os
from pathlib import Path
import shutil
import sys
import tempfile
from typing import Any

from common import (
    RECEIPT_NAME,
    ROOT,
    SKILL_DIR,
    SKILL_NAME,
    atomic_write_json,
    directory_digest,
    git_identity,
    read_version,
)
from validate_repository import validate


def default_destination() -> Path:
    codex_home = os.environ.get("CODEX_HOME")
    if codex_home:
        return Path(codex_home).expanduser().resolve() / "skills"
    return Path.home() / ".codex" / "skills"


def install(destination: Path, *, replace: bool = False) -> dict[str, Any]:
    errors = validate()
    if errors:
        raise RuntimeError("source validation failed:\n- " + "\n- ".join(errors))

    destination = destination.expanduser().resolve()
    destination.mkdir(parents=True, exist_ok=True)
    target = destination / SKILL_NAME
    source_digest = directory_digest(SKILL_DIR)

    if target.exists() and not target.is_dir():
        raise RuntimeError(f"install target exists and is not a directory: {target}")
    if target.is_dir() and directory_digest(target) == source_digest:
        return {
            "status": "unchanged",
            "target": str(target),
            "installed_skill_digest": source_digest,
        }
    if target.exists() and not replace:
        raise RuntimeError(
            f"install target already exists with different content: {target}; "
            "rerun with --replace for an explicit transactional upgrade"
        )

    staging_root = Path(
        tempfile.mkdtemp(prefix=f".{SKILL_NAME}.staging-", dir=destination)
    )
    staged_skill = staging_root / SKILL_NAME
    backup: Path | None = None
    installed = False
    try:
        shutil.copytree(SKILL_DIR, staged_skill)
        staged_digest = directory_digest(staged_skill)
        if staged_digest != source_digest:
            raise RuntimeError("staged Skill digest does not match canonical source")

        if target.exists():
            stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
            backup_root = destination / f".{SKILL_NAME}.backups"
            backup_root.mkdir(parents=True, exist_ok=True)
            backup = backup_root / stamp
            os.replace(target, backup)

        os.replace(staged_skill, target)
        installed = True
        installed_digest = directory_digest(target)
        if installed_digest != source_digest:
            raise RuntimeError("installed Skill digest does not match canonical source")

        source_git = git_identity(ROOT)
        receipt = {
            "schema_version": 1,
            "skill": SKILL_NAME,
            "version": read_version(ROOT),
            "status": "installed",
            "installed_at": datetime.now(timezone.utc).isoformat(),
            "target": str(target),
            "backup": str(backup) if backup else None,
            "source_git_commit": source_git["commit"],
            "source_git_dirty": source_git["dirty"],
            "source_skill_digest": source_digest,
            "installed_skill_digest": installed_digest,
        }
        atomic_write_json(destination / RECEIPT_NAME, receipt)
        return receipt
    except Exception:
        if installed and target.exists():
            shutil.rmtree(target)
        if backup is not None and backup.exists() and not target.exists():
            os.replace(backup, target)
        raise
    finally:
        if staging_root.exists():
            shutil.rmtree(staging_root)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dest",
        type=Path,
        default=default_destination(),
        help="Skill root; defaults to $CODEX_HOME/skills or ~/.codex/skills",
    )
    parser.add_argument(
        "--replace",
        action="store_true",
        help="Explicitly replace a different installed copy after preserving a backup",
    )
    args = parser.parse_args()
    try:
        receipt = install(args.dest, replace=args.replace)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(f"Status: {receipt['status']}")
    print(f"Target: {receipt['target']}")
    print(f"Installed digest: {receipt['installed_skill_digest']}")
    if receipt.get("source_git_commit"):
        print(f"Source commit: {receipt['source_git_commit']}")
        print(f"Source dirty: {receipt['source_git_dirty']}")
    if receipt.get("backup"):
        print(f"Backup: {receipt['backup']}")
    if receipt["status"] == "installed":
        print(f"Receipt: {Path(args.dest).expanduser().resolve() / RECEIPT_NAME}")
    print("Next-turn Codex discovery is a separate acceptance boundary.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
