"""Documentation navigation and release-preparation checks, not model evals."""
from __future__ import annotations

from pathlib import Path
import re
import sys
import unittest
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from validate_repository import PUBLIC_RELEASE_VERSION  # noqa: E402

PAIRS = (
    ("README.md", "README.zh-CN.md"),
    ("docs/usage.md", "docs/usage.zh-CN.md"),
    ("docs/release-preparation.md", "docs/release-preparation.zh-CN.md"),
    ("docs/releases/v0.2.0.md", "docs/releases/v0.2.0.zh-CN.md"),
    ("docs/releases/v0.2.1.md", "docs/releases/v0.2.1.zh-CN.md"),
    ("docs/forward-0.2.1-receipt.md", "docs/forward-0.2.1-receipt.zh-CN.md"),
    ("docs/forward-0.3.0-receipt.md", "docs/forward-0.3.0-receipt.zh-CN.md"),
    ("docs/forward-0.3.0-followup.md", "docs/forward-0.3.0-followup.zh-CN.md"),
    ("docs/releases/v0.3.0.md", "docs/releases/v0.3.0.zh-CN.md"),
)


def headings(content: str) -> set[str]:
    result: set[str] = set()
    in_fence = False
    for line in content.splitlines():
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        match = re.match(r"^#{1,6}\s+(.+?)\s*$", line)
        if match and not in_fence:
            label = re.sub(r"[^\w\s-]", "", match.group(1).strip().lower())
            result.add(re.sub(r"\s", "-", label))
    return result


class DocumentationTests(unittest.TestCase):
    def test_new_guides_have_paired_localized_navigation(self) -> None:
        for en, zh in PAIRS:
            for source, target in ((en, zh), (zh, en)):
                with self.subTest(source=source):
                    path = ROOT / source
                    self.assertTrue(path.is_file())
                    self.assertIn(f"]({Path(target).name})", path.read_text(encoding="utf-8"))

    def test_local_guide_links_and_heading_anchors_resolve(self) -> None:
        for relative in [item for pair in PAIRS for item in pair]:
            path = ROOT / relative
            content = path.read_text(encoding="utf-8")
            for raw in re.findall(r"\[[^\]]*\]\(([^)]+)\)", content):
                if raw.startswith(("https://", "http://", "mailto:")):
                    continue
                name, _, anchor = raw.partition("#")
                target = (path.parent / unquote(name)).resolve() if name else path
                with self.subTest(source=relative, link=raw):
                    self.assertTrue(target == ROOT or ROOT in target.parents)
                    self.assertTrue(target.is_file(), raw)
                    if anchor:
                        self.assertIn(unquote(anchor), headings(target.read_text(encoding="utf-8")))

    def test_use_and_install_appear_before_architecture(self) -> None:
        for relative, use, install, architecture in (
            ("README.md", "## Invoke it", "## Install from the public release", "## Architecture:"),
            ("README.zh-CN.md", "## 调用方式", "## 从公开 release 安装", "## 架构图"),
        ):
            content = (ROOT / relative).read_text(encoding="utf-8")
            self.assertLess(content.index(use), content.index(architecture))
            self.assertLess(content.index(install), content.index(architecture))
            self.assertEqual(content.count("```mermaid\n"), 1)

    def test_readme_stable_install_ref_matches_release_authority(self) -> None:
        for relative in PAIRS[0]:
            content = (ROOT / relative).read_text(encoding="utf-8")
            refs = re.findall(r"--ref\s+(v[0-9]+\.[0-9]+\.[0-9]+)", content)
            self.assertEqual(refs, [f"v{PUBLIC_RELEASE_VERSION}"], relative)

    def test_publication_status_is_recorded_after_readback(self) -> None:
        for relative in ("docs/releases/v0.3.0.md", "docs/releases/v0.3.0.zh-CN.md"):
            self.assertIn("PUBLISHED — 2026-09-22", (ROOT / relative).read_text(encoding="utf-8"))
        for relative in PAIRS[4]:
            self.assertIn("PUBLISHED — 2026-09-20", (ROOT / relative).read_text(encoding="utf-8"))
        for relative in PAIRS[3]:
            self.assertIn("PUBLISHED — 2026-09-17", (ROOT / relative).read_text(encoding="utf-8"))
        for relative in PAIRS[2]:
            self.assertIn(
                "COMPLETED — v0.2.0 PUBLISHED",
                (ROOT / relative).read_text(encoding="utf-8"),
            )

    def test_readme_does_not_mix_validation_and_daily_install_commands(self) -> None:
        for relative in PAIRS[0]:
            content = (ROOT / relative).read_text(encoding="utf-8")
            blocks = re.findall(r"```bash\n(.*?)\n```", content, flags=re.S)
            for block in blocks:
                if "scripts/validate_repository.py" in block:
                    self.assertNotIn("scripts/install_skill.py", block)
            self.assertTrue(any("--dest \"$preview_root\"" in block for block in blocks))
            self.assertTrue(any("scripts/install_skill.py --replace" in block for block in blocks))

        for relative in PAIRS[2]:
            content = (ROOT / relative).read_text(encoding="utf-8")
            preview_blocks = [
                block
                for block in re.findall(r"```bash\n(.*?)\n```", content, flags=re.S)
                if "scripts/install_skill.py --dest" in block
            ]
            self.assertEqual(len(preview_blocks), 1, relative)
            self.assertIn("PYTHONDONTWRITEBYTECODE=1", preview_blocks[0], relative)


if __name__ == "__main__":
    unittest.main()
