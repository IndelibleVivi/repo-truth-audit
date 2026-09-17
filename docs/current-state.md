# Current state

[简体中文](current-state.zh-CN.md)

Last reconciled: 2026-09-17

## Product

- Product form: standalone public repository and standalone Codex Skill.
- Naming: human-facing display name **Repo Truth Audit**; formal name
  **Repository Operational Truth Audit**; public repository slug
  `repo-truth-audit`; Skill invocation slug
  `repository-operational-truth-audit` remains unchanged.
- Version split: the canonical worktree contains the unreleased `0.2.0` source
  candidate. The latest public release remains immutable `v0.1.0`; no `0.2.0`
  tag or GitHub Release exists.
- Scope: one progressive Audit / Plan / Operate engagement. Audit is the
  read-only default, Plan terminates before mutation, and Operate requires an
  explicit finite implementation request plus matching effect authority.
- Canonical Skill: `skills/repository-operational-truth-audit/`, with the
  compact router in `SKILL.md` and progressive Audit, Operation, and Recovery
  methods under `references/`.
- Architecture: `docs/architecture/audit-runtime-model.json` is the semantic
  authority; the localized README Mermaid views mirror seven regions, 31 stable
  nodes, and 46 semantic edges. The original Audit topology remains intact and
  now feeds a visible Plan exit or guarded Operate loop.
- Deterministic operation evidence: `evals/operation-lab/` exercises the new
  operation invariants without invoking a target model. Its results are
  synthetic process evidence, not forward model evidence.
- Optional evidence helper:
  `skills/repository-operational-truth-audit/scripts/check_evidence.py` checks
  only cited-byte continuity. It does not prove semantics, Git snapshot
  identity, atomicity, authorization, or completion.

## Gates

- Source integration: the `0.2.0` candidate is source-complete within the
  documented repository, synthetic-fixture, and declared-artifact boundaries.
  Substantive commit `8b66e8d6608fdbb2ba2ab7908644a5c32061133a` is pushed to the
  canonical public `main`. It is not released, installed, activated, or
  owner-accepted on an external target.
- Deterministic validation: maintainer-local PASS on 2026-09-17 for repository
  and publication contracts, Audit / Plan / Operate architecture and localized
  Mermaid parity, all 73 unit tests, six Audit fixtures, the two-increment
  operation lab, system Skill validation, and Git whitespace validation. The
  operation lab itself reports zero target-model invocations and remains
  distinct from the separate forward receipt.
- Forward behavior: the paired
  [`forward-behavior-receipt`](forward-behavior-receipt.md) is historical
  `v0.1.0` Audit-only evidence. The separate
  [`0.2.0` receipt](forward-0.2.0-receipt.md) records focused target-model
  routing, a fresh Audit regression, and a same-session, two-increment Operate
  run accepted by a coordinator-side evaluator at the checkpoint and whole-goal
  B/S/D/U boundaries. This closes the source-candidate forward gate only within
  the stated synthetic source and declared-artifact scope.
- Checkpoint versus completion: a coherent verified increment may be retained
  while the whole goal remains open. Whole-goal completion requires the agreed
  Behavior, Structure, Delivery, and Usefulness witnesses; a green source test
  or present helper is not sufficient.
- Recovery: private continuity and cited evidence are recovery aids, not
  authority. Resume must re-pin the exact repository state, inspect preserved
  owner work, rerun changed witnesses, and distinguish Recovered from Complete.
- Git and CI: substantive commit `8b66e8d...` is published on canonical `main`.
  GitHub Actions run
  [`35198597031`](https://github.com/IndelibleVivi/repo-truth-audit/actions/runs/35198597031)
  passed all four Ubuntu/macOS and Python 3.10/3.13 jobs on that exact SHA. A
  later status-only reconciliation may move `main` without changing the
  substantive source identity.
- Local install: the previously verified installed copy is immutable `v0.1.0`.
  The `0.2.0` source candidate has not been installed or activated, and
  installed/source equality is not claimed.
- Next-turn Codex discovery: not observed for `0.2.0`.
- Release publication: GitHub Release `v0.1.0` remains the latest public
  release. Source-candidate work does not authorize or imply a new release.
  A future authorized `0.2.0` release must update the pinned README install ref
  and `PUBLIC_RELEASE_VERSION` together; current tests intentionally reject
  that change before the release gate is opened.
- Licensing: functional materials are source-available under SUL-1.0;
  standalone documentation, the renderer-neutral architecture model, and the
  Mermaid diagrams embedded in the README files are under CC BY-NC-SA 4.0
  according to `LICENSING.md`. The path map, not a single-license badge, is
  authoritative.

Replace superseded status here; do not append a development diary.
