from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import install_skill  # noqa: E402
from common import (  # noqa: E402
    RECEIPT_NAME,
    SKILL_DIR,
    SKILL_NAME,
    SKILL_PAYLOAD_FILES,
    copy_payload,
    directory_digest,
    undeclared_payload_entries,
)
from install_skill import install  # noqa: E402


#: Bytecode cache name used to simulate host residue in an installed tree.
RESIDUE_RELATIVE = Path("scripts") / "__pycache__" / "check_evidence.cpython-000.pyc"


def build_payload_tree(root: Path) -> None:
    """Recreate the declared payload below ``root`` without runtime residue."""

    copy_payload(SKILL_DIR, root, SKILL_PAYLOAD_FILES)


def generate_bytecode_cache(payload_root: Path) -> list[Path]:
    """Import the copied checker so CPython writes its ordinary bytecode cache."""

    script = payload_root / "scripts" / "check_evidence.py"
    module_name = "rta_payload_bytecode_probe"
    saved_prefix = getattr(sys, "pycache_prefix", None)
    saved_write = sys.dont_write_bytecode
    try:
        # Write the cache beside the copied source instead of a host-wide cache.
        sys.pycache_prefix = None
        sys.dont_write_bytecode = False
        spec = importlib.util.spec_from_file_location(module_name, script)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    finally:
        sys.pycache_prefix = saved_prefix
        sys.dont_write_bytecode = saved_write
        sys.modules.pop(module_name, None)
    return sorted((script.parent / "__pycache__").glob("*.pyc"))


def payload_tree_files(root: Path) -> list[str]:
    """Return the relative POSIX paths of every file below ``root``."""

    return sorted(
        path.relative_to(root).as_posix() for path in root.rglob("*") if path.is_file()
    )


class InstallSkillTests(unittest.TestCase):
    def test_fresh_install_records_equal_digests(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            destination = Path(raw)
            receipt = install(destination)
            target = destination / SKILL_NAME
            self.assertEqual(receipt["status"], "installed")
            self.assertEqual(
                receipt["source_skill_digest"],
                directory_digest(target, SKILL_PAYLOAD_FILES),
            )
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

    def test_import_generated_bytecode_does_not_change_payload_identity(self) -> None:
        """Ordinary Python bytecode caching must not change payload identity.

        A clean payload copy and a copy whose ``scripts/check_evidence.py`` was
        actually imported install to identical declared bytes and digest, and the
        generated cache stays out of the staged and installed payload.
        """

        with tempfile.TemporaryDirectory() as raw:
            workspace = Path(raw)
            clean_source = workspace / "clean-source"
            imported_source = workspace / "imported-source"
            build_payload_tree(clean_source)
            build_payload_tree(imported_source)

            generated = generate_bytecode_cache(imported_source)
            self.assertTrue(
                generated, "ordinary import did not generate bytecode residue"
            )
            for cache in generated:
                self.assertEqual(
                    cache.parent, imported_source / "scripts" / "__pycache__"
                )
                self.assertEqual(cache.suffix, ".pyc")
            self.assertEqual(undeclared_payload_entries(imported_source), [])

            clean_destination = workspace / "clean-dest"
            imported_destination = workspace / "imported-dest"
            # Only the installer source root is patched; the install still runs
            # repository validation against the real checkout.
            with mock.patch.object(install_skill, "SKILL_DIR", clean_source):
                clean_receipt = install(clean_destination)
            with mock.patch.object(install_skill, "SKILL_DIR", imported_source):
                imported_receipt = install(imported_destination)

            self.assertEqual(clean_receipt["status"], "installed")
            self.assertEqual(imported_receipt["status"], "installed")
            self.assertEqual(
                imported_receipt["source_skill_digest"],
                clean_receipt["source_skill_digest"],
            )
            self.assertEqual(
                imported_receipt["installed_skill_digest"],
                clean_receipt["installed_skill_digest"],
            )

            for destination, receipt in (
                (clean_destination, clean_receipt),
                (imported_destination, imported_receipt),
            ):
                target = destination / SKILL_NAME
                # The installed tree is the staged payload after replace, so its
                # exact file set proves the cache never entered either one.
                self.assertEqual(
                    payload_tree_files(target), sorted(SKILL_PAYLOAD_FILES)
                )
                self.assertEqual(
                    [path for path in target.rglob("*") if path.name == "__pycache__"],
                    [],
                )
                self.assertEqual(
                    sorted(path.name for path in destination.iterdir()),
                    sorted([SKILL_NAME, RECEIPT_NAME]),
                )
                self.assertEqual(
                    receipt["installed_skill_digest"],
                    directory_digest(target, SKILL_PAYLOAD_FILES),
                )

    def test_known_installed_residue_is_ignored_but_undeclared_content_is_not(
        self,
    ) -> None:
        """Known host residue keeps identity; it is not acceptance of undeclared files.

        Ignoring ``__pycache__`` bytecode preserves the declared identity of an
        already installed tree. Undeclared source or executable files are still
        rejected in the canonical source and detected as different content in an
        installed target (``test_installed_extra_file_is_different_content``).
        """

        with tempfile.TemporaryDirectory() as raw:
            destination = Path(raw)
            first = install(destination)
            target = destination / SKILL_NAME
            residue = target / RESIDUE_RELATIVE
            residue.parent.mkdir(parents=True, exist_ok=True)
            residue.write_bytes(b"runtime residue\n")
            second = install(destination)
            self.assertEqual(second["status"], "unchanged")
            self.assertEqual(
                second["installed_skill_digest"], first["installed_skill_digest"]
            )

    def test_installed_extra_file_is_different_content(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            destination = Path(raw)
            install(destination)
            target = destination / SKILL_NAME
            (target / "scripts" / "helper.py").write_text("x = 1\n", encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "--replace"):
                install(destination)
            self.assertTrue((target / "scripts" / "helper.py").is_file())

    def test_declared_byte_change_alters_payload_digest(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            build_payload_tree(root)
            before = directory_digest(root, SKILL_PAYLOAD_FILES)
            changed = root / "references" / "recovery.md"
            changed.write_bytes(changed.read_bytes() + b"\n")
            self.assertNotEqual(
                directory_digest(root, SKILL_PAYLOAD_FILES), before
            )

    def test_symlinked_payload_file_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            build_payload_tree(root)
            link = root / "NOTICE.md"
            link.unlink()
            try:
                link.symlink_to(SKILL_DIR / "NOTICE.md")
            except (NotImplementedError, OSError) as exc:
                self.skipTest(f"symlink creation unavailable on this host: {exc}")
            with self.assertRaisesRegex(ValueError, "symlink"):
                directory_digest(root, SKILL_PAYLOAD_FILES)
            with self.assertRaisesRegex(ValueError, "symlink"):
                copy_payload(root, Path(raw) / "out", SKILL_PAYLOAD_FILES)

    def test_undeclared_executable_source_file_is_rejected(self) -> None:
        """An undeclared executable source file is rejected, not ignored as residue."""

        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw) / "skill"
            build_payload_tree(root)
            stray = root / "scripts" / "helper.py"
            stray.write_text("x = 1\n", encoding="utf-8")
            if os.name == "posix":
                # Executable bits are a POSIX concept; the undeclared-entry
                # rejection below is platform-neutral.
                stray.chmod(0o755)
                self.assertTrue(stray.stat().st_mode & 0o111)
            self.assertEqual(undeclared_payload_entries(root), ["scripts/helper.py"])
            with tempfile.TemporaryDirectory() as dest_raw:
                with mock.patch.object(install_skill, "SKILL_DIR", root):
                    with self.assertRaisesRegex(RuntimeError, "undeclared payload"):
                        install(Path(dest_raw))


if __name__ == "__main__":
    unittest.main()
