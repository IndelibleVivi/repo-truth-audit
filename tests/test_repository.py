from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from common import SKILL_DIR, SKILL_NAME, directory_digest, read_version  # noqa: E402
from validate_repository import EXPECTED_CASES, validate  # noqa: E402


class RepositoryContractTests(unittest.TestCase):
    def test_repository_validator_is_clean(self) -> None:
        self.assertEqual(validate(), [])

    def test_version_is_public_release(self) -> None:
        self.assertEqual(read_version(), "0.1.0")

    def test_skill_digest_is_stable_and_nonempty(self) -> None:
        first = directory_digest(SKILL_DIR)
        second = directory_digest(SKILL_DIR)
        self.assertEqual(first, second)
        self.assertEqual(len(first), 64)

    def test_all_expected_cases_have_matching_ids(self) -> None:
        for case_id in EXPECTED_CASES:
            case_path = ROOT / "evals" / "cases" / case_id / "case.json"
            payload = json.loads(case_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["case_id"], case_id)

    def test_intentional_multiplicity_verdict_canary_is_unambiguous(self) -> None:
        case_path = ROOT / "evals/cases/intentional-multiplicity/case.json"
        payload = json.loads(case_path.read_text(encoding="utf-8"))
        assertions = {
            (item.get("type"), item.get("path"), item.get("value"))
            for item in payload["assertions"]
        }
        self.assertIn(
            ("file_contains", "AUDIT.md", "Decision answer: ready"), assertions
        )
        self.assertIn(
            ("file_not_contains", "AUDIT.md", "Decision answer: not ready"),
            assertions,
        )
        self.assertNotIn(("file_contains", "AUDIT.md", "ready"), assertions)

    def test_skill_identity_is_single_canonical_path(self) -> None:
        matches = [
            path
            for path in ROOT.rglob("SKILL.md")
            if path.parent.name == SKILL_NAME
        ]
        self.assertEqual(matches, [SKILL_DIR / "SKILL.md"])


if __name__ == "__main__":
    unittest.main()
