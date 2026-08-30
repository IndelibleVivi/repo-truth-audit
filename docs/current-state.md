# Current state

[简体中文](current-state.zh-CN.md)

Last reconciled: 2026-08-30

## Product

- Product form: standalone public repository and standalone Codex Skill.
- Version: source-complete `0.1.0` release candidate.
- Scope: complete topology-first, decision-bounded, read-only audit contract.
- Canonical Skill: `skills/repository-operational-truth-audit/`.
- Public documentation: separate English and Simplified Chinese editions.
- Architecture: one renderer-neutral model plus separate day-first English and
  Chinese SVG artifacts; semantic, locale, accessibility, and render-drift
  checks are present.
- Softpowers relationship: optional companion/reference only; no generation,
  bundling, installation, or version ownership.

## Gates

- Source: the source-complete `0.1.0` publication candidate contains the canonical Skill,
  layered license files, paired public documentation, evidence model,
  controlled eval pack, architecture model/renderer, validators, tests, and
  transactional installer.
- Deterministic validation: PASS on 2026-08-30 — architecture model and locale
  parity, deterministic SVG render check, repository/publication validator, 14
  unit tests, six fixture truth checks, fixture self-test, system Skill quick
  validation, and Git whitespace validation.
- Independent forward behavior: PASS on 2026-08-30. An artifact-split case
  reached the stale distributed entrypoint and false-green source test; a clean
  control treated stable/development selection as intentional multiplicity.
- Git source identity: the release source is the repository commit containing
  this state. It has not yet been tagged, pushed, or read back from a public
  remote; no public identity claim is made here.
- Local install: the earlier release-candidate Skill remains installed. Final
  `0.1.0` installation and source/installed digest equality are pending the
  clean release commit because package-local license and notice files change
  the Skill digest.
- Next-turn Codex discovery: not observed.
- Remote/CI: the public remote and public CI result have not yet been created or
  observed. Workflow source is not CI proof.
- Publication: the owner authorized a public repository and selected SUL-1.0
  for functional materials plus CC BY-NC-SA 4.0 for standalone documentation
  and diagrams. Source preparation is in progress; public visibility, tag,
  GitHub Release, and tagged public install remain separate pending gates.

Replace superseded status here; do not append a development diary.
