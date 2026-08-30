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
- Git source identity: canonical `0.1.0` Skill bytes and release source are
  committed at `e15dbabc84d3cae35c40dd9a0a87343fd57981d2`. That commit has not yet
  been tagged, pushed, or read back from a public remote.
- Local install: PASS. The clean source commit above was transactionally
  installed on 2026-08-30; canonical and installed Skill digests both equal
  `30d7ed369fad578c12d83291a17edaad4ad8c3195b2b7b31294c48ecf7ebe69e`.
  The local receipt records the clean source identity and recoverable backup.
- Next-turn Codex discovery: not observed.
- Remote/CI: the public remote and public CI result have not yet been created or
  observed. Workflow source is not CI proof.
- Publication: the owner authorized a public repository and selected SUL-1.0
  for functional materials plus CC BY-NC-SA 4.0 for standalone documentation
  and diagrams. Source and local installed acceptance are complete; public
  visibility, CI, tag, GitHub Release, and tagged public install remain separate
  pending gates.

Replace superseded status here; do not append a development diary.
