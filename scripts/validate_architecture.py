#!/usr/bin/env python3
"""Validate the renderer-neutral audit model and paired README Mermaid views."""

from __future__ import annotations

import json
from pathlib import Path
import re
import sys
from typing import Any

from common import ROOT


MODEL_PATH = ROOT / "docs" / "architecture" / "audit-runtime-model.json"
README_PATHS = {
    "en": ROOT / "README.md",
    "zh_cn": ROOT / "README.zh-CN.md",
}

REQUIRED_REGIONS = {
    "R00_PIN",
    "R10_RESOLVE",
    "R20_TRAVERSE",
    "R30_CHALLENGE",
    "R40_DECIDE",
    "R50_EXTERNAL",
}

REQUIRED_NODES = {
    "N00_OWNER_DECISION",
    "N01_START_PIN",
    "N02_READ_ONLY",
    "N10_AUTHORITY",
    "N11_LIVE_SELECTORS",
    "N12_OWNERSHIP_STATE",
    "N20_SOURCE_STATE",
    "N21_DERIVED_ARTIFACT",
    "N22_INSTALLED_IDENTITY",
    "N23_EVIDENCE_GATES",
    "N30_TRACE",
    "N31_FALSE_GREEN",
    "N32_MULTIPLICITY",
    "N33_EXTERNAL_UNKNOWN",
    "N34_SPECIALIST",
    "N40_OUTCOMES",
    "N41_STOPPING",
    "N42_DECISION_OUTPUT",
    "N43_END_REPIN",
    "N50_OBSERVATION_GATE",
    "N51_EXTERNAL_STATE",
}

REQUIRED_STATES = {
    "S00_UNBOUNDED",
    "S10_PINNED_READ_ONLY",
    "S20_TRAVERSING",
    "S30_ADJUDICATING",
    "S40_FIXED_POINT",
    "S50_REPORTED",
}

LOCALES = ("en", "zh_cn")
ALLOWED_EVIDENCE_STATUS = {
    "verified_repository_contract",
    "conditional_observation",
    "unobserved_by_default",
}


def _read_model(errors: list[str]) -> dict[str, Any]:
    if not MODEL_PATH.is_file():
        errors.append("missing architecture model: docs/architecture/audit-runtime-model.json")
        return {}
    try:
        payload = json.loads(MODEL_PATH.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        errors.append(f"architecture model is not valid UTF-8 JSON: {exc}")
        return {}
    if not isinstance(payload, dict):
        errors.append("architecture model root must be an object")
        return {}
    return payload


def _localized_text(value: object, context: str, errors: list[str]) -> None:
    if not isinstance(value, dict):
        errors.append(f"{context} must be a localized object")
        return
    for locale in LOCALES:
        text = value.get(locale)
        if not isinstance(text, str) or not text.strip():
            errors.append(f"{context} is missing non-empty {locale} text")


def _unique_objects(
    payload: dict[str, Any],
    key: str,
    errors: list[str],
) -> tuple[list[dict[str, Any]], set[str]]:
    raw_items = payload.get(key)
    if not isinstance(raw_items, list):
        errors.append(f"{key} must be an array")
        return [], set()

    items: list[dict[str, Any]] = []
    ids: list[str] = []
    for index, item in enumerate(raw_items):
        if not isinstance(item, dict):
            errors.append(f"{key}[{index}] must be an object")
            continue
        item_id = item.get("id")
        if not isinstance(item_id, str) or not item_id:
            errors.append(f"{key}[{index}] is missing an id")
            continue
        items.append(item)
        ids.append(item_id)
    duplicates = sorted({item_id for item_id in ids if ids.count(item_id) > 1})
    if duplicates:
        errors.append(f"{key} contains duplicate ids: {duplicates}")
    return items, set(ids)


def _github_anchor(heading: str) -> str:
    normalized = heading.strip().lower()
    normalized = re.sub(r"[^\w\s-]", "", normalized)
    return re.sub(r"\s", "-", normalized)


def _markdown_anchors(path: Path) -> set[str]:
    anchors: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^#{1,6}\s+(.+?)\s*$", line)
        if match:
            anchors.add(_github_anchor(match.group(1)))
    return anchors


def _validate_source_ref(reference: object, context: str, errors: list[str]) -> None:
    if not isinstance(reference, str) or not reference:
        errors.append(f"{context} has an invalid source reference")
        return
    relative, separator, anchor = reference.partition("#")
    path = ROOT / relative
    if path.is_absolute() and ROOT not in path.parents:
        errors.append(f"{context} source escapes the repository: {reference}")
        return
    if not path.is_file():
        errors.append(f"{context} source file does not exist: {relative}")
        return
    if separator:
        if not anchor:
            errors.append(f"{context} source has an empty anchor: {reference}")
        elif path.suffix.lower() == ".md" and anchor not in _markdown_anchors(path):
            errors.append(f"{context} source anchor does not exist: {reference}")


def _extract_mermaid_block(path: Path, errors: list[str]) -> str:
    relative = path.relative_to(ROOT).as_posix()
    if not path.is_file():
        errors.append(f"missing localized README: {relative}")
        return ""
    content = path.read_text(encoding="utf-8")
    blocks = re.findall(
        r"^```mermaid\s*\n(.*?)^```\s*$",
        content,
        re.MULTILINE | re.DOTALL,
    )
    if len(blocks) != 1:
        errors.append(
            f"{relative} must contain exactly one Mermaid architecture block, got {len(blocks)}"
        )
        return ""
    return blocks[0]


def _normalized_line(value: str) -> str:
    return " ".join(value.strip().split())


def _expected_edge_line(edge: dict[str, Any], locale: str) -> str:
    source = edge["source"]
    target = edge["target"]
    label = edge["label"][locale]
    kind = edge["kind"]
    if kind == "observed":
        return f"{source} -->|{label}| {target}"
    if kind == "conditional":
        return f"{source} -. {label} .-> {target}"
    return f"{source} == {label} ==> {target}"


def _validate_mermaid_readmes(
    model: dict[str, Any],
    region_ids: set[str],
    node_ids: set[str],
    edge_ids: set[str],
    errors: list[str],
) -> None:
    edges = model.get("edges")
    regions = model.get("regions")
    nodes = model.get("nodes")
    layout = model.get("layout_contract")
    question = model.get("primary_question")
    if not all(isinstance(value, list) for value in (edges, regions, nodes)):
        return
    if not isinstance(layout, dict) or not isinstance(question, dict):
        return

    model_edges = {
        edge["id"]: edge
        for edge in edges
        if isinstance(edge, dict) and isinstance(edge.get("id"), str)
    }
    semantic_sets: dict[str, tuple[set[str], set[str], set[str]]] = {}

    for locale, path in README_PATHS.items():
        relative = path.relative_to(ROOT).as_posix()
        source = _extract_mermaid_block(path, errors)
        if not source:
            continue

        first_line = next((line.strip() for line in source.splitlines() if line.strip()), "")
        if first_line != "flowchart TB":
            errors.append(f"{relative} Mermaid diagram must begin with 'flowchart TB'")

        rendered_region_order = re.findall(
            r"^\s*subgraph\s+(R[A-Z0-9_]+)\s*\[", source, re.MULTILINE
        )
        rendered_regions = set(rendered_region_order)
        rendered_nodes = set(
            re.findall(r"^\s*(N[A-Z0-9_]+)\s*(?=[\[\{\(])", source, re.MULTILINE)
        )
        edge_comments = re.findall(
            r"^\s*%%\s+(E[A-Z0-9_]+)\s*$", source, re.MULTILINE
        )
        semantic_edges = set(edge_comments)

        if rendered_regions != region_ids:
            errors.append(
                f"{relative} region IDs differ: expected={sorted(region_ids)} "
                f"actual={sorted(rendered_regions)}"
            )
        if rendered_nodes != node_ids:
            errors.append(
                f"{relative} node IDs differ: expected={sorted(node_ids)} "
                f"actual={sorted(rendered_nodes)}"
            )
        if semantic_edges != edge_ids:
            errors.append(
                f"{relative} semantic edge comments differ: expected={sorted(edge_ids)} "
                f"actual={sorted(semantic_edges)}"
            )
        if len(edge_comments) != len(semantic_edges):
            errors.append(f"{relative} contains duplicate semantic edge comments")
        if rendered_region_order != layout.get("region_order"):
            errors.append(
                f"{relative} region order differs: expected={layout.get('region_order')} "
                f"actual={rendered_region_order}"
            )

        lines = source.splitlines()
        for index, line in enumerate(lines):
            match = re.match(r"^\s*%%\s+(E[A-Z0-9_]+)\s*$", line)
            if not match:
                continue
            edge_id = match.group(1)
            next_index = index + 1
            while next_index < len(lines) and not lines[next_index].strip():
                next_index += 1
            if next_index == len(lines):
                errors.append(f"{relative} edge comment {edge_id} has no Mermaid edge")
                continue
            if edge_id not in model_edges:
                continue
            expected = _expected_edge_line(model_edges[edge_id], locale)
            actual = _normalized_line(lines[next_index])
            if actual != expected:
                errors.append(
                    f"{relative} edge {edge_id} differs: expected={expected!r} actual={actual!r}"
                )

        for region in regions:
            if isinstance(region, dict) and region.get("label", {}).get(locale) not in source:
                errors.append(f"{relative} omits localized region label for {region.get('id')}")
        for node in nodes:
            if isinstance(node, dict) and node.get("label", {}).get(locale) not in source:
                errors.append(f"{relative} omits localized node label for {node.get('id')}")

        raw_readme = path.read_text(encoding="utf-8")
        readme_without_quote_markers = re.sub(r"(?m)^>\s?", "", raw_readme)
        localized_question = question.get(locale)
        if isinstance(localized_question, str):
            compact_readme = re.sub(r"\s+", "", readme_without_quote_markers)
            compact_question = re.sub(r"\s+", "", localized_question)
            if compact_question not in compact_readme:
                errors.append(f"{relative} omits the model's localized reader question")

        forbidden_fragments = (
            "%%{init",
            "classDef",
            "linkStyle",
            "themeVariables",
            "<svg",
            "<image",
            "click ",
        )
        for fragment in forbidden_fragments:
            if fragment in source:
                errors.append(
                    f"{relative} Mermaid source contains forbidden renderer override: {fragment!r}"
                )

        semantic_sets[locale] = (rendered_regions, rendered_nodes, semantic_edges)

    if len(semantic_sets) == len(README_PATHS):
        values = list(semantic_sets.values())
        if values[0] != values[1]:
            errors.append("localized README Mermaid semantic ID sets differ")


def validate_model() -> list[str]:
    errors: list[str] = []
    payload = _read_model(errors)
    if not payload:
        return errors

    if payload.get("schema_version") != 1:
        errors.append("architecture schema_version must equal 1")
    if payload.get("diagram_id") != "audit-runtime":
        errors.append("architecture diagram_id must equal 'audit-runtime'")

    for field in ("artifact_role", "audience", "primary_question", "answer_contract"):
        _localized_text(payload.get(field), field, errors)

    question = payload.get("primary_question")
    if isinstance(question, dict):
        english = question.get("en", "")
        chinese = question.get("zh_cn", "")
        for phrase in ("read-only audit", "owner decision", "repository snapshot", "external"):
            if phrase not in english:
                errors.append(f"primary_question.en lost purpose phrase: {phrase!r}")
        for phrase in ("只读审计", "所有者决策", "仓库快照", "外部"):
            if phrase not in chinese:
                errors.append(f"primary_question.zh_cn lost purpose phrase: {phrase!r}")

    layout = payload.get("layout_contract")
    if not isinstance(layout, dict):
        errors.append("layout_contract must be an object")
    else:
        if layout.get("surface") != "day-first":
            errors.append("architecture must remain day-first")
        if layout.get("renderer") != "mermaid":
            errors.append("architecture renderer must equal 'mermaid'")
        if layout.get("direction") != "TB":
            errors.append("architecture Mermaid direction must equal 'TB'")
        if layout.get("render_sources") != {
            "en": "README.md",
            "zh_cn": "README.zh-CN.md",
        }:
            errors.append("architecture render_sources must bind both localized READMEs")
        if layout.get("region_order") != [
            "R00_PIN",
            "R10_RESOLVE",
            "R20_TRAVERSE",
            "R30_CHALLENGE",
            "R40_DECIDE",
            "R50_EXTERNAL",
        ]:
            errors.append("architecture region_order must retain all six day-first regions")
        if layout.get("external_region") != "R50_EXTERNAL":
            errors.append("external_region must equal R50_EXTERNAL")
        if layout.get("max_connector_meanings") != 3:
            errors.append("max_connector_meanings must equal 3")
        if "renderer defaults" not in layout.get("theme_contract", ""):
            errors.append("theme_contract must preserve renderer-default day/dark adaptation")

    legend = payload.get("connector_legend")
    if not isinstance(legend, list):
        errors.append("connector_legend must be an array")
        connector_kinds: set[str] = set()
    else:
        connector_kinds = {
            item.get("kind")
            for item in legend
            if isinstance(item, dict) and isinstance(item.get("kind"), str)
        }
        if connector_kinds != {"observed", "conditional", "feedback"}:
            errors.append(
                "connector meanings must be exactly observed, conditional, and feedback"
            )
        if len(legend) > 3:
            errors.append("connector_legend exceeds three meanings")
        for index, item in enumerate(legend):
            if isinstance(item, dict):
                _localized_text(item, f"connector_legend[{index}]", errors)

    regions, region_ids = _unique_objects(payload, "regions", errors)
    if region_ids != REQUIRED_REGIONS:
        errors.append(
            "architecture region set differs: "
            f"expected={sorted(REQUIRED_REGIONS)} actual={sorted(region_ids)}"
        )
    for region in regions:
        region_id = region["id"]
        _localized_text(region.get("label"), f"region {region_id} label", errors)
        _localized_text(region.get("purpose"), f"region {region_id} purpose", errors)

    nodes, node_ids = _unique_objects(payload, "nodes", errors)
    if node_ids != REQUIRED_NODES:
        errors.append(
            "architecture node set differs: "
            f"expected={sorted(REQUIRED_NODES)} actual={sorted(node_ids)}"
        )
    for node in nodes:
        node_id = node["id"]
        if node.get("region") not in region_ids:
            errors.append(f"node {node_id} references unknown region: {node.get('region')}")
        if node.get("evidence_status") not in ALLOWED_EVIDENCE_STATUS:
            errors.append(
                f"node {node_id} has unsupported evidence_status: {node.get('evidence_status')}"
            )
        for field in ("label", "responsibility", "limit"):
            _localized_text(node.get(field), f"node {node_id} {field}", errors)
        sources = node.get("sources")
        if not isinstance(sources, list) or not sources:
            errors.append(f"node {node_id} must cite at least one repository authority")
        else:
            for reference in sources:
                _validate_source_ref(reference, f"node {node_id}", errors)

    edges, edge_ids = _unique_objects(payload, "edges", errors)
    if len(edge_ids) < 24:
        errors.append("architecture must retain the complete decision-bearing edge topology")
    for edge in edges:
        edge_id = edge["id"]
        source = edge.get("source")
        target = edge.get("target")
        if source not in node_ids:
            errors.append(f"edge {edge_id} has unknown source: {source}")
        if target not in node_ids:
            errors.append(f"edge {edge_id} has unknown target: {target}")
        if source == target:
            errors.append(f"edge {edge_id} cannot be a self-loop")
        if edge.get("kind") not in connector_kinds:
            errors.append(f"edge {edge_id} has unknown connector kind: {edge.get('kind')}")
        _localized_text(edge.get("label"), f"edge {edge_id} label", errors)

    states, state_ids = _unique_objects(payload, "states", errors)
    if state_ids != REQUIRED_STATES:
        errors.append(
            "architecture state set differs: "
            f"expected={sorted(REQUIRED_STATES)} actual={sorted(state_ids)}"
        )
    for state in states:
        state_id = state["id"]
        _localized_text(state.get("label"), f"state {state_id} label", errors)
        if not isinstance(state.get("invariant"), str) or not state["invariant"].strip():
            errors.append(f"state {state_id} must have an invariant")

    transitions = payload.get("state_transitions")
    if not isinstance(transitions, list) or not transitions:
        errors.append("state_transitions must be a non-empty array")
    else:
        for index, transition in enumerate(transitions):
            if not isinstance(transition, dict):
                errors.append(f"state_transitions[{index}] must be an object")
                continue
            if transition.get("from") not in state_ids:
                errors.append(
                    f"state_transitions[{index}] has unknown from state: {transition.get('from')}"
                )
            if transition.get("to") not in state_ids:
                errors.append(
                    f"state_transitions[{index}] has unknown to state: {transition.get('to')}"
                )
            if not isinstance(transition.get("trigger"), str) or not transition["trigger"].strip():
                errors.append(f"state_transitions[{index}] must have a trigger")

    boundary = payload.get("boundary")
    if not isinstance(boundary, dict):
        errors.append("boundary must be an object")
    else:
        includes = boundary.get("includes")
        excludes = boundary.get("excludes")
        if not isinstance(includes, list) or len(includes) < 5:
            errors.append("boundary.includes must retain the audit's material surfaces")
        if not isinstance(excludes, list) or len(excludes) < 4:
            errors.append("boundary.excludes must keep adjacent reader jobs separate")

    _validate_mermaid_readmes(payload, region_ids, node_ids, edge_ids, errors)
    return errors


def main() -> int:
    errors = validate_model()
    if errors:
        print("Audit architecture contract validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("Audit architecture model, README Mermaid parity, and proof boundaries: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
