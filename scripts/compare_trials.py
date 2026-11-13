#!/usr/bin/env python3
"""Compare matched engineering trials without imputing costs or scoring repos.

This is an offline evaluator, never a Skill runtime dependency or model launcher.
Receipts are observations with provenance, not authenticated proof. Referenced
evidence is not executed. Unknown human effort is never converted to zero.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
import math
from pathlib import Path
import sys
from typing import Any

MATCH_FIELDS = (
    "task_id", "subject_digest", "task_prompt_digest", "harness", "model",
    "settings_id", "environment_id", "replicate",
)
METRICS = {
    "tool_calls": "count",
    "exec_commands": "count",
    "elapsed_seconds": "seconds",
    "input_tokens": "count",
    "output_tokens": "count",
    "human_active_seconds": "seconds",
    "review_seconds": "seconds",
    "human_interventions": "count",
    "false_attributions": "count",
    "unnecessary_changes": "count",
    "unauthorized_mutations": "count",
    "resume_rework_seconds": "seconds",
}
STATUSES = {"success", "failure", "blocked", "unjudged"}
METHODS = {"deterministic-consumer", "independent-review", "self-report", "not-run"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_trial(trial: Any) -> None:
    require(isinstance(trial, dict), "each trial must be an object")
    name = trial.get("run_id", "<missing>")
    require(trial.get("schema_version") == 1, f"{name}: schema_version must be 1")
    for key in ("run_id", "block_id", "arm", *MATCH_FIELDS):
        require(nonempty(trial.get(key)), f"{name}: {key} must be a nonempty string")
    skill = trial.get("skill")
    require(isinstance(skill, dict), f"{name}: skill exposure is required")
    exposure = skill.get("exposure")
    require(exposure in {"loaded", "available-unread", "none", "unknown"},
            f"{name}: invalid skill exposure")
    if exposure in {"loaded", "available-unread"}:
        require(nonempty(skill.get("digest")), f"{name}: exposed Skill needs a digest")
    outcome = trial.get("outcome")
    require(isinstance(outcome, dict), f"{name}: outcome is required")
    require(outcome.get("status") in STATUSES, f"{name}: invalid outcome status")
    require(outcome.get("method") in METHODS, f"{name}: invalid outcome method")
    evidence = outcome.get("evidence", [])
    require(isinstance(evidence, list) and all(nonempty(v) for v in evidence),
            f"{name}: outcome evidence must be a list of locators")
    if outcome["status"] in {"success", "failure"}:
        require(outcome["method"] != "not-run" and bool(evidence),
                f"{name}: a judged result needs a method and evidence")
    measurements = trial.get("measurements", {})
    require(isinstance(measurements, dict), f"{name}: measurements must be an object")
    for metric, item in measurements.items():
        require(metric in METRICS, f"{name}: unknown metric {metric}")
        require(isinstance(item, dict), f"{name}: {metric} must have provenance")
        state = item.get("status")
        require(state in {"observed", "proxy", "unavailable"},
                f"{name}: {metric} has invalid measurement status")
        require(nonempty(item.get("source")), f"{name}: {metric} needs a source/reason")
        value = item.get("value")
        if state == "unavailable":
            require(value is None, f"{name}: unavailable {metric} must be null")
        else:
            require(type(value) in (int, float) and math.isfinite(value) and value >= 0,
                    f"{name}: {metric} must be a finite nonnegative number")
            if METRICS[metric] == "count":
                require(value == int(value), f"{name}: {metric} must be an integer count")


def measurement(trial: dict, metric: str) -> dict:
    return trial.get("measurements", {}).get(metric, {
        "status": "unavailable", "value": None, "source": "not recorded",
    })


def compare(trials: list[dict], baseline: str = "without-skill",
            candidate: str = "candidate") -> dict:
    require(baseline != candidate, "baseline and candidate arms must differ")
    require(isinstance(trials, list), "trials must be an array")
    seen: set[str] = set()
    blocks: dict[str, dict[str, dict]] = {}
    for trial in trials:
        validate_trial(trial)
        require(trial["run_id"] not in seen, f"duplicate run_id: {trial['run_id']}")
        seen.add(trial["run_id"])
        require(trial["arm"] in {baseline, candidate},
                f"unselected arm: {trial['arm']}; select or separate comparisons")
        block = blocks.setdefault(trial["block_id"], {})
        require(trial["arm"] not in block,
                f"duplicate arm in block {trial['block_id']}: {trial['arm']}")
        block[trial["arm"]] = trial

    pairs = []
    totals = {arm: Counter(t["outcome"]["status"] for t in trials if t["arm"] == arm)
              for arm in (baseline, candidate)}
    for block_id, arms in sorted(blocks.items()):
        left, right = arms.get(baseline), arms.get(candidate)
        reasons = []
        if left is None or right is None:
            reasons.append("missing arm")
        else:
            reasons.extend(f"mismatched {key}" for key in MATCH_FIELDS
                           if left[key] != right[key])
            # Record intention-to-treat observations, but never call unread
            # treatment an effect of actually using this Skill.
            if right["skill"]["exposure"] != "loaded":
                reasons.append("candidate Skill was not observed loaded")
            if left["skill"]["exposure"] == "unknown":
                reasons.append("baseline Skill exposure is unknown")
            if any(t["outcome"]["method"] in {"self-report", "not-run"}
                   for t in (left, right)):
                reasons.append("independent outcome missing")
            if any(t["outcome"]["status"] in {"blocked", "unjudged"}
                   for t in (left, right)):
                reasons.append("task outcome unresolved")
            if left["outcome"]["method"] != right["outcome"]["method"]:
                reasons.append("mismatched outcome method")
        row = {
            "block_id": block_id,
            "baseline_run": left["run_id"] if left else None,
            "candidate_run": right["run_id"] if right else None,
            "comparable": not reasons, "reasons": reasons,
            "outcomes": {arm: t["outcome"] for arm, t in arms.items()},
            "measurements": {},
        }
        for metric in METRICS:
            a = measurement(left, metric) if left else None
            b = measurement(right, metric) if right else None
            observed = (not reasons and a and b and
                        a["status"] == b["status"] == "observed")
            row["measurements"][metric] = {
                "unit": METRICS[metric], "baseline": a, "candidate": b,
                "candidate_minus_baseline": b["value"] - a["value"] if observed else None,
            }
        pairs.append(row)
    return {
        "schema_version": 1, "arms": {"baseline": baseline, "candidate": candidate},
        "trial_count": len(trials), "block_count": len(blocks),
        "comparable_blocks": sum(p["comparable"] for p in pairs),
        "outcome_counts": {arm: {status: counts[status] for status in sorted(STATUSES)}
                           for arm, counts in totals.items()},
        "pairs": pairs,
        "interpretation": (
            "Descriptive paired observations, not a causal estimate or repository score. "
            "Failed, blocked and unjudged runs remain in denominators. Missing effort is "
            "not zero; proxies are retained but not subtracted as measured human time. "
            "Receipts record provenance; this tool does not authenticate their claims."
        ),
    }


def render(report: dict) -> str:
    clean = lambda v: str(v).replace("|", "\\|").replace("\n", " ").replace("\r", " ")
    lines = ["# Matched engineering trials", "",
             f"Trials: {report['trial_count']}; blocks: {report['block_count']}; "
             f"comparable: {report['comparable_blocks']}.", "",
             "| Block | Comparison | Outcomes |", "| --- | --- | --- |"]
    for pair in report["pairs"]:
        outcomes = "; ".join(f"{arm}: {outcome['status']}" for arm, outcome in pair["outcomes"].items())
        reason = "matched" if pair["comparable"] else "; ".join(pair["reasons"])
        # A receipt is data. Keep Markdown rendering literal enough that values
        # cannot manufacture additional table rows or headings.
        lines.append(f"| {clean(pair['block_id'])} | {clean(reason)} | {clean(outcomes)} |")
    for pair in report["pairs"]:
        lines.extend(["", f"## {clean(pair['block_id'])}", ""])
        for metric, item in pair["measurements"].items():
            a, b = item["baseline"], item["candidate"]
            if a and b and a["status"] == b["status"] == "unavailable":
                continue
            describe = lambda v: "missing arm" if v is None else f"{v['status']} {v['value']}"
            delta = item["candidate_minus_baseline"]
            lines.append(f"- {metric}: {describe(a)} → {describe(b)}; measured delta: {delta}.")
    lines.extend(["", report["interpretation"], ""])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("receipt", type=Path, help="JSON array or an object with trials")
    parser.add_argument("--baseline", default="without-skill")
    parser.add_argument("--candidate", default="candidate")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        payload = json.loads(args.receipt.read_text(encoding="utf-8"))
        trials = payload.get("trials") if isinstance(payload, dict) else payload
        report = compare(trials, args.baseline, args.candidate)
    except (OSError, ValueError, TypeError) as exc:
        print(f"Trial comparison failed: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(report, ensure_ascii=False, indent=2) if args.json else render(report), end="\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
