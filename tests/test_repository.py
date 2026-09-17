from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from common import (  # noqa: E402
    SKILL_DIR,
    SKILL_NAME,
    SKILL_PAYLOAD_FILES,
    directory_digest,
    read_version,
)
from validate_repository import EXPECTED_CASES, validate  # noqa: E402


class RepositoryContractTests(unittest.TestCase):
    def test_repository_validator_is_clean(self) -> None:
        self.assertEqual(validate(), [])

    def test_source_version_is_stable_semver(self) -> None:
        self.assertRegex(read_version(), r"^[0-9]+\.[0-9]+\.[0-9]+$")

    def test_public_release_install_ref_remains_immutable(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("--ref v0.1.0", readme)
        self.assertNotIn("--ref v0.2.0", readme)

    def test_skill_digest_is_stable_and_nonempty(self) -> None:
        first = directory_digest(SKILL_DIR, SKILL_PAYLOAD_FILES)
        second = directory_digest(SKILL_DIR, SKILL_PAYLOAD_FILES)
        self.assertEqual(first, second)
        self.assertEqual(len(first), 64)

    def test_directory_digest_uses_portable_relative_path_order(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            payloads = {
                "B.txt": b"uppercase\n",
                "a.txt": b"lowercase\n",
            }
            for relative, content in payloads.items():
                (root / relative).write_bytes(content)

            expected = hashlib.sha256()
            for relative in sorted(payloads):
                expected.update(relative.encode("utf-8"))
                expected.update(b"\0")
                expected.update(b"0\0")
                expected.update(payloads[relative])
                expected.update(b"\0")

            self.assertEqual(
                directory_digest(root, ["B.txt", "a.txt"]), expected.hexdigest()
            )

    def test_all_expected_cases_have_matching_ids(self) -> None:
        for case_id in EXPECTED_CASES:
            case_path = ROOT / "evals" / "cases" / case_id / "case.json"
            payload = json.loads(case_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["case_id"], case_id)

    def test_mode_controls_keep_write_authority_explicit(self) -> None:
        import csv

        with (ROOT / "evals/mode-prompts.csv").open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        for row in rows:
            expected = "yes" if row["expected_mode"] == "operate" else "no"
            self.assertEqual(row["target_mutation"], expected, row["id"])
        by_id = {row["id"]: row for row in rows}
        self.assertEqual(by_id["unbounded-cleanup"]["expected_mode"], "reconnaissance")

    def test_runtime_body_excludes_bounded_non_topology_work(self) -> None:
        skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        body = skill.split("---", 2)[2]
        operation = (SKILL_DIR / "references/operation.md").read_text(encoding="utf-8")
        for text in (body, operation):
            normalized = " ".join(text.split())
            self.assertIn("isolated known-bug repair", normalized)
            self.assertIn("no repository-topology question", normalized)

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
