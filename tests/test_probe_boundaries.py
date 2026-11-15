"""Read-only evaluator output must never replace the product it observes."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ProbeBoundaryTests(unittest.TestCase):
    def test_field_receipts_cannot_overwrite_observed_inputs(self):
        with tempfile.TemporaryDirectory() as raw:
            base = Path(raw)
            source, seed = base / "source", base / "seed"
            source.mkdir(); seed.mkdir()
            for script, args, protected in (
                ("probe_dotenv.py", ["--repo", str(source)], source),
                ("probe_mitt.py", ["--source", str(source), "--consumer-seed", str(seed)], source),
                ("probe_mitt.py", ["--source", str(source), "--consumer-seed", str(seed)], seed),
                ("probe_viper.py", ["--repo", str(source), "--go", sys.executable], source),
            ):
                with self.subTest(script=script, protected=protected.name):
                    original = protected / "product.txt"
                    original.write_bytes(b"owned input\n")
                    result = subprocess.run([sys.executable, str(ROOT / "evals/field" / script),
                                             *args, "--output", str(original)],
                                            capture_output=True, text=True, timeout=10)
                    self.assertEqual(result.returncode, 2, result.stderr)
                    self.assertIn("outside", result.stderr)
                    self.assertEqual(original.read_bytes(), b"owned input\n")

    def test_trial_receipt_cannot_overwrite_subject_or_delivered_artifact(self):
        with tempfile.TemporaryDirectory() as raw:
            base = Path(raw)
            subject = base / "subject"
            subject.mkdir()
            for original in (subject / "app.py", base / "delivered.zip"):
                with self.subTest(path=original.name):
                    original.write_bytes(b"owned input\n")
                    result = subprocess.run([
                        sys.executable,
                        str(ROOT / "evals/experiments/2026-11-user-outcomes/verify_trial.py"),
                        "resume", str(subject), "--artifact", str(base / "delivered.zip"),
                        "--output", str(original)], capture_output=True, text=True, timeout=10)
                    self.assertEqual(result.returncode, 2, result.stderr)
                    self.assertIn("must not overwrite", result.stderr)
                    self.assertEqual(original.read_bytes(), b"owned input\n")


if __name__ == "__main__":
    unittest.main()
