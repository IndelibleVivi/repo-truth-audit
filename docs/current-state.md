# Current state

[简体中文](current-state.zh-CN.md)

Last reconciled: 2026-08-30

## Product

- Product form: standalone public repository and standalone Codex Skill.
- Version: public release `v0.1.0`.
- Scope: complete topology-first, decision-bounded, read-only audit contract.
- Canonical Skill: `skills/repository-operational-truth-audit/`.
- Public documentation: separate English and Simplified Chinese editions.
- Architecture: one renderer-neutral model plus separate day-first English and
  Chinese SVG artifacts; semantic, locale, accessibility, and render-drift
  checks are present.
- Softpowers relationship: optional companion/reference only; no generation,
  bundling, installation, or version ownership.

## Gates

- Source: public `v0.1.0` contains the canonical Skill,
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
- Git source identity: canonical `0.1.0` Skill bytes entered at
  `e15dbabc84d3cae35c40dd9a0a87343fd57981d2`. Annotated tag object
  `235be6e839a87867b7a0758b47ce577c66380111` peels to release commit
  `0180e4c23413a0691f4e895a0d64d7efaa0a12bb`. `main` may contain later
  status-only reconciliation; the tag remains the immutable release identity.
- Local install: PASS. The clean source commit above was transactionally
  installed on 2026-08-30; canonical and installed Skill digests both equal
  `30d7ed369fad578c12d83291a17edaad4ad8c3195b2b7b31294c48ecf7ebe69e`.
  The local receipt records the clean source identity and recoverable backup.
- Next-turn Codex discovery: not observed.
- Remote/CI: PASS. The public repository is
  `https://github.com/IndelibleVivi/repository-operational-truth-audit`, its
  default branch is `main`, and Actions run `33295744677` passed all four
  Ubuntu/macOS and Python 3.10/3.13 jobs on the peeled release commit using
  Node 24 Actions. Workflow source and live CI remain separate facts.
- Publication: PASS. GitHub Release `v0.1.0` was published on 2026-08-30 and is
  neither draft nor prerelease. Anonymous raw read-back of both READMEs, both
  localized SVGs, and `LICENSE` matched tagged bytes. A disposable install from
  the public tag passed Skill quick validation; its digest matched the canonical
  digest above, and its SUL text matched pinned SHA-256
  `c6d0dde0f0463c800e542d7d64237ffef37f43b17004975a558604f17b5d1af1`.
- Licensing: functional materials are source-available under SUL-1.0;
  standalone documentation and independent diagrams are under CC BY-NC-SA 4.0
  according to `LICENSING.md`. GitHub reports the layered repository license as
  `Other`; the path map, not a single-license badge, is authoritative.

Replace superseded status here; do not append a development diary.
