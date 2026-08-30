# Audit runtime architecture

[简体中文](README.zh-CN.md)

This directory owns the semantic contract behind the public audit-runtime
architecture. The localized diagrams themselves are native Mermaid blocks in
the two root READMEs. They explain how one read-only audit reaches a
decision-bounded result; they are not a brand banner, an abstract project
concept, or this repository's packaging and release architecture.

## Reader question

> How does one read-only audit turn a concrete owner decision and an exact
> repository snapshot into a decision-bounded answer without crossing
> unobserved external boundaries?

The diagrams answer through six regions:

1. pin the audit object;
2. resolve authority and reachability;
3. traverse distinct evidence layers;
4. challenge and adjudicate material candidates;
5. reach a decision fixed point and report; and
6. keep external state behind an explicit fresh-observation gate.

## Truth surfaces

| Surface | Authority |
| --- | --- |
| [`audit-runtime-model.json`](audit-runtime-model.json) | Renderer-neutral semantic authority: reader question, boundaries, stable IDs, nodes, edges, states, source mapping, and render acceptance |
| [`../../README.md`](../../README.md) | Standalone English Mermaid view |
| [`../../README.zh-CN.md`](../../README.zh-CN.md) | Standalone Simplified Chinese Mermaid view |
| [`../../scripts/validate_architecture.py`](../../scripts/validate_architecture.py) | Model, source-anchor, topology, localization, connector-kind, and README parity validation |

The JSON model owns meaning. Each README owns its locale's concise display
copy and Mermaid syntax. Region, node, and semantic-edge IDs are shared, and
every modeled edge remains visible in both diagrams.

Every internal node maps to current repository authority:

- [`../product-spec.md`](../product-spec.md) owns accepted product behavior;
- [`../evidence-model.md`](../evidence-model.md) owns proof, adjudication, clean,
  unknown, and stopping semantics;
- [`../../skills/repository-operational-truth-audit/SKILL.md`](../../skills/repository-operational-truth-audit/SKILL.md)
  owns runtime workflow and invocation boundaries; and
- [`../../AGENTS.md`](../../AGENTS.md) owns repository, read-only, source/install,
  privacy, and publication boundaries.

The external-state node is `unobserved_by_default`. Repository evidence never
silently proves runtime, edge, device, account, or owner acceptance.

## Connector meanings

The Mermaid views use three shape-level connector meanings that remain visible
without relying on color:

- solid arrow: in-scope, evidence-bearing traversal;
- dotted arrow: optional specialist or explicitly authorized fresh external
  observation; and
- thick return arrow: new decision-relevant evidence reopens traversal.

Passing evidence never upgrades a claim to the next layer. Source, derived
artifact, installed/deployed identity, and external state stay separate.

## Localization and theme contract

English and Simplified Chinese are two independent Mermaid diagrams, not
bilingual text on one canvas. They share region, node, semantic-edge, and
connector-kind parity while allowing locale-specific line breaks.

The diagrams use Mermaid renderer defaults and no hard-coded theme colors.
GitHub can therefore adapt them to day and dark surfaces instead of preserving
a fixed SVG palette or fixed-canvas text scale.

## Edit and validate

Change architecture meaning in `audit-runtime-model.json`, then update both
README Mermaid blocks in the same change. Run:

```bash
python3 scripts/validate_architecture.py
python3 scripts/validate_repository.py
python3 -m unittest tests.test_architecture
```

The validator requires all six regions, all stable nodes, all 30 semantic
edges, exact connector kinds and localized edge labels, model source anchors,
locale parity, top-to-bottom flow, and the visible read-only, external-proof,
and fixed-point feedback boundaries.

The immutable `v0.1.0` release remains historical evidence of the earlier SVG
edition. Current `main` uses the README Mermaid views as the active public
architecture surface.
