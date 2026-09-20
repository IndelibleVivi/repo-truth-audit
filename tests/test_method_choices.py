"""Check synthetic subjects and counterexamples, never model method selection."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "rta_method_choice", ROOT / "evals/operation-lab/prepare_method_choice.py")
subject = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(subject)


@unittest.skipUnless(shutil.which("git"), "synthetic Git baselines require git")
class MethodChoiceSubjectsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)

    def seed(self, name: str) -> Path:
        root = self.base / name
        request = subject.prepare(name, root)
        self.assertTrue(request)
        self.assertFalse((root / "method_choice_cases.json").exists())
        self.assertFalse((root / "prepare_method_choice.py").exists())
        return root

    def observe(self, root: Path) -> tuple[str, str]:
        ledger = self.base / "observation.txt"
        ledger.write_text("old\n", encoding="utf-8")
        result = subprocess.run([sys.executable, "-I", "-B", str(root / "app.py"), "3", str(ledger)],
                                check=True, capture_output=True, text=True, timeout=5)
        return result.stdout, ledger.read_text(encoding="utf-8")

    def test_optional_helper_changes_no_application_bytes(self) -> None:
        plain = self.seed("retire-existing-green")
        optional = self.seed("retire-optional-test-first")
        for name in ("app.py", "writer.py", "legacy.py", "delivery.json", "bundle.json", "check.py"):
            self.assertEqual((plain / name).read_bytes(), (optional / name).read_bytes())
        self.assertFalse((optional / "AGENTS.md").exists())
        self.assertTrue((optional / "methods/test-first.md").is_file())
        self.assertEqual(self.observe(plain), ("3\n", "old\n3\n"))

    def test_existing_green_can_hide_real_state_defect(self) -> None:
        root = self.seed("durable-defect-optional-test-first")
        result = subprocess.run([sys.executable, "-B", str(root / "check.py")],
                                check=True, capture_output=True, text=True, timeout=10)
        self.assertIn("passed", result.stdout)
        self.assertEqual(self.observe(root), ("3\n", "old\n3\n3\n"))
        # Known evaluator repair: validates the subject's failure/repair distinction only.
        (root / "writer.py").write_bytes(subject.WRITER.encode("utf-8"))
        self.assertEqual(self.observe(root), ("3\n", "old\n3\n"))

    def test_retirement_and_bundle_need_no_new_runtime_framework(self) -> None:
        root = self.seed("retire-existing-green")
        before = self.observe(root)
        # Known valid cut, not a required implementation recipe for target agents.
        (root / "delivery.json").write_text('{"module": "writer"}\n', encoding="utf-8")
        (root / "legacy.py").unlink()
        members = ["app.py", "writer.py", "delivery.json"]
        (root / "bundle.json").write_text(json.dumps(members) + "\n", encoding="utf-8")
        self.assertEqual(self.observe(root), before)
        artifact = self.base / "artifact"
        artifact.mkdir()
        for name in json.loads((root / "bundle.json").read_text()):
            shutil.copyfile(root / name, artifact / name)
        self.assertEqual(self.observe(artifact), before)
        # Restore only the forbidden selector: the actual artifact no longer runs.
        (artifact / "delivery.json").write_text('{"module": "legacy"}\n', encoding="utf-8")
        with self.assertRaises(subprocess.CalledProcessError):
            self.observe(artifact)

    def test_required_project_policy_is_separate_from_optional_helper(self) -> None:
        root = self.seed("retire-project-required-test-first")
        self.assertEqual((root / "AGENTS.md").read_text(), subject.POLICY)
        self.assertFalse((root / "METHODS.md").exists())
        self.assertEqual(self.observe(root), ("3\n", "old\n3\n"))

    def test_dirty_subject_and_audit_control_have_real_git_state(self) -> None:
        for name in ("retire-reviewed-dirty-adapter", "audit-with-optional-test-first"):
            with self.subTest(case=name):
                root = self.seed(name)
                status = subprocess.run(["git", "status", "--porcelain"], cwd=root,
                                        check=True, capture_output=True, text=True, timeout=5).stdout
                self.assertIn(" M legacy.py", status)
                self.assertIn("?? owner-notes.txt", status)
                head = subprocess.run(["git", "show", "HEAD:legacy.py"], cwd=root,
                                      check=True, capture_output=True, text=True, timeout=5).stdout
                self.assertNotEqual(head, (root / "legacy.py").read_text())

    def test_existing_destination_is_not_overwritten(self) -> None:
        root = self.seed("retire-existing-green")
        before = (root / "writer.py").read_bytes()
        with self.assertRaises(FileExistsError):
            subject.prepare("durable-defect-optional-test-first", root)
        self.assertEqual((root / "writer.py").read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
