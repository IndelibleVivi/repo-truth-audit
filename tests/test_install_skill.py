from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from common import RECEIPT_NAME, SKILL_NAME, directory_digest  # noqa: E402
from install_skill import install  # noqa: E402


class InstallSkillTests(unittest.TestCase):
    def test_fresh_install_records_equal_digests(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            destination = Path(raw)
            receipt = install(destination)
            target = destination / SKILL_NAME
            self.assertEqual(receipt["status"], "installed")
            self.assertEqual(receipt["source_skill_digest"], directory_digest(target))
            self.assertEqual(receipt["source_skill_digest"], receipt["installed_skill_digest"])
            stored = json.loads((destination / RECEIPT_NAME).read_text(encoding="utf-8"))
            self.assertEqual(stored["installed_skill_digest"], receipt["installed_skill_digest"])

    def test_equal_install_is_no_change(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            destination = Path(raw)
            first = install(destination)
            second = install(destination)
            self.assertEqual(first["status"], "installed")
            self.assertEqual(second["status"], "unchanged")

    def test_different_target_requires_explicit_replace(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            destination = Path(raw)
            target = destination / SKILL_NAME
            target.mkdir(parents=True)
            (target / "foreign.txt").write_text("foreign\n", encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "--replace"):
                install(destination)
            self.assertTrue((target / "foreign.txt").is_file())

    def test_replace_preserves_backup_and_installs_source(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            destination = Path(raw)
            target = destination / SKILL_NAME
            target.mkdir(parents=True)
            (target / "foreign.txt").write_text("foreign\n", encoding="utf-8")
            receipt = install(destination, replace=True)
            backup = Path(receipt["backup"])
            self.assertTrue((backup / "foreign.txt").is_file())
            self.assertFalse((target / "foreign.txt").exists())
            self.assertTrue((target / "SKILL.md").is_file())


if __name__ == "__main__":
    unittest.main()
