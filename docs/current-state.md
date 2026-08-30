# Current state

[简体中文](current-state.zh-CN.md)

Last reconciled: 2026-08-30

## Product

- Product form: standalone public repository and standalone Codex Skill.
- Version: public release `v0.1.0`; current `main` contains an unreleased
  architecture-presentation correction and does not retag that release.
- Scope: complete topology-first, decision-bounded, read-only audit contract.
- Canonical Skill: `skills/repository-operational-truth-audit/`.
- Public documentation: separate English and Simplified Chinese editions.
- Architecture on current `main`: one renderer-neutral semantic model plus one
  native Mermaid diagram in each localized README. Both diagrams retain six
  regions, 21 stable nodes, 30 semantic edges, exact connector-kind parity,
  and explicit read-only, external-proof, and fixed-point boundaries.
- Historical release architecture: immutable `v0.1.0` contains the earlier
  localized SVG pair and deterministic renderer. Those tagged bytes remain
  release evidence; the generated SVGs and renderer are retired from current
  source rather than maintained as a parallel active path.
- Softpowers relationship: optional companion/reference only; no generation,
  bundling, installation, or version ownership.

## Gates

- Current source: the localized README Mermaid blocks are the active public
  architecture views; `docs/architecture/audit-runtime-model.json` remains the
  semantic authority. Architecture docs, product spec, AGENTS, licensing map,
  changelog, validators, tests, and CI commands are reconciled to that split.
- Deterministic validation: local PASS on 2026-08-30 — architecture model,
  source anchors, exact Mermaid topology, localized edge labels,
  connector-kind and locale parity, repository/publication validation, 15 unit
  tests, six fixture truth checks, fixture self-test, system Skill quick
  validation, and Git whitespace validation.
- Mermaid render acceptance: PASS on 2026-08-30 for public `main` architecture
  commit `9805fa52f35a3635ee66e3f651ca891de4baad23`. GitHub rendered both localized
  blocks in light mode; all read-only, external-proof, fixed-point, and end
  re-pin boundaries were present, and the Chinese rendered surface exposed all
  30 localized edge labels. The native viewer supplied zoom and pan controls.
  Default fit remains compact because the complete topology is dense; this is
  not represented as large-text acceptance without using the native viewer.
- Independent forward behavior: PASS on 2026-08-30. An artifact-split case
  reached the stale distributed entrypoint and false-green source test; a clean
  control treated stable/development selection as intentional multiplicity.
- Git release identity: canonical `0.1.0` Skill bytes entered at
  `e15dbabc84d3cae35c40dd9a0a87343fd57981d2`. Annotated tag object
  `235be6e839a87867b7a0758b47ce577c66380111` peels to release commit
  `0180e4c23413a0691f4e895a0d64d7efaa0a12bb`. The tag remains immutable.
- Local install: PASS for `v0.1.0`. Canonical and installed Skill digests both
  equal `30d7ed369fad578c12d83291a17edaad4ad8c3195b2b7b31294c48ecf7ebe69e`.
  The Mermaid correction does not change Skill package bytes, so it does not
  create a new install or next-turn discovery claim.
- Next-turn Codex discovery: not observed.
- Current-main CI: PASS. Actions run `33299095186` passed all four Ubuntu/macOS
  and Python 3.10/3.13 jobs for architecture commit `9805fa52...`. Release run
  `33295744677` separately passed the same matrix on the peeled `v0.1.0`
  release commit. Workflow source and live CI remain separate facts.
- Release publication: PASS. GitHub Release `v0.1.0` was published on
  2026-08-30 and is neither draft nor prerelease. Anonymous tagged read-back,
  disposable public-tag installation, Skill validation, digest equality, and
  pinned SUL text were verified. No new release is implied by the current
  README architecture correction.
- Current-main publication: PASS for architecture commit `9805fa52...`.
  `origin/main`, the repository root README, and the standalone Chinese README
  exposed the Mermaid correction. A later status-only reconciliation may move
  `main` without changing that architecture identity.
- Licensing: functional materials are source-available under SUL-1.0;
  standalone documentation, the renderer-neutral architecture model, and the
  Mermaid diagrams embedded in the README files are under CC BY-NC-SA 4.0
  according to `LICENSING.md`. GitHub reports the layered repository license as
  `Other`; the path map, not a single-license badge, is authoritative.

Replace superseded status here; do not append a development diary.
