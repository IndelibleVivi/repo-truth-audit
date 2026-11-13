from copy import deepcopy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from compare_trials import compare


def trial(arm):
    return {
        "schema_version": 1, "run_id": arm, "block_id": "task-1-r1", "arm": arm,
        "task_id": "task-1", "subject_digest": "same-input", "task_prompt_digest": "same-task",
        "harness": "native", "model": "recorded-model", "settings_id": "same-settings",
        "environment_id": "same-dependencies", "replicate": "1",
        "skill": {"exposure": "none"} if arm == "without-skill" else
                 {"exposure": "loaded", "digest": "candidate-bytes"},
        "outcome": {"status": "success", "method": "deterministic-consumer", "evidence": ["check.json"]},
        "measurements": {},
    }


class TrialComparisonTests(unittest.TestCase):
    def setUp(self):
        self.a, self.b = trial("without-skill"), trial("candidate")

    def test_unknown_human_time_is_not_zero_and_observed_cost_is_paired(self):
        self.a["measurements"]["tool_calls"] = {"status": "observed", "value": 5, "source": "host trace"}
        self.b["measurements"]["tool_calls"] = {"status": "observed", "value": 8, "source": "host trace"}
        result = compare([self.a, self.b])["pairs"][0]["measurements"]
        self.assertEqual(result["tool_calls"]["candidate_minus_baseline"], 3)
        self.assertIsNone(result["review_seconds"]["candidate_minus_baseline"])
        self.assertIsNone(result["review_seconds"]["baseline"]["value"])

    def test_proxy_does_not_become_human_effort_measurement(self):
        for t in (self.a, self.b):
            t["measurements"]["review_seconds"] = {"status": "proxy", "value": 20, "source": "estimated from words"}
        self.assertIsNone(compare([self.a, self.b])["pairs"][0]["measurements"]["review_seconds"]["candidate_minus_baseline"])

    def test_failed_and_blocked_runs_are_retained(self):
        self.a["outcome"]["status"] = "failure"
        self.b["outcome"] = {"status": "blocked", "method": "not-run", "evidence": ["setup.log"]}
        result = compare([self.a, self.b])
        self.assertEqual(result["trial_count"], 2)
        self.assertEqual(result["outcome_counts"]["without-skill"]["failure"], 1)
        self.assertEqual(result["outcome_counts"]["candidate"]["blocked"], 1)
        self.assertEqual(result["comparable_blocks"], 0)

    def test_environment_mismatch_or_unread_treatment_prevents_comparison(self):
        for key in ("task_id", "subject_digest", "task_prompt_digest", "model", "settings_id", "environment_id"):
            other = deepcopy(self.b)
            other[key] = "different"
            self.assertEqual(compare([self.a, other])["comparable_blocks"], 0, key)
        self.b["skill"]["exposure"] = "available-unread"
        self.assertEqual(compare([self.a, self.b])["comparable_blocks"], 0)

    def test_missing_arm_is_visible(self):
        result = compare([self.b])
        self.assertEqual(result["trial_count"], 1)
        self.assertEqual(result["pairs"][0]["reasons"], ["missing arm"])

    def test_unjudged_run_cannot_look_like_a_faster_solution(self):
        for t, cost in ((self.a, 10), (self.b, 2)):
            t["measurements"]["elapsed_seconds"] = {
                "status": "observed", "value": cost, "source": "host clock"}
        self.b["outcome"] = {"status": "unjudged", "method": "independent-review", "evidence": []}
        result = compare([self.a, self.b])
        self.assertEqual(result["trial_count"], 2)
        self.assertEqual(result["comparable_blocks"], 0)
        self.assertIn("task outcome unresolved", result["pairs"][0]["reasons"])
        self.assertIsNone(result["pairs"][0]["measurements"]["elapsed_seconds"]["candidate_minus_baseline"])

    def test_different_judgment_methods_do_not_silently_match(self):
        self.b["outcome"]["method"] = "independent-review"
        result = compare([self.a, self.b])
        self.assertEqual(result["comparable_blocks"], 0)
        self.assertIn("mismatched outcome method", result["pairs"][0]["reasons"])

    def test_duplicate_runs_and_duplicate_arm_cannot_inflate_sample(self):
        with self.assertRaisesRegex(ValueError, "duplicate run_id"):
            compare([self.a, self.a])
        duplicate = deepcopy(self.a)
        duplicate["run_id"] = "second"
        with self.assertRaisesRegex(ValueError, "duplicate arm"):
            compare([self.a, duplicate])

    def test_false_zero_nonfinite_and_boolean_costs_are_rejected(self):
        for value, status in ((0, "unavailable"), (float("nan"), "observed"),
                              (float("inf"), "observed"), (-1, "observed"), (True, "observed")):
            self.b["measurements"]["review_seconds"] = {"status": status, "value": value, "source": "trace"}
            with self.assertRaises(ValueError):
                compare([self.a, self.b])

    def test_success_requires_evidence_and_self_report_remains_separate(self):
        self.b["outcome"]["evidence"] = []
        with self.assertRaisesRegex(ValueError, "needs a method and evidence"):
            compare([self.a, self.b])
        self.b["outcome"]["evidence"] = ["agent-message.md"]
        self.b["outcome"]["method"] = "self-report"
        self.assertEqual(compare([self.a, self.b])["comparable_blocks"], 0)


if __name__ == "__main__":
    unittest.main()
