# Current state

[简体中文](current-state.zh-CN.md)

Last reconciled: 2026-09-20

## Product and source

Repo Truth Audit remains one standalone Skill with Audit / Plan / Operate modes.
The invocation slug and canonical path `skills/repository-operational-truth-audit/`
are unchanged. Audit stays read-only; Plan stops before edits; Operate carries an
explicit finite structural-change outcome through its applicable evidence boundary.

Source `0.2.1` is an **unreleased candidate**, developed in
[PR #5](https://github.com/IndelibleVivi/repo-truth-audit/pull/5) from public baseline
`e70642fff3c09476b5a81cebde0f16c5cdb4cc16`. Latest public release remains `v0.2.0`;
stable installation stays pinned to that release. PR #5 records the source
integration state; no candidate daily installation, tag or release was performed.

The candidate refines auxiliary-method applicability, proportionate witnesses,
authorized dirty-work retirement, lasting verification costs and evidence-based
reassessment of a challenged result. It adds no execution engine, installed
runtime file, mode, coverage quota or per-test approval gate. The eight-file
payload definition in `scripts/common.py::SKILL_PAYLOAD_FILES` is unchanged;
the candidate payload and bounded forward evidence are pinned in the
[0.2.1 receipt](forward-0.2.1-receipt.md).

The renderer-neutral architecture model remains authoritative, with its existing
seven regions, 31 stable nodes and 46 edges. These refinements operate within the
existing authority, witness, increment and acceptance nodes; no topology or SVG
layout change is proposed. The optional byte checker still proves named bytes
only, not semantic correctness, authorization, isolation or activation.

## Candidate evidence

Six contrasted synthetic subjects and six fixture/counterexample tests are added
under the existing operation lab. They cover optional versus project-required
test-first workflows, a real duplicate-write defect hidden by output-only green,
selected artifact retirement, authorized dirty cleanup and a read-only control.
Preparation creates a fresh synthetic Git repository and exposes only the target
files and request; evaluator reviews and known edits stay outside its inputs.

The reviewed runtime head `aa84cd0c7cf84caae9055b90623f03f74bea4d10` passed
[PR CI run 35498436856](https://github.com/IndelibleVivi/repo-truth-audit/actions/runs/35498436856)
on Ubuntu/macOS and Python 3.10/3.13. Local acceptance independently passed
repository/architecture validation, all 91 unit tests, six fixture self-tests and
Skill validation. The optional Field Lab pack was migrated to a disposable v2
manifest without modifying source; validation and six expected-overlay self-tests
passed with zero target-model calls. Later documentation commits retain their
own PR checks; this CI link is pinned to the reviewed runtime head.

**Bounded synthetic forward acceptance passed:** nine fresh native sessions and
two read-only continuations, with independent diff/source/bundle/ledger checks.
The [receipt](forward-0.2.1-receipt.md) records identities, actual helper exposure,
required test-first ordering, dirty before-image preservation, unchanged read-only
subjects and opposite complaint verdicts for complete/incomplete results. Both
versions passed the two-by-two helper comparison; this does not demonstrate
superiority or method selection without a literal conflict. Ordinary validation
still makes no network or target-model calls.

[Issue #4](https://github.com/IndelibleVivi/repo-truth-audit/issues/4) and its
maintainer clarification motivate this work. They do not establish that RTA or
TDD caused a failed cleanup. The candidate does not change the reporter's project
or infer that useful tests should be removed.

## Stable release and remaining gates

The published [v0.2.0 release](releases/v0.2.0.md),
[release record](release-preparation.md) and
[0.2.0 forward receipt](forward-0.2.0-receipt.md) retain their exact historical
claims. Its annotated tag peels to `5d25c581a7d331329d39be9f6bace11371dd4437`.
The recorded 0.2.0 installation/discovery and payload digest belong to those
historical bytes; they are not current candidate installation evidence.

The original diff has independent review and the candidate has forward evidence
at the declared synthetic boundary. Integration still requires final-head checks;
PR #5 records that outcome. Installation, fresh host discovery and publication
remain separate owner-authorized gates. Source acceptance is not a release.

Functional materials remain source-available under SUL-1.0. Standalone public
documentation and diagrams use CC BY-NC-SA 4.0 according to [LICENSING.md](../LICENSING.md).
No external Skill text or code is vendored; the optional test-first policy in the
new subjects is original synthetic evaluator material.
