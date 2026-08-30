#!/usr/bin/env python3
"""Render the day-first English and Chinese audit-runtime architecture SVGs."""

from __future__ import annotations

import argparse
import hashlib
from html import escape
import json
from pathlib import Path
from typing import Any

from common import ROOT


MODEL_PATH = ROOT / "docs" / "architecture" / "audit-runtime-model.json"
OUTPUTS = {
    "en": ROOT / "docs" / "architecture" / "audit-runtime.en.svg",
    "zh_cn": ROOT / "docs" / "architecture" / "audit-runtime.zh-CN.svg",
}

W = 1600
H = 1080

REGION_LAYOUT = {
    "R00_PIN": (38, 146, 246, 726),
    "R10_RESOLVE": (296, 146, 282, 726),
    "R20_TRAVERSE": (590, 146, 312, 726),
    "R30_CHALLENGE": (914, 146, 374, 726),
    "R40_DECIDE": (1300, 146, 262, 726),
}

NODE_LAYOUT = {
    "N00_OWNER_DECISION": (38, 226, 246, 183),
    "N01_START_PIN": (38, 409, 246, 238),
    "N02_READ_ONLY": (38, 647, 246, 225),
    "N10_AUTHORITY": (296, 226, 282, 203),
    "N11_LIVE_SELECTORS": (296, 429, 282, 226),
    "N12_OWNERSHIP_STATE": (296, 655, 282, 217),
    "N20_SOURCE_STATE": (590, 226, 312, 148),
    "N21_DERIVED_ARTIFACT": (590, 374, 312, 148),
    "N22_INSTALLED_IDENTITY": (590, 522, 312, 148),
    "N23_EVIDENCE_GATES": (590, 670, 312, 202),
    "N30_TRACE": (914, 226, 374, 170),
    "N31_FALSE_GREEN": (914, 396, 374, 132),
    "N32_MULTIPLICITY": (914, 528, 374, 132),
    "N33_EXTERNAL_UNKNOWN": (914, 660, 374, 148),
    "N34_SPECIALIST": (914, 808, 374, 64),
    "N40_OUTCOMES": (1300, 226, 262, 276),
    "N41_STOPPING": (1300, 502, 262, 158),
    "N42_DECISION_OUTPUT": (1300, 660, 262, 143),
    "N43_END_REPIN": (1300, 803, 262, 69),
    "N50_OBSERVATION_GATE": (438, 930, 490, 78),
    "N51_EXTERNAL_STATE": (958, 930, 578, 78),
}

REGION_TAGLINES = {
    "en": {
        "R00_PIN": "decision + exact identity + mutation boundary",
        "R10_RESOLVE": "what owns truth now · what actually selects it",
        "R20_TRAVERSE": "proof layers stay separate",
        "R30_CHALLENGE": "close the trace · test the green · name unknowns",
        "R40_DECIDE": "fixed point + bounded answer",
        "R50_EXTERNAL": "never infer beyond the freshly observed layer",
    },
    "zh_cn": {
        "R00_PIN": "决策 + 精确身份 + mutation boundary",
        "R10_RESOLVE": "谁拥有当前事实 · 什么真正选择它",
        "R20_TRAVERSE": "始终分开各个 proof layer",
        "R30_CHALLENGE": "闭合 trace · 挑战绿灯 · 命名未知",
        "R40_DECIDE": "固定点 + 有边界的答案",
        "R50_EXTERNAL": "绝不推断超出新鲜观察的层",
    },
}

DISPLAY_COPY: dict[str, dict[str, dict[str, list[str]]]] = {
    "en": {
        "N00_OWNER_DECISION": {
            "body": [
                "re-entry · migration · consolidation",
                "safe archive · handoff · release readiness",
            ],
            "limit": ["No decision → bounded reconnaissance, then ask."],
        },
        "N01_START_PIN": {
            "body": [
                "physical root + Git root",
                "branch / HEAD / working tree",
                "upstream / worktree / submodule identity",
            ],
            "limit": ["Pin one exact target — never infer from a sibling checkout."],
        },
        "N02_READ_ONLY": {
            "body": ["observe without mutation", "preserve concurrent work"],
            "limit": ["≠ fix · commit · push · install · deploy · account action"],
        },
        "N10_AUTHORITY": {
            "body": [
                "canonical source / config / durable state",
                "runbooks / generated copies",
                "status / receipts / history",
            ],
            "limit": ["Historical evidence ≠ current authority"],
        },
        "N11_LIVE_SELECTORS": {
            "body": [
                "registrations · metadata · manifests",
                "imports · callers · build pipelines",
                "services · persistence · operator routes",
            ],
            "limit": ["File presence ≠ reachability"],
        },
        "N12_OWNERSHIP_STATE": {
            "body": [
                "selector · owner / purpose · callers",
                "isolated state · version / artifact identity",
                "compatibility or retirement intent",
            ],
            "limit": ["Multiple paths ≠ drift by default"],
        },
        "N20_SOURCE_STATE": {
            "body": ["owns behavior or persistent truth", "for this decision"],
            "limit": ["source ≠ artifact ≠ running instance"],
        },
        "N21_DERIVED_ARTIFACT": {
            "body": ["derivation identity", "source → artifact relation"],
            "limit": ["Green build proves only its artifact"],
        },
        "N22_INSTALLED_IDENTITY": {
            "body": ["fresh exact instance", "only when observed in scope"],
            "limit": ["package / receipt ≠ running instance"],
        },
        "N23_EVIDENCE_GATES": {
            "body": [
                "exact input · exact path",
                "observable assertion · failure sensitivity",
                "proof layer · observed identity",
            ],
            "limit": ["Passing evidence never upgrades the next layer"],
        },
        "N30_TRACE": {
            "body": [
                "claim / live surface",
                "→ mechanism + state",
                "→ contradiction or gap",
                "→ decision impact",
                "→ fresh validation",
            ],
            "limit": ["A disconnected stale file is not a finding."],
        },
        "N31_FALSE_GREEN": {
            "body": [
                "Exact path ran? Assertion observable?",
                "Broken invariant fails? Claimed layer proved?",
            ],
            "limit": ["Disposable mutation only if safe; never the real target."],
        },
        "N32_MULTIPLICITY": {
            "body": [
                "selector · owner · isolated state · version",
                "callers · compatibility / retirement intent",
            ],
            "limit": ["selected + owned + isolated = intentional"],
        },
        "N33_EXTERNAL_UNKNOWN": {
            "body": [
                "missing observation → prevented claim",
                "→ affected decision → exact fresh observation needed",
            ],
            "limit": ["Unavailable external state ≠ repository defect"],
        },
        "N34_SPECIALIST": {
            "body": ["material observation only · no default fan-out"],
            "limit": [],
        },
        "N40_OUTCOMES": {
            "body": [],
            "limit": ["Never collapse these into one score."],
        },
        "N41_STOPPING": {
            "body": [
                "every candidate adjudicated",
                "no new material evidence edge",
                "other surfaces cannot change the answer",
                "external limits are explicit",
            ],
            "limit": ["new material edge → traverse again"],
        },
        "N42_DECISION_OUTPUT": {
            "body": [
                "decision · pin · live topology",
                "full traces · non-findings",
                "proof boundary · checks · overhead",
            ],
            "limit": ["No score · backlog · repair loop"],
        },
        "N43_END_REPIN": {
            "body": ["start ↔ end · mutation statement"],
            "limit": [],
        },
        "N50_OBSERVATION_GATE": {
            "body": ["scope + authorization · exact current named instance"],
            "limit": ["source audit never silently crosses"],
        },
        "N51_EXTERNAL_STATE": {
            "body": ["runtime · edge · device · account · owner acceptance"],
            "limit": ["unobserved = explicit unknown"],
        },
    },
    "zh_cn": {
        "N00_OWNER_DECISION": {
            "body": [
                "重新进入 · 迁移 · 整合",
                "安全归档 · 交接 · 发布准备",
            ],
            "limit": ["没有决策 → 只做有限侦察，然后询问。"],
        },
        "N01_START_PIN": {
            "body": [
                "physical root + Git root",
                "branch / HEAD / working tree",
                "upstream / worktree / submodule identity",
            ],
            "limit": ["钉住一个精确目标，绝不从相邻 checkout 推断。"],
        },
        "N02_READ_ONLY": {
            "body": ["只观察，不 mutation", "保留并行工作"],
            "limit": ["≠ 修复 · commit · push · install · deploy · account action"],
        },
        "N10_AUTHORITY": {
            "body": [
                "canonical source / config / durable state",
                "runbooks / generated copies",
                "status / receipts / history",
            ],
            "limit": ["历史证据 ≠ 当前权威"],
        },
        "N11_LIVE_SELECTORS": {
            "body": [
                "registrations · metadata · manifests",
                "imports · callers · build pipelines",
                "services · persistence · operator routes",
            ],
            "limit": ["文件存在 ≠ 实际可达"],
        },
        "N12_OWNERSHIP_STATE": {
            "body": [
                "selector · owner / purpose · callers",
                "isolated state · version / artifact identity",
                "compatibility 或 retirement intent",
            ],
            "limit": ["多条路径 ≠ 默认发生 drift"],
        },
        "N20_SOURCE_STATE": {
            "body": ["拥有该决策所依赖的", "行为或持久事实"],
            "limit": ["source ≠ artifact ≠ running instance"],
        },
        "N21_DERIVED_ARTIFACT": {
            "body": ["derivation identity", "source → artifact relation"],
            "limit": ["Green build 只证明它的 artifact"],
        },
        "N22_INSTALLED_IDENTITY": {
            "body": ["仅在范围内被观察时", "记录新鲜的精确 instance"],
            "limit": ["package / receipt ≠ running instance"],
        },
        "N23_EVIDENCE_GATES": {
            "body": [
                "exact input · exact path",
                "observable assertion · failure sensitivity",
                "proof layer · observed identity",
            ],
            "limit": ["证据通过不会自动升级到下一层"],
        },
        "N30_TRACE": {
            "body": [
                "claim / live surface",
                "→ mechanism + state",
                "→ contradiction 或 gap",
                "→ decision impact",
                "→ fresh validation",
            ],
            "limit": ["断开的旧文件不是 finding。"],
        },
        "N31_FALSE_GREEN": {
            "body": [
                "exact path 运行？assertion 可观察？",
                "破坏 invariant 会失败？claimed layer 被证明？",
            ],
            "limit": ["Disposable mutation 仅在安全时；绝不动真实目标。"],
        },
        "N32_MULTIPLICITY": {
            "body": [
                "selector · owner · isolated state · version",
                "callers · compatibility / retirement intent",
            ],
            "limit": ["被选择 + 有所有者 + 已隔离 = intentional"],
        },
        "N33_EXTERNAL_UNKNOWN": {
            "body": [
                "missing observation → prevented claim",
                "→ affected decision → 所需的 exact fresh observation",
            ],
            "limit": ["不可得的外部状态 ≠ 仓库缺陷"],
        },
        "N34_SPECIALIST": {
            "body": ["仅限实质观察 · 不做默认 fan-out"],
            "limit": [],
        },
        "N40_OUTCOMES": {
            "body": [],
            "limit": ["绝不把这些压成一个 score。"],
        },
        "N41_STOPPING": {
            "body": [
                "每个候选项均已裁定",
                "没有新的实质证据边",
                "其他表面不能改变答案",
                "外部限制已经明确",
            ],
            "limit": ["新的实质证据边 → 重新穿行"],
        },
        "N42_DECISION_OUTPUT": {
            "body": [
                "决策 · pin · live topology",
                "完整 traces · non-findings",
                "proof boundary · checks · overhead",
            ],
            "limit": ["没有 score · backlog · repair loop"],
        },
        "N43_END_REPIN": {
            "body": ["核对 start ↔ end · mutation 说明"],
            "limit": [],
        },
        "N50_OBSERVATION_GATE": {
            "body": ["范围 + 授权 · 对具名 instance 的精确当前观察"],
            "limit": ["source audit 绝不默默跨越"],
        },
        "N51_EXTERNAL_STATE": {
            "body": ["runtime · edge · device · account · owner acceptance"],
            "limit": ["未观察 = 显式未知"],
        },
    },
}

OUTCOME_COPY = {
    "en": [
        "validated contradiction",
        "false-green evidence",
        "shadow path",
        "intentional multiplicity",
        "non-material residue",
        "decision-critical unknown",
        "external proof boundary",
        "clean within scope",
    ],
    "zh_cn": [
        "已验证矛盾",
        "false-green evidence",
        "shadow path",
        "有意多重模式",
        "非实质残留",
        "决策关键未知",
        "外部证明边界",
        "范围内 clean",
    ],
}

HEADER_COPY = {
    "en": {
        "eyebrow": "LANE 2 / REPOSITORY OPERATIONAL TRUTH",
        "title": "One audit · one decision · one pinned repository truth",
        "question": "How does a read-only audit reach a bounded answer without crossing unobserved external state?",
        "scope": "AUDIT RUNTIME — packaging and release are a separate reader view",
    },
    "zh_cn": {
        "eyebrow": "LANE 2 / 仓库 OPERATIONAL TRUTH",
        "title": "一次审计 · 一个决策 · 一份钉住的仓库事实",
        "question": "只读审计如何抵达有边界的答案，并在未观察的外部状态前停下？",
        "scope": "审计运行时 — packaging 与 release 属于另一张 reader view",
    },
}

DISPLAY_LABEL = {
    "en": {
        "N00_OWNER_DECISION": "Owner decision",
        "N01_START_PIN": "Exact start pin",
        "N02_READ_ONLY": "Read-only boundary",
        "N10_AUTHORITY": "Current authority",
        "N11_LIVE_SELECTORS": "Live selectors",
        "N12_OWNERSHIP_STATE": "Ownership + isolation",
        "N20_SOURCE_STATE": "Source / config / state",
        "N21_DERIVED_ARTIFACT": "Derived artifact",
        "N22_INSTALLED_IDENTITY": "Installed identity",
        "N23_EVIDENCE_GATES": "Evidence gate",
        "N30_TRACE": "Full candidate trace",
        "N31_FALSE_GREEN": "False-green test",
        "N32_MULTIPLICITY": "Multiplicity or shadow path?",
        "N33_EXTERNAL_UNKNOWN": "External unknown",
        "N34_SPECIALIST": "Specialist — only if material",
        "N40_OUTCOMES": "Adjudication register",
        "N41_STOPPING": "Decision fixed-point test",
        "N42_DECISION_OUTPUT": "Decision answer",
        "N43_END_REPIN": "End re-pin",
        "N50_OBSERVATION_GATE": "Fresh observation gate",
        "N51_EXTERNAL_STATE": "Runtime · edge · device · account · owner acceptance",
    },
    "zh_cn": {
        "N00_OWNER_DECISION": "所有者决策",
        "N01_START_PIN": "精确起始钉点",
        "N02_READ_ONLY": "只读边界",
        "N10_AUTHORITY": "当前权威",
        "N11_LIVE_SELECTORS": "实际 selectors",
        "N12_OWNERSHIP_STATE": "所有权与隔离",
        "N20_SOURCE_STATE": "Source / config / state",
        "N21_DERIVED_ARTIFACT": "Derived artifact",
        "N22_INSTALLED_IDENTITY": "Installed identity",
        "N23_EVIDENCE_GATES": "证据 gate",
        "N30_TRACE": "完整候选 trace",
        "N31_FALSE_GREEN": "False-green 测试",
        "N32_MULTIPLICITY": "多重模式还是 shadow path？",
        "N33_EXTERNAL_UNKNOWN": "外部未知",
        "N34_SPECIALIST": "Specialist — 仅在实质相关时",
        "N40_OUTCOMES": "裁定结果簿",
        "N41_STOPPING": "决策固定点测试",
        "N42_DECISION_OUTPUT": "决策答案",
        "N43_END_REPIN": "结束复钉",
        "N50_OBSERVATION_GATE": "新鲜观察 gate",
        "N51_EXTERNAL_STATE": "Runtime · edge · device · account · owner acceptance",
    },
}


def _model() -> dict[str, Any]:
    return json.loads(MODEL_PATH.read_text(encoding="utf-8"))


def _node_map(model: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {node["id"]: node for node in model["nodes"]}


def _region_map(model: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {region["id"]: region for region in model["regions"]}


def _edge_map(model: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {edge["id"]: edge for edge in model["edges"]}


def _tspans(lines: list[str], x: float, y: float, css_class: str, leading: float) -> str:
    if not lines:
        return ""
    return "".join(
        f'<text class="{css_class}" x="{x}" y="{y + index * leading}">{escape(line)}</text>'
        for index, line in enumerate(lines)
    )


def _glyph_width(character: str, font_size: float) -> float:
    if character.isspace():
        return font_size * 0.32
    if ord(character) > 127:
        return font_size * 0.92
    if character in "ilI.,:;|'`":
        return font_size * 0.3
    if character in "mwMW@#%":
        return font_size * 0.86
    if character.isupper():
        return font_size * 0.63
    return font_size * 0.53


def _wrap_one(line: str, max_width: float, font_size: float) -> list[str]:
    if not line:
        return []
    output: list[str] = []
    remaining = line.strip()
    while remaining:
        width = 0.0
        last_break = -1
        cut = len(remaining)
        for index, character in enumerate(remaining):
            width += _glyph_width(character, font_size)
            if character.isspace() or character in "·/→":
                last_break = index + 1
            if width > max_width:
                cut = last_break if last_break > 0 else max(1, index)
                break
        chunk = remaining[:cut].strip()
        if not chunk:
            chunk = remaining[:1]
            cut = 1
        output.append(chunk)
        remaining = remaining[cut:].strip()
    return output


def _wrap_lines(lines: list[str], max_width: float, font_size: float) -> list[str]:
    wrapped: list[str] = []
    for line in lines:
        wrapped.extend(_wrap_one(line, max_width, font_size))
    return wrapped


def _separator(x: float, y: float, width: float) -> str:
    return f'<line class="node-separator" x1="{x + 18}" y1="{y}" x2="{x + width - 18}" y2="{y}"/>'


def _node_section(
    node: dict[str, Any],
    locale: str,
    layout: tuple[int, int, int, int],
    *,
    compact: bool = False,
    external: bool = False,
) -> str:
    x, y, width, height = layout
    copy = DISPLAY_COPY[locale][node["id"]]
    text_width = width - 52
    title_font = 14.2
    body_font = 12.1
    limit_font = 10.1
    title_leading = 16
    body_leading = 16.5 if compact else 18
    limit_leading = 14
    title_lines = _wrap_one(
        DISPLAY_LABEL[locale][node["id"]], text_width, title_font
    )
    body_lines = _wrap_lines(copy["body"], text_width, body_font)
    limit_lines = _wrap_lines(copy["limit"], text_width, limit_font)
    title_y = y + (23 if compact else 30)
    body_y = title_y + 22 + (len(title_lines) - 1) * title_leading
    limit_y = y + height - (13 if compact else 18) - max(0, len(limit_lines) - 1) * limit_leading
    body_bottom = body_y + max(0, len(body_lines) - 1) * body_leading
    if limit_lines and body_bottom > limit_y - 15:
        raise ValueError(
            f"display copy overflow for {locale} {node['id']}: "
            f"body_bottom={body_bottom:.1f} limit_y={limit_y:.1f}"
        )
    if not limit_lines and body_bottom > y + height - 10:
        raise ValueError(
            f"display copy overflow for {locale} {node['id']}: "
            f"body_bottom={body_bottom:.1f} section_bottom={y + height}"
        )
    marker_class = "node-marker external-marker" if external else "node-marker"
    group_class = "node-section external-node" if external else "node-section"
    parts = [
        f'<g id="node-{node["id"]}" data-node-id="{node["id"]}" class="{group_class}">',
        f'<title>{escape(node["label"][locale])}</title>',
        _separator(x, y, width) if not external else "",
        f'<rect class="{marker_class}" x="{x + 18}" y="{title_y - 12}" width="8" height="8" rx="2"/>',
        _tspans(title_lines, x + 34, title_y, "node-title", title_leading),
        _tspans(body_lines, x + 34, body_y, "node-body", body_leading),
    ]
    if copy["limit"]:
        parts.append(
            _tspans(limit_lines, x + 34, limit_y, "node-limit", limit_leading)
        )
    parts.append("</g>")
    return "".join(parts)


def _outcomes_section(
    node: dict[str, Any], locale: str, layout: tuple[int, int, int, int]
) -> str:
    x, y, width, height = layout
    parts = [
        f'<g id="node-{node["id"]}" data-node-id="{node["id"]}" class="node-section outcomes">',
        f'<title>{escape(node["label"][locale])}</title>',
        _separator(x, y, width),
        f'<rect class="node-marker" x="{x + 18}" y="{y + 18}" width="8" height="8" rx="2"/>',
        f'<text class="node-title" x="{x + 34}" y="{y + 30}">{escape(DISPLAY_LABEL[locale][node["id"]])}</text>',
    ]
    chip_y = y + 52
    for index, outcome in enumerate(OUTCOME_COPY[locale]):
        tone = " outcome-clay" if index in {0, 1, 2, 5, 6} else ""
        parts.extend(
            [
                f'<rect class="outcome-chip{tone}" x="{x + 20}" y="{chip_y}" width="{width - 40}" height="22" rx="6"/>',
                f'<text class="outcome-text" x="{x + 31}" y="{chip_y + 15}">{escape(outcome)}</text>',
            ]
        )
        chip_y += 25
    parts.append(
        _tspans(DISPLAY_COPY[locale][node["id"]]["limit"], x + 34, y + height - 16, "node-limit", 15)
    )
    parts.append("</g>")
    return "".join(parts)


def _region_panel(
    region: dict[str, Any],
    locale: str,
    layout: tuple[int, int, int, int],
    fill_class: str,
) -> str:
    x, y, width, height = layout
    return "".join(
        [
            f'<g id="region-{region["id"]}" data-region-id="{region["id"]}">',
            f'<title>{escape(region["label"][locale])}</title>',
            f'<rect class="region-panel {fill_class}" x="{x}" y="{y}" width="{width}" height="{height}" rx="14"/>',
            f'<line class="region-rule" x1="{x}" y1="{y + 70}" x2="{x + width}" y2="{y + 70}"/>',
            f'<text class="region-index" x="{x + 18}" y="{y + 28}">{escape(region["index"])}</text>',
            f'<text class="region-title" x="{x + 52}" y="{y + 30}">{escape(region["label"][locale])}</text>',
            f'<text class="region-tagline" x="{x + 18}" y="{y + 55}">{escape(REGION_TAGLINES[locale][region["id"]])}</text>',
            "</g>",
        ]
    )


def _edge_group(edge_id: str, path: str, kind: str, label: str | None = None) -> str:
    label_markup = ""
    if label:
        label_markup = f'<title>{escape(label)}</title>'
    return (
        f'<g id="edge-{edge_id}" data-edge-id="{edge_id}" class="edge-group">'
        f"{label_markup}<path class=\"edge edge-{kind}\" d=\"{path}\" "
        f'marker-end="url(#arrow-{kind})"/></g>'
    )


def _local_spines() -> str:
    spans = {
        "R00": (66, 261, 842, [285, 445, 681]),
        "R10": (324, 261, 842, [285, 465, 691]),
        "R20": (618, 261, 842, [285, 409, 557, 705]),
        "R30": (942, 261, 842, [285, 431, 563, 695, 833]),
        "R40": (1328, 261, 842, [285, 537, 695, 832]),
    }
    parts: list[str] = []
    for lane_id, (x, y1, y2, dots) in spans.items():
        parts.append(f'<g class="local-spine" id="spine-{lane_id}">')
        parts.append(f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}"/>')
        for dot_y in dots:
            parts.append(f'<circle cx="{x}" cy="{dot_y}" r="4"/>')
        parts.append("</g>")
    return "".join(parts)


def _semantic_edge_metadata(model: dict[str, Any], locale: str) -> str:
    """Retain every model edge as accessible metadata without adding visual clutter."""

    parts = ['<g id="semantic-edge-index" aria-label="Semantic edge index">']
    for edge in model["edges"]:
        parts.append(
            f'<desc data-semantic-edge-id="{edge["id"]}">'
            f'{escape(edge["source"])} → {escape(edge["target"])}: '
            f'{escape(edge["label"][locale])}</desc>'
        )
    parts.append("</g>")
    return "".join(parts)


def _render(locale: str, model: dict[str, Any]) -> str:
    nodes = _node_map(model)
    regions = _region_map(model)
    edges = _edge_map(model)
    header = HEADER_COPY[locale]
    model_digest = hashlib.sha256(MODEL_PATH.read_bytes()).hexdigest()
    language = "en" if locale == "en" else "zh-CN"
    title_id = f"audit-runtime-title-{language}"
    desc_id = f"audit-runtime-desc-{language}"

    parts: list[str] = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="{title_id} {desc_id}" lang="{language}">',
        f'<title id="{title_id}">{escape(header["title"])}</title>',
        f'<desc id="{desc_id}">{escape(model["primary_question"][locale])} {escape(model["answer_contract"][locale])}</desc>',
        f'<metadata>{{"diagram_id":"audit-runtime","locale":"{language}","model_sha256":"{model_digest}","surface":"day-first"}}</metadata>',
        """<defs>
          <marker id="arrow-observed" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#0F6B63"/></marker>
          <marker id="arrow-conditional" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#B5663F"/></marker>
          <marker id="arrow-feedback" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#527B73"/></marker>
          <style>
            .paper { fill: #F3F0E8; }
            .paper-line { stroke: #DCD8CD; stroke-width: 1; }
            text { font-family: Inter, "SF Pro Text", "PingFang SC", "Noto Sans CJK SC", Arial, sans-serif; fill: #18302F; }
            .eyebrow { font-size: 11px; font-weight: 750; letter-spacing: 1.8px; fill: #0F6B63; }
            .main-title { font-size: 27px; font-weight: 700; letter-spacing: -0.35px; }
            .question { font-size: 14px; font-weight: 440; fill: #53645F; }
            .scope-note { font-size: 9.5px; font-weight: 650; letter-spacing: .7px; fill: #7A857F; }
            .legend-text { font-size: 10.5px; fill: #596A65; }
            .region-panel { stroke: #C8D1CA; stroke-width: 1.2; }
            .region-a { fill: #FFFDF8; }
            .region-b { fill: #F7F9F3; }
            .region-c { fill: #EDF5F0; }
            .region-d { fill: #FAF7F0; }
            .region-e { fill: #FFFDF9; }
            .region-rule { stroke: #BCC9C1; stroke-width: 1; }
            .region-index { font-size: 11px; font-weight: 800; letter-spacing: 1px; fill: #0F6B63; }
            .region-title { font-size: 16.5px; font-weight: 720; letter-spacing: -0.15px; }
            .region-tagline { font-size: 10.2px; font-weight: 500; fill: #6A7873; }
            .node-separator { stroke: #D2D8D3; stroke-width: 1; }
            .node-marker { fill: #0F6B63; }
            .external-marker { fill: #B5663F; }
            .node-title { font-size: 14.2px; font-weight: 720; }
            .node-body { font-size: 12.1px; font-weight: 470; fill: #334B48; }
            .node-limit { font-size: 10.1px; font-weight: 620; fill: #A55836; }
            .outcome-chip { fill: #E7F0EB; stroke: #CBDDD3; stroke-width: .7; }
            .outcome-clay { fill: #F4E7DC; stroke: #E4C9B7; }
            .outcome-text { font-size: 10.3px; font-weight: 580; }
            .edge { fill: none; stroke-linecap: round; stroke-linejoin: round; }
            .edge-observed { stroke: #0F6B63; stroke-width: 2.2; }
            .edge-conditional { stroke: #B5663F; stroke-width: 2; stroke-dasharray: 7 6; }
            .edge-feedback { stroke: #527B73; stroke-width: 1.8; stroke-dasharray: 3 5; }
            .edge-label { font-size: 10px; font-weight: 650; fill: #527B73; }
            .edge-label-clay { font-size: 10px; font-weight: 650; fill: #A55836; }
            .edge-label-bg { fill: #F3F0E8; }
            .local-spine line { stroke: #B8CEC4; stroke-width: 1.3; }
            .local-spine circle { fill: #F9FCF9; stroke: #0F6B63; stroke-width: 1.2; }
            .external-band { fill: #FBF1E8; stroke: #C7825F; stroke-width: 1.35; stroke-dasharray: 8 6; }
            .external-kicker { font-size: 10px; font-weight: 800; letter-spacing: 1.4px; fill: #A55836; }
            .external-title { font-size: 16px; font-weight: 720; }
            .external-tagline { font-size: 10.5px; fill: #80695D; }
            .external-divider { stroke: #DAB49E; stroke-width: 1; }
            .footer { font-size: 9.5px; fill: #71807A; }
          </style>
        </defs>""",
        '<rect class="paper" width="1600" height="1080"/>',
        '<line class="paper-line" x1="38" y1="126" x2="1562" y2="126"/>',
        f'<text class="eyebrow" x="38" y="30">{escape(header["eyebrow"])}</text>',
        f'<text class="main-title" x="38" y="64">{escape(header["title"])}</text>',
        f'<text class="question" x="38" y="90">{escape(header["question"])}</text>',
        f'<text class="scope-note" x="38" y="112">{escape(header["scope"])}</text>',
    ]

    # Compact connector legend in the header; it explains meaning rather than decorating.
    legend_x = 1122
    legend_y = 34
    legend = model["connector_legend"]
    for index, item in enumerate(legend):
        y = legend_y + index * 24
        dash = ' stroke-dasharray="7 6"' if item["kind"] == "conditional" else (' stroke-dasharray="3 5"' if item["kind"] == "feedback" else "")
        color = "#B5663F" if item["kind"] == "conditional" else ("#527B73" if item["kind"] == "feedback" else "#0F6B63")
        parts.append(f'<line x1="{legend_x}" y1="{y}" x2="{legend_x + 34}" y2="{y}" stroke="{color}" stroke-width="2"{dash}/>' )
        parts.append(f'<text class="legend-text" x="{legend_x + 44}" y="{y + 4}">{escape(item[locale])}</text>')

    fills = ["region-a", "region-b", "region-c", "region-d", "region-e"]
    for region_id, fill in zip(model["layout_contract"]["region_order"], fills):
        parts.append(_region_panel(regions[region_id], locale, REGION_LAYOUT[region_id], fill))

    # Region-to-region truth spine. Detailed semantics remain in the model and local node spines.
    for edge_id, x1, x2 in (
        ("E03_PIN_TO_AUTHORITY", 284, 296),
        ("E06_OWNERSHIP_TO_SOURCE", 578, 590),
        ("E14_GATES_TO_TRACE", 902, 914),
        ("E23_TRACE_TO_OUTCOMES", 1288, 1300),
    ):
        parts.append(_edge_group(edge_id, f"M {x1} 181 L {x2} 181", "observed"))

    parts.append(_local_spines())

    for node_id, layout in NODE_LAYOUT.items():
        if node_id in {"N50_OBSERVATION_GATE", "N51_EXTERNAL_STATE"}:
            continue
        node = nodes[node_id]
        if node_id == "N40_OUTCOMES":
            parts.append(_outcomes_section(node, locale, layout))
        else:
            parts.append(
                _node_section(
                    node,
                    locale,
                    layout,
                    compact=node_id in {"N34_SPECIALIST", "N43_END_REPIN"},
                )
            )

    # Visible causal loops that materially change audit behavior.
    feedback_label = edges["E28_STOP_FEEDBACK"]["label"][locale]
    parts.append(
        _edge_group(
            "E28_STOP_FEEDBACK",
            "M 1562 580 L 1576 580 L 1576 132 L 438 132 L 438 146",
            "feedback",
            feedback_label,
        )
    )
    parts.append('<rect class="edge-label-bg" x="760" y="126" width="210" height="18" rx="9"/>')
    parts.append(f'<text class="edge-label" x="770" y="139">{escape(feedback_label)}</text>')

    # Explicit external proof boundary.
    ext_region = regions["R50_EXTERNAL"]
    parts.extend(
        [
            '<g id="region-R50_EXTERNAL" data-region-id="R50_EXTERNAL">',
            f'<title>{escape(ext_region["label"][locale])}</title>',
            '<rect class="external-band" x="38" y="906" width="1524" height="120" rx="14"/>',
            '<line class="external-divider" x1="408" y1="922" x2="408" y2="1010"/>',
            f'<text class="external-kicker" x="58" y="935">{escape(ext_region["index"])}</text>',
            f'<text class="external-title" x="58" y="963">{escape(ext_region["label"][locale])}</text>',
            f'<text class="external-tagline" x="58" y="988">{escape(REGION_TAGLINES[locale]["R50_EXTERNAL"])}</text>',
            '</g>',
            _node_section(nodes["N50_OBSERVATION_GATE"], locale, NODE_LAYOUT["N50_OBSERVATION_GATE"], compact=True, external=True),
            _node_section(nodes["N51_EXTERNAL_STATE"], locale, NODE_LAYOUT["N51_EXTERNAL_STATE"], compact=True, external=True),
        ]
    )

    parts.append(
        _edge_group(
            "E20_UNKNOWN_TO_GATE",
            "M 1104 808 C 1104 880 760 884 700 930",
            "conditional",
            nodes["N50_OBSERVATION_GATE"]["label"][locale],
        )
    )
    parts.append(
        _edge_group(
            "E21_GATE_TO_EXTERNAL",
            "M 928 970 L 958 970",
            "conditional",
        )
    )
    parts.append(
        _edge_group(
            "E22_EXTERNAL_TO_TRACE",
            "M 1238 930 C 1288 884 1294 720 1294 314 L 1288 314",
            "conditional",
        )
    )
    parts.append(
        f'<text class="edge-label-clay" x="734" y="894">{escape(edges["E20_UNKNOWN_TO_GATE"]["label"][locale])}</text>'
    )

    # The model contains all 30 exact edges; the canvas intentionally shows a
    # causally legible subset and indexes the remainder for accessible parity.
    parts.append(_semantic_edge_metadata(model, locale))
    parts.append(
        f'<text class="footer" x="38" y="1055">MODEL audit-runtime · {escape(language)} · source → artifact → installed identity → external observation remain distinct</text>'
    )
    parts.append(
        '<text class="footer" x="1562" y="1055" text-anchor="end">read-only by default · fixed-point stopping · no inferred external claims</text>'
    )
    parts.append("</svg>\n")
    return "".join(parts)


def render_all() -> None:
    model = _model()
    for locale, path in OUTPUTS.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(_render(locale, model), encoding="utf-8")


def check_all() -> list[str]:
    model = _model()
    errors: list[str] = []
    for locale, path in OUTPUTS.items():
        relative = path.relative_to(ROOT)
        if not path.is_file():
            errors.append(f"missing rendered architecture: {relative}")
            continue
        expected = _render(locale, model)
        actual = path.read_text(encoding="utf-8")
        if actual != expected:
            errors.append(f"rendered architecture is stale: {relative}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Verify tracked SVGs match the model and renderer without writing files.",
    )
    args = parser.parse_args()
    if args.check:
        errors = check_all()
        if errors:
            for error in errors:
                print(f"ERROR: {error}")
            return 1
        print("Rendered English and Chinese architecture SVGs are current: PASS")
        return 0

    render_all()
    for locale, path in OUTPUTS.items():
        print(f"rendered {locale}: {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
