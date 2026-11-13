"""Deterministic consumer-first experiment preparation and consumer checks."""
from __future__ import annotations

import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
EXPERIMENT = ROOT / "evals/experiments/2026-11-consumer-first"
sys.path.insert(0, str(EXPERIMENT))

import prepare_trial  # noqa: E402
import subjects  # noqa: E402
import verify_trial  # noqa: E402

class ConsumerFirstTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)

    def prepared(self, task: str, language: str = "en") -> Path:
        path = self.base / f"{task}-{language}"
        receipt = prepare_trial.prepare(task, path, language)
        self.assertEqual(receipt["target_model_invocations"], 0)
        return path

    def test_preregistration_is_the_same_derived_payload_with_twelve_slots(self) -> None:
        stored = json.loads((EXPERIMENT / "preregistration.json").read_text(encoding="utf-8"))
        self.assertEqual(stored, prepare_trial.preregistration())
        slots = stored["slots"]
        self.assertEqual(len(slots), 12)
        self.assertEqual({row["slot"] for row in slots}, set(range(1, 13)))
        identities = {(row["task_id"], row["arm"]) for row in slots}
        self.assertEqual(identities, {
            (task, arm) for task in prepare_trial.TASKS for arm in prepare_trial.ARMS
        })
        self.assertEqual(stored["order_seed"], "consumer-first-2026-11-14-v1")
        self.assertEqual(stored["target_model_invocations_observed_now"], 0)
        self.assertEqual(stored["maximum_target_model_invocations"], 12)

    def test_receipts_separate_inventory_from_actual_protected_inputs(self) -> None:
        targets = {
            "migration-recovery": {"TASK.md", "owner-notes.txt", "CHECKPOINT.md", "entry.py"},
            "delivery-adoption": {"TASK.md", "PROGRAM.md", "store.json",
                                  "supplied-worksheet.json", "docs/current-use.md"},
            "known-bug": {"TASK.md"},
        }
        for task, protected in targets.items():
            with self.subTest(task=task):
                receipt = prepare_trial.prepare(task, self.base / task)
                self.assertEqual(set(receipt["protected_inputs"]), protected)
                self.assertIn("TASK.md", receipt["initial_files"])
                if task == "migration-recovery":
                    self.assertIn("bundle.json", receipt["initial_files"])
                    self.assertIn("delivery.json", receipt["initial_files"])
                if task == "known-bug":
                    self.assertIn("app.py", receipt["initial_files"])
                    self.assertNotIn("app.py", receipt["protected_inputs"])
        clean = self.base / "clean-baseline"
        clean_receipt = prepare_trial.prepare("clean-baseline", clean)
        self.assertEqual(set(clean_receipt["protected_inputs"]),
                         set(clean_receipt["initial_files"]) | {"TASK.md"})
        for name in clean_receipt["initial_files"]:
            self.assertTrue((clean / name).is_file())

    def test_clean_subject_is_coherent_and_unchanged_accepted(self) -> None:
        root = self.prepared("clean-baseline")
        (root / "INTENT-AUDIT.md").write_text(
            "Decision answer: no change is warranted for the stated local use.\n",
            encoding="utf-8")
        result = verify_trial.verify_clean(root)
        self.assertTrue(result["bytes_unchanged"])
        self.assertEqual(json.loads(result["behavior"]["4-2"]["stdout"]), [2, 3, 4])

    def test_known_bug_allows_real_regression_edit_and_accepts_bundle_helper(self) -> None:
        root = self.prepared("known-bug")
        subjects.apply_known_range_repair(root)
        with (root / "test_app.py").open("a", encoding="utf-8") as handle:
            handle.write("\nassert run('4-2') == [2, 3, 4]\n")
        (root / "README.md").write_text("# Updated accepted behavior\n", encoding="utf-8")
        (root / "range_support.py").write_text("def marker():\n    return True\n", encoding="utf-8")
        members = json.loads((root / "bundle.json").read_text(encoding="utf-8"))
        members.append("range_support.py")
        (root / "bundle.json").write_text(json.dumps(members) + "\n", encoding="utf-8")
        result = verify_trial.verify_known_bug(root)
        self.assertEqual(result["valid_neighbor"], [2, 3, 4])
        # A source-only repair that leaves the selected entry stale must fail.
        (root / "app.py").write_text(subjects.RANGE_BUGGY, encoding="utf-8")
        with self.assertRaisesRegex(AssertionError, "wrong valid expansion"):
            verify_trial.verify_known_bug(root)

    def test_known_bug_source_only_repair_cannot_hide_in_artifact(self) -> None:
        root = self.prepared("known-bug")
        subjects.apply_known_range_repair(root)
        broken = root / "broken.py"
        broken.write_text(subjects.RANGE_BUGGY, encoding="utf-8")
        (root / "launch.json").write_text('{"entry": "broken.py"}\n', encoding="utf-8")
        members = json.loads((root / "bundle.json").read_text(encoding="utf-8"))
        members.append("broken.py")
        (root / "bundle.json").write_text(json.dumps(members) + "\n", encoding="utf-8")
        with self.assertRaisesRegex(AssertionError, "wrong valid expansion"):
            verify_trial.verify_known_bug(root)

    def test_migration_requires_actual_zip_and_legitimate_forwarding_shim(self) -> None:
        root = self.prepared("migration-recovery")
        fixture = verify_trial.module(
            "consumer_test_resume", ROOT / "evals/operation-lab/run_operation_lab.py")
        fixture.complete_fixture(root)
        forwarding = '"""Compatibility export for unselected callers."""\nfrom runner import process\n'
        (root / "legacy.py").write_text(forwarding, encoding="utf-8")
        # Newly built artifact initially missing: source work is not enough.
        with self.assertRaisesRegex(AssertionError, "deliverable.zip"):
            verify_trial.verify_migration(root, None)
        stale = self.base / "stale.zip"
        with zipfile.ZipFile(stale, "w") as package:
            package.writestr("delivery.json", '{"module": "legacy"}\n')
        with self.assertRaisesRegex(AssertionError, "ZIP|artifact|legacy"):
            verify_trial.verify_migration(root, stale)
        actual = verify_trial.write_migration_zip(root)
        result = verify_trial.verify_migration(root, actual)
        self.assertTrue(result["deliverable_zip_verified"])
        self.assertTrue(result["unselected_legacy_reexport"])

    def test_partial_migration_is_rejected(self) -> None:
        root = self.prepared("migration-recovery")
        with self.assertRaisesRegex(AssertionError, "legacy|bundle|deliverable"):
            verify_trial.verify_migration(root, None)

    def test_behavioral_success_cannot_hide_writer_in_runner(self) -> None:
        root = self.prepared("migration-recovery")
        fixture = verify_trial.module("consumer_wrong_owner", ROOT / "evals/operation-lab/run_operation_lab.py")
        fixture.complete_fixture(root)
        (root / "runner.py").write_text(fixture.TRANSITION, encoding="utf-8")
        fixture.characterize(root)
        actual = verify_trial.write_migration_zip(root)
        with self.assertRaisesRegex(AssertionError, "storage owner"):
            verify_trial.verify_migration(root, actual)

    def test_chinese_task_is_verified_with_its_registered_language(self) -> None:
        root = self.prepared("clean-baseline", "zh-CN")
        (root / "INTENT-AUDIT.md").write_text("Decision answer: 当前约定无需修改。\n", encoding="utf-8")
        self.assertEqual(verify_trial.verify("clean-baseline", root, language="zh-CN")["status"], "passed")
        with self.assertRaisesRegex(AssertionError, "prompt"):
            verify_trial.verify("clean-baseline", root, language="en")

    def test_ascii_locale_child_still_grades(self) -> None:
        root = self.prepared("known-bug")
        subjects.apply_known_range_repair(root)
        old = {name: os.environ.get(name) for name in ("LANG", "LC_ALL", "PYTHONUTF8")}
        os.environ.update({"LANG": "C", "LC_ALL": "C", "PYTHONUTF8": "1"})
        try:
            verify_trial.verify_known_bug(root)
        finally:
            for name, value in old.items():
                if value is None:
                    os.environ.pop(name, None)
                else:
                    os.environ[name] = value

    def test_review_packet_is_anonymous_and_missing_time_stays_null(self) -> None:
        result = self.base / "RESULT.md"
        result.write_text("consumer-first and progressive-rta migrated successfully\n",
                          encoding="utf-8")
        module = verify_trial.module("consumer_review", EXPERIMENT / "prepare_review.py")
        payload = module.packet("migration-recovery", "consumer-first",
                                result.read_text(encoding="utf-8"), "opaque-result")
        public = module.public_packet(payload)
        serialized = json.dumps(public)
        for planted in ("consumer-first", "progressive-rta", "without-skill",
                        "repository-operational-truth-audit"):
            self.assertNotIn(planted, serialized)
        self.assertNotIn("arm", public)
        self.assertIsNone(public["timing"]["human_active_seconds"])
        self.assertIsNone(public["timing"]["agent_elapsed_seconds"])

if __name__ == "__main__":
    unittest.main()
