# Audit / Plan / Operate runtime architecture

[简体中文](README.zh-CN.md)

This directory owns the semantic contract behind the public Repo Truth Audit
architecture. The localized diagrams are native Mermaid blocks in the two root
READMEs. They explain how one evidence-led engagement stops at Audit or Plan, or
crosses an explicit implementation gate and reaches verified Operate completion.
They do not depict this repository's packaging or release pipeline.

## Reader question

> How does Repo Truth Audit turn an exact repository snapshot and a concrete
> owner intent into a bounded read-only answer, a decision-ready plan, or an
> authorized structural change with verified completion without overclaiming
> evidence or external state?

The diagrams answer through seven regions:

1. pin owner intent, requested terminal boundary, and repository identity;
2. resolve current authority and reachability;
3. traverse distinct evidence layers;
4. challenge and adjudicate material candidates;
5. close Audit or Plan without target mutation;
6. when explicitly authorized, establish protected witnesses and iterate from
   coherent increments through checkpoints/recovery to whole-goal acceptance;
7. keep external state behind an explicit fresh-observation gate.

## Truth surfaces

| Surface | Authority |
| --- | --- |
| [`audit-runtime-model.json`](audit-runtime-model.json) | Renderer-neutral semantic authority: reader question, boundaries, stable IDs, nodes, edges, states, source mapping, and render acceptance |
| [`../../README.md`](../../README.md) | Standalone English Mermaid view |
| [`../../README.zh-CN.md`](../../README.zh-CN.md) | Standalone Simplified Chinese Mermaid view |
| [`../../scripts/validate_architecture.py`](../../scripts/validate_architecture.py) | Model, source-anchor, topology, localization, connector-kind, and README parity validation |

The JSON model owns meaning. Each README owns its locale's concise display copy
and Mermaid syntax. Region, node, and semantic-edge IDs are shared, and every
modeled edge remains visible in both diagrams.

Every internal node maps to current repository authority:

- [`../product-spec.md`](../product-spec.md) owns Audit / Plan / Operate behavior,
  effect authority, acceptance, and terminal results;
- [`../evidence-model.md`](../evidence-model.md) owns proof, adjudication,
  checkpoints, completion, recovery, and stopping semantics;
- [`../../skills/repository-operational-truth-audit/`](../../skills/repository-operational-truth-audit/)
  owns the runtime router and progressive Audit, Operation, and Recovery methods;
- [`../../AGENTS.md`](../../AGENTS.md) owns canonical source, write, install,
  privacy, and publication boundaries.

The external-state node remains `unobserved_by_default`. Repository evidence
never silently proves runtime, edge, device, account, or owner acceptance.

## Connector meanings

The Mermaid views use three shape-level connector meanings visible without
color:

- solid arrow: in-scope evidence or implementation flow;
- dotted arrow: conditional authority, specialist, or fresh external observation;
- thick return arrow: new evidence reopens diagnosis or the next increment.

Passing evidence never upgrades a claim to the next proof layer. A verified
checkpoint never becomes whole-goal completion while applicable Behavior,
Structure, Delivery, or Usefulness obligations remain.

## Localization and theme contract

English and Simplified Chinese are independent Mermaid diagrams, not bilingual
text on one canvas. They share region, node, semantic-edge, and connector-kind
parity while allowing locale-specific line breaks.

The diagrams use Mermaid renderer defaults and no hard-coded theme colors so
GitHub can adapt them to day and dark surfaces.

## Edit and validate

Change meaning in `audit-runtime-model.json`, then update both README Mermaid
blocks in the same change. Run:

```bash
python3 scripts/validate_architecture.py
python3 scripts/validate_repository.py
python3 -m unittest tests.test_architecture
```

The validator requires all seven regions, all stable nodes, all 46 semantic
edges, exact connector kinds and localized edge labels, model source anchors,
locale parity, top-to-bottom flow, the read-only diagnosis boundary, the
explicit Operate gate, checkpoint/recovery feedback, whole-goal acceptance, and
the external proof boundary.

The immutable `v0.1.0` release remains historical evidence of the earlier
audit-only architecture. Current `main` uses the expanded README Mermaid views
for the unreleased 0.2.0 source candidate.
