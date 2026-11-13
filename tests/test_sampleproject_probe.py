"""Offline tests: no package download, external checkout or model required."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location(
    "sampleproject_probe", Path(__file__).resolve().parents[1] / "evals/field/probe_sampleproject.py")
probe = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(probe)


def readings():
    rows = {}
    for name, (value, kind) in probe.EXPECTED.items():
        rows[name] = {"value": value,
                      "module_file": ("<temporary>/regular/lib/python3.13/site-packages/sample/simple.py"
                                      if kind == "wheel" else "<temporary>/source/src/sample/simple.py"),
                      "direct_url": ({"url": "file://<temporary>/wheel-1/sampleproject-4.0.0-py3-none-any.whl",
                                      "archive_info": {}} if kind == "wheel" else
                                     {"url": "file://<temporary>/source", "dir_info": {"editable": True}})}
    return rows


class SelectionTests(unittest.TestCase):
    def test_expected_matrix_accepts_legitimate_frozen_wheel(self):
        rows = readings()
        self.assertEqual(rows["owner-edit-frozen-wheel"]["value"], 12)
        self.assertEqual(rows["owner-edit-editable"]["value"], 13)
        self.assertTrue(probe.matrix_matches(rows))

    def test_reject_value_or_missing_neighbor(self):
        for name in probe.EXPECTED:
            with self.subTest(name=name):
                rows = readings()
                rows[name]["value"] += 1
                self.assertFalse(probe.matrix_matches(rows))
        rows = readings()
        rows.pop("owner-edit-frozen-wheel")
        self.assertFalse(probe.matrix_matches(rows))

    def test_reject_checkout_shim_as_editable_and_wrong_selected_origin(self):
        for change in ("metadata", "origin", "wheel-metadata", "malformed-metadata"):
            rows = readings()
            if change == "metadata":
                rows["editable"]["direct_url"] = None
            elif change == "origin":
                rows["delivered-wheel"]["module_file"] = "<temporary>/source/src/sample/simple.py"
            elif change == "malformed-metadata":
                rows["editable"]["direct_url"] = ["wrong shape"]
            else:
                rows["baseline-wheel"]["direct_url"] = {"dir_info": {"editable": True}}
            self.assertFalse(probe.matrix_matches(rows))

    def test_protect_both_overlap_directions(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            source, seed = root / "source", root / "seed"
            probe.protect(source, seed, root / "receipt.json")
            for a, b in ((source, source / "seed"), (source / "nested", source)):
                with self.assertRaises(ValueError):
                    probe.protect(a, b)
            for output in (source / "receipt.json", seed / "receipt.json", root):
                with self.assertRaises(ValueError):
                    probe.protect(source, seed, output)

    def test_symlink_output_rejected_before_probe_or_write(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            source, seed = root / "source", root / "seed"
            source.mkdir()
            seed.mkdir()
            victim = source / "README.md"
            victim.write_text("preserve", encoding="utf-8")
            link = root / "alias"
            link.symlink_to(source, target_is_directory=True)
            with patch.object(probe, "probe") as execute, contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as caught:
                    probe.main(["--source", str(source), "--seed", str(seed),
                                "--output", str(link / "README.md")])
                self.assertEqual(caught.exception.code, 2)
                execute.assert_not_called()
            self.assertEqual(victim.read_text(encoding="utf-8"), "preserve")
            with self.assertRaises(ValueError):
                probe.protect(source, link)

    def test_cli_setup_failure_differs_from_mismatch(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            argv = ["--source", str(root / "source"), "--seed", str(root / "seed")]
            with patch.object(probe, "probe", side_effect=probe.SetupBlocked("missing wheel")):
                with contextlib.redirect_stdout(io.StringIO()) as output:
                    self.assertEqual(probe.main(argv), 2)
                self.assertEqual(json.loads(output.getvalue())["status"], "setup-blocked")
            with patch.object(probe, "probe", return_value={"status": "expectation-mismatch"}):
                with contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(probe.main(argv), 1)

    def test_real_setup_failure_keeps_portable_command_evidence(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            source, seed = root / "source", root / "seed"
            source.mkdir()
            seed.mkdir()
            with contextlib.redirect_stdout(io.StringIO()) as output:
                code = probe.main(["--source", str(source), "--seed", str(seed)])
            report = json.loads(output.getvalue())
            self.assertEqual(code, 2)
            self.assertEqual(report["status"], "setup-blocked")
            self.assertEqual(report["commands"][0]["argv"], ["git", "rev-parse", "HEAD"])
            self.assertNotEqual(report["commands"][0]["exit_code"], 0)
            self.assertNotIn(str(root), output.getvalue())

    def test_ready_consumer_failure_or_invalid_json_is_mismatch(self):
        for output, code in (("panic", 1), ("not json", 0), ('{"value": 12}', 2)):
            with self.subTest(output=output, code=code):
                row = probe.consumer_reading(output, code)
                self.assertIn("observation_error", row)
                rows = readings()
                rows["editable"] = row
                self.assertFalse(probe.matrix_matches(rows))
        self.assertEqual(probe.consumer_reading('{"value": 12}', 0)["value"], 12)

    def test_snapshot_detects_file_and_symlink_changes(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            (root / "input").write_text("original", encoding="utf-8")
            before = probe.snapshot(root)
            (root / "input").write_text("mutated", encoding="utf-8")
            self.assertNotEqual(before, probe.snapshot(root))
            before = probe.snapshot(root)
            (root / "alias").symlink_to(root / "input")
            self.assertNotEqual(before, probe.snapshot(root))


if __name__ == "__main__":
    unittest.main()
