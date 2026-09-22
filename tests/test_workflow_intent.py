"""Behavioral ground truth for realistic dialogue and normal-use burden subjects."""
from pathlib import Path
import sys
import tempfile
import unittest

LAB = Path(__file__).resolve().parents[1] / "evals" / "intent-lab"
sys.path.insert(0, str(LAB))
import workflow_subjects as workflow
from prepare_intent_subject import write_subject


class WorkflowSubjectTests(unittest.TestCase):
    def test_same_complete_functionality_has_different_normal_steps(self):
        with tempfile.TemporaryDirectory() as raw:
            for variant in ("direct", "gated", "accepted"):
                with self.subTest(variant=variant):
                    root = Path(raw) / variant
                    write_subject(root, workflow.files(variant))
                    workflow.check(root, variant)

    def test_later_consent_changes_authority_without_changing_implementation(self):
        before = workflow.files("gated")
        after = workflow.files("accepted")
        changed = {name for name in before if before[name] != after[name]}
        self.assertEqual(changed, {"docs/development-chat.md"})
        self.assertTrue(after["docs/development-chat.md"].startswith(before["docs/development-chat.md"]))

    def test_broken_workflow_and_erased_later_consent_are_rejected(self):
        with tempfile.TemporaryDirectory() as raw:
            for variant in ("direct", "gated", "accepted"):
                with self.subTest(variant=variant):
                    root = Path(raw) / variant
                    write_subject(root, workflow.files(variant))
                    workflow.corrupt(root, variant)
                    with self.assertRaises(AssertionError):
                        workflow.check(root, variant)

    def test_subject_contains_dialogue_without_evaluator_answers(self):
        for variant in ("direct", "gated", "accepted"):
            payload = workflow.files(variant)
            self.assertNotIn("AGENTS.md", payload)
            chat = payload["docs/development-chat.md"]
            for label in ("Adopted", "Rejected", "supersedes", "expected", "ground truth"):
                self.assertNotIn(label, chat)
            for case_id in workflow.CASES:
                self.assertNotIn(case_id, "\n".join(payload.values()))


if __name__ == "__main__":
    unittest.main()
