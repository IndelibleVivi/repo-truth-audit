# Audit runtime architecture

[简体中文](README.zh-CN.md)

This directory owns the public architecture view for the audit runtime
contract. It is an explanatory model of how one read-only audit reaches a
decision-bounded result; it is not a brand banner, an abstract project concept,
or the packaging and release architecture of this repository.

## Reader question

> How does one read-only audit turn a concrete owner decision and an exact
> repository snapshot into a decision-bounded answer without crossing
> unobserved external boundaries?

The diagram answers by showing six regions:

1. pin the audit object;
2. resolve authority and reachability;
3. traverse distinct evidence layers;
4. challenge and adjudicate material candidates;
5. reach a decision fixed point and report; and
6. keep external state behind an explicit fresh-observation gate.

## Files

| File | Role |
| --- | --- |
| `audit-runtime-model.json` | Renderer-neutral semantic authority: audience, question, boundary, nodes, edges, states, source mapping, and render acceptance |
| `audit-runtime.en.svg` | Standalone day-first English edition |
| `audit-runtime.zh-CN.svg` | Standalone day-first Simplified Chinese edition |
| `../../scripts/render_architecture_svg.py` | Deterministic visual composition and locale-specific line breaking |
| `../../scripts/validate_architecture.py` | Model, source-anchor, topology, localization, SVG-ID, accessibility, and render-drift validation |

The JSON model owns meaning. The renderer owns fixed geometry and condensed
display copy. The two SVGs are generated artifacts checked into the repository
so GitHub and offline readers can display them without a build step.

## Truth sources

Every internal node maps to current repository authority:

- [`../product-spec.md`](../product-spec.md) owns accepted product behavior;
- [`../evidence-model.md`](../evidence-model.md) owns proof, adjudication, clean,
  unknown, and stopping semantics;
- [`../../skills/repository-operational-truth-audit/SKILL.md`](../../skills/repository-operational-truth-audit/SKILL.md)
  owns runtime workflow and invocation boundaries; and
- [`../../AGENTS.md`](../../AGENTS.md) owns repository, read-only, source/install,
  privacy, and publication boundaries.

The external-state node is explicitly `unobserved_by_default`. The diagram does
not claim that a runtime, edge, device, account, or owner-acceptance surface has
been observed merely because repository evidence exists.

## Connector meanings

The visual uses exactly three connector meanings:

- solid teal: in-scope, evidence-bearing traversal;
- dashed clay: an optional specialist or explicitly authorized fresh external
  observation; and
- dotted teal return: a new decision-relevant evidence edge reopens traversal.

Passing evidence never upgrades a claim to the next layer. Source, derived
artifact, installed/deployed identity, and external state remain separate.

## Localization contract

English and Simplified Chinese are separate SVG artifacts, not bilingual text
on one canvas. They share region, node, and semantic-edge IDs while allowing
locale-specific labels and line breaks. The renderer-neutral model contains
both language editions of all semantic labels, responsibilities, limits, edge
labels, state labels, and the primary reader question.

## Render and validate

Regenerate both artifacts after changing the model or renderer:

```bash
python3 scripts/render_architecture_svg.py
```

Then run:

```bash
python3 scripts/validate_architecture.py
python3 scripts/render_architecture_svg.py --check
```

The validator requires stable topology, valid repository source anchors,
three connector meanings, exact locale parity, direct accessible title and
description elements, a day-first surface, current model digests, and the
visible decision-bearing feedback and proof-boundary edges.

The SVGs contain no scripts, network dependencies, embedded raster images, or
`foreignObject` content. They remain ordinary standalone SVG files.
