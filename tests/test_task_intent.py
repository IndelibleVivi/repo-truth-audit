"""Deterministic Cedar subject/candidate checks, never model understanding."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

LAB = Path(__file__).resolve().parents[1] / "evals" / "intent-lab"
sys.path.insert(0, str(LAB))
import task_subjects as task
from prepare_intent_subject import prepare, load_cases
import check_intent_subject as checker
import packet_handoff_challenges as handoff


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
        code = app.read_text(encoding="utf-8")
        if alternate:
            code = code.replace('records = payload["claims"]',
                                'records = payload.get("claims", payload.get("arguments"))')
            code = code.replace('{"claims": summaries(records)}', '{"arguments": records}')
        else:
            code = code.replace('{"claims": summaries(records)}', '{"claims": records}')
        app.write_text(code, encoding="utf-8")

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
        text = "\n".join(p.read_text(encoding="utf-8") for p in root.rglob("*")
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
                code = app.read_text(encoding="utf-8")
                self.assertEqual(code.count(old), 1)
                app.write_text(code.replace(old, f"affected = {expression}"), encoding="utf-8")
                with self.assertRaisesRegex(AssertionError, "exact complete"):
                    task.assert_repair(root)

    def test_ignoring_revision_and_mutating_packet_or_store_are_rejected(self):
        changes = (
            ("revision", ' and ref["revision"] == args.revision', "", "exact complete"),
            ("packet", 'print(json.dumps(affected, ensure_ascii=False))',
             'args.packet.write_text("{}", encoding="utf-8")\n        print(json.dumps(affected, ensure_ascii=False))',
             "preserve packet"),
            ("store", 'args.output.write_text(json.dumps(',
             'path.write_text("{}", encoding="utf-8")\n        args.output.write_text(json.dumps(', "preserve input"),
        )
        for name, old, new, message in changes:
            with self.subTest(name=name):
                root = self.seed(name)
                self.repair(root)
                app = root / "app.py"
                code = app.read_text(encoding="utf-8")
                self.assertEqual(code.count(old), 1)
                app.write_text(code.replace(old, new), encoding="utf-8")
                with self.assertRaisesRegex(AssertionError, message):
                    task.assert_repair(root)

    def test_selected_entry_not_unused_source_is_checked(self):
        root = self.seed()
        (root / "old.py").write_text((root / "app.py").read_text(encoding="utf-8"), encoding="utf-8")
        (root / "launch.json").write_text('{"entry": "old.py"}', encoding="utf-8")
        (root / "bundle.json").write_text('["app.py", "old.py"]', encoding="utf-8")
        self.repair(root)
        with self.assertRaisesRegex(AssertionError, "selected CLI failed"):
            task.assert_repair(root)

    def test_packet_consumer_cannot_borrow_producer_local_caches(self):
        for name in ("relative-producer-cache", "absolute-producer-cache",
                     "absolute-cache-pointer", "input-sidecar-pointer", "packet-sidecar",
                     "home-cache", "temporary-cache"):
            with self.subTest(name=name):
                root = self.seed(name)
                handoff.candidate(root, name)
                before = self.snapshot(root)
                self.assertTrue(handoff.local_roundtrip(root))
                with self.assertRaisesRegex(AssertionError, "selected CLI failed"):
                    task.assert_repair(root)
                self.assertEqual(self.snapshot(root), before)

    def test_packet_witness_preserves_distinct_packets_on_same_consumer(self):
        # An implementation that caches one correct packet and reuses it for
        # every later path passes a fresh-reader-per-packet witness. Crossed
        # histories have equal summaries but different affected records.
        root = self.seed()
        self.repair(root)
        app = root / "app.py"
        code = app.read_text(encoding="utf-8").replace('        affected = [row for row in records if any(',
            '        cache = Path(".first-read.json")\n'
            '        if cache.exists():\n'
            '            records = json.loads(cache.read_text(encoding="utf-8"))\n'
            '        else:\n'
            '            cache.write_text(json.dumps(records), encoding="utf-8")\n'
            '        affected = [row for row in records if any(')
        app.write_text(code, encoding="utf-8")
        with self.assertRaisesRegex(AssertionError, "exact complete"):
            task.assert_repair(root)

    def test_packet_consumer_cannot_borrow_inherited_application_data(self):
        for variant in ("xdg-data-cache", "appdata-cache"):
            with self.subTest(variant=variant):
                root = self.seed(variant)
                handoff.candidate(root, variant)
                before = self.snapshot(root)
                self.assertTrue(handoff.local_roundtrip(root))
                ambient = handoff.private_application_data(self.base / f"ambient-{variant}")
                with patch.dict(os.environ, ambient):
                    with self.assertRaisesRegex(AssertionError, "selected CLI failed"):
                        task.assert_repair(root)
                    self.assertTrue(all(not list(Path(path).rglob("*")) for path in ambient.values()),
                                    "role processes must not use inherited app-data directories")
                self.assertEqual(self.snapshot(root), before)

    def test_role_application_directories_are_separate_and_caller_environment_is_preserved(self):
        before = dict(os.environ)
        first = task._role_environment(self.base / "producer")
        second = task._role_environment(self.base / "recipient")
        for variable in ("HOME", "USERPROFILE", "XDG_CACHE_HOME", "XDG_DATA_HOME",
                         "XDG_CONFIG_HOME", "XDG_STATE_HOME", "APPDATA", "LOCALAPPDATA",
                         "TMPDIR", "TMP", "TEMP"):
            with self.subTest(variable=variable):
                self.assertNotEqual(first[variable], second[variable])
                self.assertTrue(Path(first[variable]).is_relative_to(self.base / "producer"))
                self.assertTrue(Path(second[variable]).is_relative_to(self.base / "recipient"))
        self.assertEqual(dict(os.environ), before)

    def test_complete_candidate_passes_with_ascii_parent_locale(self):
        root = self.seed()
        self.repair(root)
        before = self.snapshot(root)
        environment = {**os.environ, "LC_ALL": "C", "LANG": "C", "PYTHONUTF8": "0",
                       "PYTHONCOERCECLOCALE": "0"}
        result = subprocess.run([sys.executable, "-B", str(LAB / "check_intent_subject.py"),
                                 "--verify-operate", "task-export-handoff", "--candidate", str(root)],
                                env=environment, capture_output=True, encoding="utf-8", timeout=60)
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertEqual(json.loads(result.stdout)["status"], "passed")
        self.assertEqual(self.snapshot(root), before)

    def test_complete_source_does_not_hide_artifact_only_cache_fallback(self):
        root = self.seed()
        handoff.candidate(root, "artifact-cache-fallback")
        before = self.snapshot(root)
        with self.assertRaisesRegex(AssertionError, "artifact-received"):
            task.assert_repair(root)
        self.assertEqual(self.snapshot(root), before)

    def test_candidate_cli_uses_existing_verify_operate_entry(self):
        root = self.seed()
        self.repair(root)
        before = self.snapshot(root)
        result = subprocess.run([sys.executable, "-B", str(LAB / "check_intent_subject.py"),
                                 "--verify-operate", "task-export-handoff", "--candidate", str(root)],
                                capture_output=True, encoding="utf-8", timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertEqual(json.loads(result.stdout)["status"], "passed")
        evidence = json.loads(result.stdout)["evidence"]
        self.assertIn("independent_packet_recipient", evidence["proof_layers"])
        self.assertFalse(evidence["os_isolation"])
        self.assertEqual(self.snapshot(root), before)


if __name__ == "__main__":
    unittest.main()
