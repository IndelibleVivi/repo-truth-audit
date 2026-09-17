from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_architecture import (  # noqa: E402
    MODEL_PATH,
    OVERVIEW_PATHS,
    README_PATHS,
    REQUIRED_NODES,
    REQUIRED_REGIONS,
    validate_model,
)


class ArchitectureContractTests(unittest.TestCase):
    def test_architecture_model_is_valid(self) -> None:
        self.assertEqual(validate_model(), [])

    def test_every_required_node_is_renderable_in_both_locales(self) -> None:
        payload = json.loads(MODEL_PATH.read_text(encoding="utf-8"))
        nodes = {node["id"]: node for node in payload["nodes"]}
        self.assertEqual(set(nodes), REQUIRED_NODES)
        for node in nodes.values():
            for field in ("label", "responsibility", "limit"):
                self.assertTrue(node[field]["en"].strip())
                self.assertTrue(node[field]["zh_cn"].strip())

    def test_regions_cover_every_node_once(self) -> None:
        payload = json.loads(MODEL_PATH.read_text(encoding="utf-8"))
        region_ids = {region["id"] for region in payload["regions"]}
        self.assertEqual(region_ids, REQUIRED_REGIONS)
        self.assertTrue(all(node["region"] in region_ids for node in payload["nodes"]))

    def test_external_state_is_unobserved_by_default(self) -> None:
        payload = json.loads(MODEL_PATH.read_text(encoding="utf-8"))
        nodes = {node["id"]: node for node in payload["nodes"]}
        self.assertEqual(
            nodes["N51_EXTERNAL_STATE"]["evidence_status"],
            "unobserved_by_default",
        )
        self.assertEqual(
            nodes["N50_OBSERVATION_GATE"]["evidence_status"],
            "conditional_observation",
        )

    def test_each_locale_has_one_native_mermaid_view(self) -> None:
        for locale, path in README_PATHS.items():
            source = path.read_text(encoding="utf-8")
            self.assertEqual(source.count("```mermaid"), 1)
            self.assertEqual(source.count("flowchart TB"), 1)
            self.assertNotIn("audit-runtime.en.svg", source)
            self.assertNotIn("audit-runtime.zh-CN.svg", source)
            overview = OVERVIEW_PATHS[locale].relative_to(ROOT).as_posix()
            embed = f"]({overview})"
            self.assertEqual(source.count(embed), 1)
            self.assertLess(source.index(embed), source.index("```mermaid"))


if __name__ == "__main__":
    unittest.main()
