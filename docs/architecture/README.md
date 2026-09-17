# Audit / Plan / Operate runtime architecture

[简体中文](README.zh-CN.md)

This directory owns the semantic and presentation contract behind the public
Repo Truth Audit architecture. Each root README first embeds a localized,
reader-first SVG overview, then retains a visible native Mermaid map with
the complete modeled topology. Together they explain how one evidence-led
engagement stops at Audit or Plan, or crosses an explicit implementation gate
and reaches verified Operate completion. They do not depict this repository's
packaging or release pipeline.

## Reader question

> How does Repo Truth Audit turn an exact repository snapshot and a concrete
> owner intent into a bounded read-only answer, a decision-ready plan, or an
> authorized structural change with verified completion without overclaiming
> evidence or external state?

The reader overview compresses the answer into the owner question, pinned
operational reality, terminal boundary, three mode outcomes, Operate acceptance,
checkpoint/completion split, and external proof boundary. The complete Mermaid
maps preserve all seven regions:

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
| [`repo-truth-audit-overview.en.svg`](repo-truth-audit-overview.en.svg) and [`repo-truth-audit-overview.zh-CN.svg`](repo-truth-audit-overview.zh-CN.svg) | Paired day-first reader maps: intentionally compressed presentation, not a second semantic authority |
| [`../../README.md`](../../README.md) | English overview embed, plain-language B/S/D/U key, and complete Mermaid view |
| [`../../README.zh-CN.md`](../../README.zh-CN.md) | Simplified Chinese overview embed, plain-language B/S/D/U key, and complete Mermaid view |
| [`../../scripts/validate_architecture.py`](../../scripts/validate_architecture.py) | Model, source-anchor, full Mermaid topology, connector-kind, SVG accessibility/safety, embed order, and locale-parity validation |

The JSON model owns meaning. The SVG pair is a maintained editorial projection:
it may compress routine topology but cannot change a mode, gate, proof boundary,
or completion claim. Each README owns its locale's concise prose and Mermaid
syntax. Region, node, and semantic-edge IDs are shared by the full maps, and
every modeled edge remains visible in both Mermaid editions.

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

## Detailed-map connector meanings

The Mermaid views use three shape-level connector meanings visible without
color:

- solid arrow: in-scope evidence or implementation flow;
- dotted arrow: conditional authority, specialist, or fresh external observation;
- thick return arrow: new evidence reopens diagnosis or the next increment.

Passing evidence never upgrades a claim to the next proof layer. A verified
checkpoint never becomes whole-goal completion while applicable Behavior,
Structure, Delivery, or Usefulness obligations remain.

## Localization and theme contract

English and Simplified Chinese use separate SVG and Mermaid editions, not
bilingual text on one canvas. The SVGs share semantic group IDs while allowing
locale-specific type metrics and line breaks. The Mermaid maps share region,
node, semantic-edge, and connector-kind parity.

The accepted SVG overview is deliberately day-first and includes its own warm
paper background for stable rendering. The detailed maps use Mermaid renderer
defaults and no hard-coded theme colors so GitHub can adapt them to day and dark
surfaces.

## Edit and validate

Change meaning in `audit-runtime-model.json`, then update both README Mermaid
blocks in the same change. If that meaning is visible in the compressed reader
map, update both SVG editions as well. Run:

```bash
python3 scripts/validate_architecture.py
python3 scripts/validate_repository.py
python3 -m unittest tests.test_architecture
```

The validator requires all seven regions, all stable nodes, all 46 semantic
edges, exact connector kinds and localized edge labels, model source anchors,
locale parity, top-to-bottom flow, the read-only diagnosis boundary, the
explicit Operate gate, checkpoint/recovery feedback, whole-goal acceptance, and
the external proof boundary. It also requires accessible, standalone localized
SVGs with matching semantic groups and the correct overview-before-detail embed
order in both READMEs.

The immutable `v0.1.0` release remains historical evidence of the earlier
audit-only architecture. Released `v0.2.0` uses the paired reader overviews and
default-visible complete README Mermaid views.
