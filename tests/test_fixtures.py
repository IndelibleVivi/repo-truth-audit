from __future__ import annotations

from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from selftest import run_checks  # noqa: E402


class FixtureContractTests(unittest.TestCase):
    def test_all_controlled_fixtures_have_their_intended_truth(self) -> None:
        self.assertEqual(run_checks(), [])


if __name__ == "__main__":
    unittest.main()
