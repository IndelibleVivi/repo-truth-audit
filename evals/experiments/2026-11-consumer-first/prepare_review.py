#!/usr/bin/env python3
"""Create an anonymized review packet without soliciting or timing reviewers."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

TASKS = ("migration-recovery", "delivery-adoption", "known-bug", "clean-baseline")
ARMS = ("without-skill", "progressive-rta", "consumer-first")
PRIVATE_IDENTIFIERS = re.compile(
    r"\b(?:\w+[-_.])?progressive(?:-rta)?\b|\b(?:repo-)?consumer-first-?instruction\b|"
    r"\bconsumer-first\b|\bwithout-skill\b|"
    r"\brepository-operational-truth-audit\b", re.IGNORECASE)

def digest(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()

def packet(task: str, arm: str, result: str, result_identity: str) -> dict:
    opaque = "review-" + digest(f"{task}\0{result_identity}")[:16]
    visible = PRIVATE_IDENTIFIERS.sub("[treatment]", result)
    return {
        "schema": "rta-review-packet/1",
        "status": "prepared-not-reviewed",
        "review_id": opaque,
        "task_material": {
            "task_file": f"tasks/en/{task}.md",
            "prompt_sha256": digest((Path(__file__).parent / "tasks/en" / f"{task}.md")
                                    .read_text(encoding="utf-8")),
        },
        "candidate_result": visible,
        "candidate_result_sha256": digest(visible),
        "review_instruction": (
            "Judge only the visible result against the task. You may use a stopwatch "
            "you operate; report active review seconds once. Do not infer time from text."
        ),
        "timing": {
            "status": "unavailable",
            "human_active_seconds": None,
            "agent_elapsed_seconds": None,
            "source": "No voluntary reviewer timing was supplied.",
        },
        "privacy": {
            "planted_arm_label": arm,
            "arm_label_hidden_in_candidate_result": True,
            "note": "The two mapping fields are excluded before giving the candidate packet to a reviewer.",
        },
    }

def public_packet(payload: dict) -> dict:
    """Return only material intended for a reviewer; keep arm mapping private."""
    return {
        "schema": payload["schema"],
        "status": payload["status"],
        "review_id": payload["review_id"],
        "task_material": payload["task_material"],
        "candidate_result": payload["candidate_result"],
        "candidate_result_sha256": payload["candidate_result_sha256"],
        "review_instruction": payload["review_instruction"],
        "timing": payload["timing"],
    }

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--subject", required=True, choices=TASKS)
    parser.add_argument("--arm", required=True, choices=ARMS)
    parser.add_argument("--result", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    try:
        if args.output.exists():
            raise ValueError("output must not exist")
        text = args.result.read_text(encoding="utf-8")
        payload = packet(args.subject, args.arm, text, hashlib.sha256(text.encode()).hexdigest())
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("x", encoding="utf-8") as handle:
            json.dump(public_packet(payload), handle, ensure_ascii=False, indent=2)
            handle.write("\n")
    except (OSError, ValueError) as exc:
        print(f"review packet preparation failed: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(public_packet(payload), ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
