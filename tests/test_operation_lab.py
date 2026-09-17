"""Fixture/evaluator sensitivity checks, NOT forward-model evaluation."""
from __future__ import annotations
import importlib.util
import ast
import json
from pathlib import Path
import tempfile
import unittest

PATH = Path(__file__).resolve().parents[1] / 'evals' / 'operation-lab' / 'run_operation_lab.py'
spec = importlib.util.spec_from_file_location('rta_operation_lab', PATH)
assert spec and spec.loader
lab = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lab)


class OperationLabTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='rta-lab-test-')
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / 'source'
        lab.seed(self.root)

    def test_evaluator_does_not_disable_observations_under_python_optimization(self):
        tree = ast.parse(PATH.read_text())
        self.assertFalse(any(isinstance(n, ast.Assert) for n in ast.walk(tree)))
        with self.assertRaises(AssertionError):
            lab.require_equal('broken', 'expected', 'witness')

    def test_baseline_exercises_real_manifest_selected_entry(self):
        self.assertEqual(len(lab.characterize(self.root)), 7)
        with self.assertRaisesRegex(AssertionError, 'selector'):
            lab.assert_structure(self.root)

    def test_first_cut_keeps_behavior_but_is_only_checkpoint(self):
        before = lab.characterize(self.root)
        lab.apply_known_cut(self.root, lab.CUT_ONE, lab.snapshot(self.root))
        self.assertEqual(lab.characterize(self.root), before)
        with self.assertRaises(AssertionError):
            lab.assert_structure(self.root)

    def test_two_increments_close_whole_goal_and_preserve_existing_content(self):
        owner = (self.root / 'owner-notes.txt').read_bytes()
        baseline = lab.characterize(self.root)
        lab.complete_fixture(self.root)
        self.assertEqual(lab.characterize(self.root), baseline)
        lab.assert_structure(self.root)
        self.assertEqual((self.root / 'owner-notes.txt').read_bytes(), owner)

    def test_facade_keeps_behavior_but_fails_retirement(self):
        lab.apply_known_cut(self.root, {'runner.py': 'from legacy import process\n',
                            'delivery.json': '{"module":"runner"}\n'}, lab.snapshot(self.root))
        lab.characterize(self.root)
        with self.assertRaisesRegex(AssertionError, 'not been retired'):
            lab.assert_structure(self.root)

    def test_unused_new_implementation_does_not_count_as_migration(self):
        lab.apply_known_cut(self.root, {'runner.py': lab.RUNNER, 'formatting.py': lab.FORMATTING,
                                      'storage.py': lab.STORAGE}, lab.snapshot(self.root))
        lab.characterize(self.root)
        with self.assertRaisesRegex(AssertionError, 'selector'):
            lab.assert_structure(self.root)

    def test_stale_artifact_can_pass_behavior_while_failing_completion(self):
        artifact = self.base / 'old_artifact'
        lab.build_artifact(self.root, artifact)
        lab.complete_fixture(self.root)
        self.assertEqual(lab.characterize(artifact), lab.characterize(self.root))
        lab.assert_structure(self.root)
        with self.assertRaises(AssertionError):
            lab.assert_structure(artifact)

    def test_final_declared_artifact_reaches_same_contract(self):
        lab.complete_fixture(self.root)
        artifact = self.base / 'artifact'
        lab.build_artifact(self.root, artifact)
        self.assertEqual(lab.characterize(artifact), lab.characterize(self.root))
        lab.assert_structure(artifact)
        self.assertFalse((artifact / 'owner-notes.txt').exists())

    def test_duplicate_side_effect_is_caught_despite_identical_stdout(self):
        lab.complete_fixture(self.root)
        bad = lab.RUNNER.replace('    append_receipt(rows, state)\n',
                                 '    append_receipt(rows, state)\n' * 2)
        lab.apply_known_cut(self.root, {'runner.py': bad}, lab.snapshot(self.root))
        observation = lab.observe(self.root, lab.ROWS, 'json')
        self.assertEqual(observation['stdout'], lab.PROBES[0][5])
        with self.assertRaises(AssertionError):
            lab.characterize(self.root)

    def test_follow_on_change_does_not_touch_storage_or_entry(self):
        lab.complete_fixture(self.root)
        result = lab.add_format_probe(self.root)
        self.assertEqual(result['changed_paths'], ['formatting.py'])
        lab.assert_structure(self.root)

    def test_prewrite_drift_refuses_without_overwriting_user_edit(self):
        before = lab.snapshot(self.root)
        (self.root / 'legacy.py').write_text('# concurrent edit\n')
        moved = lab.snapshot(self.root)
        with self.assertRaises(lab.ReconcileRequired):
            lab.apply_known_cut(self.root, lab.CUT_ONE, before)
        self.assertEqual(lab.snapshot(self.root), moved)

    def test_partial_increment_requires_reconciliation_instead_of_replay(self):
        before = lab.snapshot(self.root)
        (self.root / 'formatting.py').write_text(lab.FORMATTING)
        partial = lab.snapshot(self.root)
        with self.assertRaises(lab.ReconcileRequired):
            lab.apply_known_cut(self.root, lab.CUT_ONE, before)
        self.assertEqual(lab.snapshot(self.root), partial)

    def test_code_recovery_preserves_unrelated_concurrent_edit(self):
        before = lab.snapshot(self.root)
        lab.apply_known_cut(self.root, lab.CUT_ONE, before)
        after = lab.snapshot(self.root)
        (self.root / 'owner-notes.txt').write_text('new owner work\n')
        lab.restore_owned_fixture_changes(self.root, before, after)
        self.assertEqual((self.root / 'legacy.py').read_bytes(), before['legacy.py'])
        self.assertFalse((self.root / 'formatting.py').exists())
        self.assertEqual((self.root / 'owner-notes.txt').read_text(), 'new owner work\n')

    def test_code_recovery_refuses_changed_owned_postimage(self):
        before = lab.snapshot(self.root)
        lab.apply_known_cut(self.root, lab.CUT_ONE, before)
        after = lab.snapshot(self.root)
        (self.root / 'legacy.py').write_text('# user changed task-owned path\n')
        moved = lab.snapshot(self.root)
        with self.assertRaises(lab.ReconcileRequired):
            lab.restore_owned_fixture_changes(self.root, before, after)
        self.assertEqual(lab.snapshot(self.root), moved)

    def test_baseline_expectations_are_not_relearned_from_broken_candidate(self):
        (self.root / 'legacy.py').write_text(lab.LEGACY.replace("return output", "return 'wrong'"))
        with self.assertRaises(AssertionError):
            lab.characterize(self.root)

    def test_full_rehearsal_receipt_does_not_claim_model_evaluation(self):
        result = lab.run_lab()
        self.assertEqual(result['status'], 'passed')
        self.assertEqual(result['target_model_invocations'], 0)
        self.assertIn('real_model_operation', result['not_observed'])
        self.assertEqual(result['increments'][0]['whole_goal'], 'checkpoint')
        self.assertEqual(result['increments'][1]['whole_goal'], 'completed_fixture_scope')


if __name__ == '__main__':
    unittest.main()
