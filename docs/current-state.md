# Current state

Last reconciled: 2026-08-30

## Product

- Product form: standalone repository and standalone Codex Skill.
- Version: `0.1.0-rc1`.
- Scope: complete topology-first, decision-bounded, read-only audit contract.
- Canonical Skill: `skills/repository-operational-truth-audit/`.
- Softpowers relationship: optional future companion/reference only; no
  generation, bundling, installation, or version ownership.

## Gates

- Source: complete `0.1.0-rc1` candidate; canonical Skill, evidence model,
  controlled eval pack, validator, tests, and transactional installer are
  present.
- Deterministic validation: PASS on 2026-08-30 — repository validator, 10 unit
  tests, six fixture truth checks, system Skill quick validation, Field Lab
  pack validation, and Field Lab six-case credibility self-test.
- Independent forward behavior: PASS on 2026-08-30. A raw artifact-split case
  reached the stale distributed entrypoint and false-green source test. A raw
  clean control treated stable/development selection as intentional
  multiplicity. Its first run exposed an incomplete fixture identity path;
  the fixture was corrected and independently rerun before acceptance.
- Git source identity: canonical Skill bytes are committed at
  `5d6a9f78c0068c5ac3b0ba361fb94106390905d1`; the installation receipt records
  that source as clean. This installation-state reconciliation changes docs
  only and does not change the Skill digest.
- Local install: PASS. The canonical and installed Skill digests both equal
  `6d5a2c72cde925f3133fd64f3ec1eb119fcf2cbe9124042362f84c672eb87c11`.
  The derived target is `~/.codex/skills/repository-operational-truth-audit/`;
  its receipt is `~/.codex/skills/.repository-operational-truth-audit-install.json`.
- Next-turn Codex discovery: not observed.
- Remote/CI: no remote configured; workflow source will not count as CI proof.
- Publication: not authorized; no public license, tag, release, or public install.

Update this file by replacing superseded status. Do not append a development
diary.
