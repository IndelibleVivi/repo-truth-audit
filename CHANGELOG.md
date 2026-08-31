# Changelog

[简体中文](CHANGELOG.zh-CN.md)

## Unreleased

- Made ordinary Windows source checkouts deterministic by preserving LF for
  tracked text files and sorting Skill digest entries by normalized POSIX
  relative path, with regression coverage for both boundaries.
- Adopted **Repo Truth Audit** as the human-facing display name and
  `repo-truth-audit` as the public repository slug while preserving the formal
  product name and `repository-operational-truth-audit` Skill slug.
- Tightened the intentional-multiplicity clean-control canary so a verdict that
  begins `Decision answer: not ready` cannot satisfy the positive assertion.
- Added a public-safe independent forward-behavior receipt and short dirty/clean
  result examples before the README architecture diagrams.
- Replaced the active architecture surface on `main` with separate native
  Mermaid diagrams embedded in the English and Simplified Chinese READMEs.
- Preserved the renderer-neutral model, all six regions, all stable node IDs,
  all 30 semantic edges, and the read-only, external-proof, and fixed-point
  boundaries while retiring the fixed-canvas SVG renderer from current source.
- Added exact Mermaid topology, localized edge-label, connector-kind,
  theme-neutrality, and locale-parity validation.

## 0.1.0 — 2026-08-30

- Released Repository Operational Truth Audit as an independently owned,
  standalone Codex Skill and public source-available repository.
- Added the complete decision-bounded, topology-first, read-only audit contract.
- Added controlled behavior cases for artifact drift, false-green evidence,
  authority drift, intentional multiplicity, missing decisions, and unavailable
  external state.
- Added deterministic repository, fixture, installation, architecture-model,
  localized-SVG, and render-drift validation.
- Added a transactional local installer with source commit, dirty-state, digest,
  backup, and target provenance.
- Added separate English and Simplified Chinese README, product, evidence,
  architecture, research, current-state, licensing, changelog, and release-note
  editions.
- Applied SUL-1.0 to functional materials and CC BY-NC-SA 4.0 to standalone
  documentation and independent diagrams through an explicit path map.
