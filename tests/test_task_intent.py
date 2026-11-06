"""Deterministic Cedar subject/candidate checks, never model understanding."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

LAB = Path(__file__).resolve().parents[1] / "evals" / "intent-lab"
sys.path.insert(0, str(LAB))
import task_subjects as task
from prepare_intent_subject import prepare, load_cases
import check_intent_subject as checker


@unittest.skipUnless(shutil.which("git"), "prepared subjects require Git baselines")
class TaskIntentTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)

    def seed(self, name="candidate", case="task-export-handoff"):
        root = self.base / name
        prepare(case, root)
        return root

    def repair(self, root, alternate=False):
        app = root / "app.py"
        code = app.read_text()
        if alternate:
            code = code.replace('records = payload["claims"]',
                                'records = payload.get("claims", payload.get("arguments"))')
            code = code.replace('{"claims": summaries(records)}', '{"arguments": records}')
        else:
            code = code.replace('{"claims": summaries(records)}', '{"claims": records}')
        app.write_text(code)

    def snapshot(self, root):
        return {str(p.relative_to(root)): p.read_bytes()
                for p in root.rglob("*") if p.is_file()}

    def test_same_source_data_and_tests_only_current_use_differs(self):
        revision, summary = task.files("revision"), task.files("summary")
        self.assertEqual({k for k in revision if revision[k] != summary[k]},
                         {"docs/current-use.md"})
        for case, variant in task.CASES.items():
            root = self.seed(variant, case)
            task.check(root, variant)
            self.assertTrue((root / "cedar").stat().st_mode & 0o111)

    def test_catalog_and_preparation_do_not_leak_evaluator_material(self):
        catalog = {c["id"]: c for c in load_cases()}
        self.assertIn("operate_request", catalog["task-export-handoff"])
        self.assertNotIn("operate_request", catalog["task-summary-use"])
        root = self.seed()
        self.assertNotEqual(catalog["task-export-handoff"]["request"],
                            catalog["task-summary-use"]["request"])
        text = "\n".join(p.read_text() for p in root.rglob("*")
                         if p.is_file() and ".git" not in p.parts)
        for name in task.CASES:
            self.assertNotIn(name, text)
        for private in ("probe_stores", "q-71", "task_subjects.py", "review_notes"):
            self.assertNotIn(private, text)
        request = prepare("task-export-handoff", self.base / "operate", operate=True)
        self.assertIn("完整原论证 records", request)
        self.assertNotIn("q-71", request)

    def test_current_use_corruptions_are_rejected(self):
        for case, variant in task.CASES.items():
            root = self.seed(variant, case)
            task.corrupt(root, variant)
            with self.assertRaisesRegex(AssertionError, "current use"):
                task.check(root, variant)

    def test_crossed_histories_keep_summaries_but_need_distinct_answers(self):
        first, second = task.probe_stores()
        summaries = lambda store: [{"id": r["id"], "text": r["text"]}
                                    for r in store["claims"]]
        self.assertEqual(summaries(first), summaries(second))
        self.assertNotEqual(task.expected_affected(first, "lab-z", 4),
                            task.expected_affected(second, "lab-z", 4))
        self.assertEqual(len(task.expected_affected(first, "lab-z", 4)), 2)
        self.assertEqual(task.expected_affected(first, "absent", 8), [])

    def test_reference_and_alternate_packet_repairs_pass_without_candidate_writes(self):
        for name, alternate in (("nested", False), ("alternate", True)):
            root = self.seed(name)
            self.repair(root, alternate)
            before = self.snapshot(root)
            task.assert_repair(root)
            self.assertEqual(self.snapshot(root), before)

    def test_unrepaired_packet_is_rejected(self):
        root = self.seed()
        with self.assertRaisesRegex(AssertionError, "selected CLI failed"):
            task.assert_repair(root)

    def test_empty_constant_partial_and_cross_contaminated_answers_are_rejected(self):
        old = '''affected = [row for row in records if any(
            ref["source"] == args.source and ref["revision"] == args.revision
            for ref in row["references"])]'''
        for name, expression in (
            ("empty", "[]"),
            ("constant", repr(task.STORE["claims"][:1])),
            ("polluted", "records"),
            ("partial", "records[:1]"),
        ):
            with self.subTest(name=name):
                root = self.seed(name)
                self.repair(root)
                app = root / "app.py"
                code = app.read_text()
                self.assertEqual(code.count(old), 1)
                app.write_text(code.replace(old, f"affected = {expression}"))
                with self.assertRaisesRegex(AssertionError, "exact complete"):
                    task.assert_repair(root)

    def test_ignoring_revision_and_mutating_packet_or_store_are_rejected(self):
        changes = (
            ("revision", ' and ref["revision"] == args.revision', "", "exact complete"),
            ("packet", 'print(json.dumps(affected, ensure_ascii=False))',
             'args.packet.write_text("{}")\n        print(json.dumps(affected, ensure_ascii=False))',
             "preserve packet"),
            ("store", 'args.output.write_text(json.dumps(',
             'path.write_text("{}")\n        args.output.write_text(json.dumps(', "preserve input"),
        )
        for name, old, new, message in changes:
            with self.subTest(name=name):
                root = self.seed(name)
                self.repair(root)
                app = root / "app.py"
                code = app.read_text()
                self.assertEqual(code.count(old), 1)
                app.write_text(code.replace(old, new))
                with self.assertRaisesRegex(AssertionError, message):
                    task.assert_repair(root)

    def test_selected_entry_not_unused_source_is_checked(self):
        root = self.seed()
        (root / "old.py").write_text((root / "app.py").read_text())
        (root / "launch.json").write_text('{"entry": "old.py"}')
        (root / "bundle.json").write_text('["app.py", "old.py"]')
        self.repair(root)
        with self.assertRaisesRegex(AssertionError, "selected CLI failed"):
            task.assert_repair(root)

    def test_candidate_cli_uses_existing_verify_operate_entry(self):
        root = self.seed()
        self.repair(root)
        before = self.snapshot(root)
        result = subprocess.run([sys.executable, "-B", str(LAB / "check_intent_subject.py"),
                                 "--verify-operate", "task-export-handoff", "--candidate", str(root)],
                                capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertEqual(json.loads(result.stdout)["status"], "passed")
        self.assertEqual(self.snapshot(root), before)


if __name__ == "__main__":
    unittest.main()
