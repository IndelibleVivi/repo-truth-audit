#!/usr/bin/env python3
"""Prepare one frozen consumer-first subject; never call a model or grade output."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
TASKS = ("migration-recovery", "delivery-adoption", "known-bug", "clean-baseline")
ARMS = ("without-skill", "progressive-rta", "consumer-first")
SEED = "consumer-first-2026-11-14-v1"
PROGRESSIVE_DIGEST = "28b73009402e0f149c7078379a15d51cf88468c66ec092f49a59a5f6926fb211"
RESUME_OWNER = (
    "Unrelated pre-existing uncommitted owner content.\n"
    "Later owner edit: keep the French launch wording pending review.\n"
)
RESUME_CHECKPOINT = (
    "# Previous operation checkpoint\n\n"
    "Formatting extraction was applied and source output checks passed.\n"
    "A previous progress label says complete, but it records no rebuilt\n"
    "artifact observation or proof that the remaining owner moved.\n"
    "The live request remains the finite architecture in TASK.md.\n"
    "The owner appended notes after the checkpoint; preserve them.\n"
)

def digest_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()

def content_digest(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*")):
        if path.is_file() and ".git" not in path.relative_to(root).parts:
            digest.update(path.relative_to(root).as_posix().encode() + b"\0")
            digest.update(digest_bytes(path.read_bytes()).encode("ascii") + b"\0")
    return digest.hexdigest()

def module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded

def prompt(task: str, language: str) -> str:
    return (HERE / "tasks" / language / f"{task}.md").read_text(encoding="utf-8")

def slot_order(seed: str = SEED) -> list[dict]:
    rows = []
    for task in TASKS:
        for arm in ARMS:
            key = digest_bytes(f"{seed}\0{task}\0{arm}".encode("utf-8"))
            rows.append({"slot": None, "task_id": task, "arm": arm, "order_key": key})
    rows.sort(key=lambda row: row["order_key"])
    for index, row in enumerate(rows, 1):
        row["slot"] = index
    return rows

def preregistration(seed: str = SEED) -> dict:
    sys.path.insert(0, str(ROOT / "scripts"))
    from common import SKILL_DIR, SKILL_PAYLOAD_FILES, directory_digest
    payload = directory_digest(SKILL_DIR, SKILL_PAYLOAD_FILES)
    if payload != PROGRESSIVE_DIGEST:
        raise ValueError(f"progressive treatment snapshot moved: {payload}")
    instructions = {
        arm: digest_bytes((HERE / "instructions" / f"{arm}.md").read_bytes())
        for arm in ("progressive-rta", "consumer-first")
    }
    prompts = {task: digest_bytes(prompt(task, "en").encode("utf-8")) for task in TASKS}
    return {
        "schema": "rta-consumer-first-preregistration/1",
        "status": "frozen-not-run",
        "question": "consumer-first instruction versus current progressive RTA and no-Skill controls",
        "order_seed": seed,
        "arms": list(ARMS),
        "task_ids": list(TASKS),
        "replicate_count": 1,
        "maximum_fresh_sessions": 12,
        "invocation_unit": "fresh Agent subject session, not individual model API requests",
        "maximum_target_model_invocations": 12,
        "target_model_invocations_observed_now": 0,
        "frozen_before_target_calls": True,
        "absolute_slot_limit": 12,
        "further_replication": "requires a new preregistration, seed, budget and result-blind-integrity declaration",
        "protocol": {
            "replicates": 1,
            "paired_arms": [
                ["without-skill", "progressive-rta"],
                ["without-skill", "consumer-first"],
                ["progressive-rta", "consumer-first"],
            ],
            "languages": ["en", "zh-CN"],
            "language_matching": "one language consistently within each matched block",
            "outcomes": ["success", "failure", "blocked", "unjudged"],
            "result_recording": "retain failures, setup blocks, unread treatment, and missing metrics",
            "further_replication_forbidden_without_new_preregistration": True,
            "human_review": "voluntary, anonymous, stopwatch active time, separate from agent elapsed time",
            "reviewer_contact": "not authorized",
            "maximum_target_model_calls_for_coordinator": 12,
        },
        "progressive_payload": {
            "digest": payload,
            "files": list(SKILL_PAYLOAD_FILES),
        },
        "instructions": instructions,
        "task_prompt_digests_en": prompts,
        "task_prompt_digests_zh-CN": {
            task: digest_bytes(prompt(task, "zh-CN").encode("utf-8")) for task in TASKS
        },
        "slots": slot_order(seed),
    }

def overlaps(candidate: Path, protected: Path) -> bool:
    """Reject lexical equality/nesting and resolved equality/nesting."""
    lexical = candidate.absolute()
    other = protected.absolute()
    if lexical == other or lexical.is_relative_to(other) or other.is_relative_to(lexical):
        return True
    resolved = candidate.resolve(strict=False)
    target = protected.resolve()
    return resolved == target or resolved.is_relative_to(target) or target.is_relative_to(resolved)

def protected_paths(task: str) -> list[Path]:
    return [HERE, ROOT / "skills" / "repository-operational-truth-audit",
            ROOT / "evals" / "intent-lab", ROOT / "evals" / "operation-lab"]

def prepare(task: str, destination: Path, language: str = "en") -> dict:
    if task not in TASKS:
        raise ValueError(f"unknown task: {task}")
    if language not in {"en", "zh-CN"}:
        raise ValueError(f"unknown prompt language: {language}")
    if destination.exists():
        raise ValueError("destination must not exist")
    for protected in protected_paths(task):
        if overlaps(destination, protected):
            raise ValueError(f"destination overlaps protected path: {protected}")
    task_prompt = prompt(task, language)
    if task == "migration-recovery":
        fixture = module("consumer_resume_fixture", ROOT / "evals/operation-lab/run_operation_lab.py")
        fixture.seed(destination)
        fixture.apply_known_cut(destination, fixture.CUT_ONE, fixture.snapshot(destination))
        (destination / "CHECKPOINT.md").write_text(RESUME_CHECKPOINT, encoding="utf-8")
        (destination / "owner-notes.txt").write_text(RESUME_OWNER, encoding="utf-8")
        (destination / "README.md").write_text(
            "# Local receipt CLI\n\n"
            "Run `python3 entry.py --input records.json --state ledger.txt --format json`.\n"
            "Text format is also supported. `delivery.json` selects a module and\n"
            "`bundle.json` lists files distributed to recipients. Each valid nonempty\n"
            "batch appends `count:sum` to the existing ledger once.\n", encoding="utf-8")
    elif task == "delivery-adoption":
        intent = module("consumer_cedar_fixture", ROOT / "evals/intent-lab/prepare_intent_subject.py")
        intent.prepare("task-export-handoff", destination, operate=True)
    elif task == "known-bug":
        subjects = module("consumer_subjects", HERE / "subjects.py")
        subjects.write_files(destination, subjects.KNOWN_BUG_FILES)
    else:
        subjects = module("consumer_subjects", HERE / "subjects.py")
        subjects.write_files(destination, subjects.CLEAN_FILES)
    (destination / "TASK.md").write_text(task_prompt, encoding="utf-8")
    initial_files = sorted(
        path.relative_to(destination).as_posix()
        for path in destination.rglob("*") if path.is_file()
    )
    protected_inputs = {
        "migration-recovery": ["TASK.md", "owner-notes.txt", "CHECKPOINT.md", "entry.py"],
        "delivery-adoption": ["TASK.md", "PROGRAM.md", "store.json",
                              "supplied-worksheet.json", "docs/current-use.md"],
        "known-bug": ["TASK.md"],
        "clean-baseline": list(initial_files),
    }[task]
    return {
        "schema": "rta-consumer-first-preparation/1",
        "task_id": task,
        "language": language,
        "subject_digest": content_digest(destination),
        "task_prompt_digest": digest_bytes(task_prompt.encode("utf-8")),
        "initial_files": initial_files,
        "protected_inputs": sorted(set(protected_inputs)),
        "target_model_invocations": 0,
    }

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("task", nargs="?", choices=TASKS)
    parser.add_argument("destination", type=Path, nargs="?")
    parser.add_argument("--language", choices=("en", "zh-CN"), default="en")
    parser.add_argument("--preregistration", action="store_true",
                        help="print the frozen seed, slots, and treatment identities")
    parser.add_argument("--write-preregistration", action="store_true",
                        help="write the preregistration payload from the same function")
    args = parser.parse_args()
    try:
        if args.write_preregistration:
            path = HERE / "preregistration.json"
            if path.exists():
                raise ValueError("preregistration.json already exists; review before replacing")
            payload = preregistration()
            path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                            encoding="utf-8")
            result = payload
        elif args.preregistration:
            result = preregistration()
        else:
            if args.task is None or args.destination is None:
                parser.error("task and destination are required unless --preregistration is used")
            result = prepare(args.task, args.destination, args.language)
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        print(f"preparation failed: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
