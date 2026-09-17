# `0.2.0` forward-behavior receipt

[简体中文](forward-0.2.0-receipt.zh-CN.md)

Observed: 2026-09-17

Status: **PASS within the synthetic source and declared-artifact boundary below;
historical payload residue reconciled and clean-payload follow-up passed**

This public-safe receipt records a focused routing check, a fresh Audit
regression, and a two-increment Operate run against the unreleased `0.2.0`
source candidate, followed by a clean-payload Plan and one-request Operate
check. It complements, but does not rewrite, the historical
[`v0.1.0` Audit-only
receipt](forward-behavior-receipt.md).

## Original forward subject identity

| Field | Recorded value |
| --- | --- |
| Source candidate | `0.2.0`, copied from the canonical dirty worktree based on Git HEAD `d2aebdfd82200d48dff7df4c1a8a0a9e72e1b85b` |
| Historical copied Skill directory digest | `8dc185ad608e1a94af3c37206f92c540b8be519cbd88c7238b9622dabc8b210b` |
| Runtime `SKILL.md` digest | `810b8756aa53174a3c11420f50871017aac0884b5eba9884b7d66f35448b5916` |
| Adapter-reported model | `commandcode/deepseek-v4.1-flash` |
| Provider identity | **Unverified** — the adapter report is not provider attestation |
| Model turns | One focused routing turn; one Audit turn; two Operate turns in one resumed session |

The Skill was copied into each disposable fixture before the run. The candidate
had not yet been committed, pushed, installed, or activated, so those higher
identities are not implied by the digests above.

## Focused routing regression

One read-only turn classified four independent requests from the final Skill
bytes without performing target work:

- an isolated `parse_config` bug fix with no topology question did not activate
  this Skill;
- an unbounded “clean everything” request entered reconnaissance with no target
  mutation;
- an explicit structural plan stayed Plan with no target mutation; and
- a finite cross-surface refactor entered Operate with only bounded local source
  authority.

The routing workspace remained clean. This is a focused instruction-following
observation, not deterministic enforcement of natural-language routing.

## Audit regression

The public `source-artifact-split` fixture was copied without its evaluator
answer. The requested mode was Audit, with `AUDIT.md` as the only authorized
write.

- The result began `Decision answer: Not ready to hand off.`
- It followed `distribution.json` to the selected `dist/cli.py`, executed the
  artifact, and observed `artifact-v1` against the documented `artifact-v2`
  contract.
- It established that the green test runs only `src/cli.py` and therefore proves
  the source layer, not the selected distribution artifact.
- Independent assertions confirmed every required decision marker, the green
  source test, the stale artifact output, and an exact changed-file set of only
  `AUDIT.md`.

This supports preservation of the read-only default and the original
decision-bounded Audit behavior after the router expansion.

## Two-increment Operate run

A separate disposable fixture began with one selected `legacy.py` path that
mixed normalization, rendering, and a durable append. Its bundle selected that
path, and an unrelated untracked `owner-notes.txt` represented pre-existing
owner work.

### Increment 1 — verified checkpoint

The first turn was explicitly bounded to a coherent checkpoint:

- normalization and rendering moved into an active `formatting.py` owner;
- `legacy.py` delegated to it but deliberately retained the durable write;
- `delivery.json` continued to select `legacy`;
- the bundle was reconciled;
- seven independent behavior/state cases remained unchanged; and
- `owner-notes.txt` remained byte-identical and untracked.

The worker classified the result as **Verified checkpoint — whole goal still
open** and named selector migration, state-owner extraction, and legacy
retirement as remaining obligations. A coordinator-side AST and executable
evaluator independently accepted the checkpoint.

During this turn the worker disclosed one malformed edit that briefly emptied
`entry.py`. It restored that tracked file from the clean baseline before the
checkpoint, verified byte identity, and reran the witnesses. The coordinator
also confirmed `entry.py` matched the baseline. This is an observed repaired
transient error, not evidence of crash recovery or general selective rollback.

### Increment 2 — whole-goal completion

The same model session resumed from that checkpoint and completed the finite
goal:

- `state_store.py` became the sole durable-write owner;
- `process.py` composed normalization, rendering, and the state owner;
- `delivery.json` selected `process`;
- the declared bundle contained the actual selected delivery files; and
- `legacy.py` was deleted rather than retained as a facade or unreachable copy.

Coordinator-side evaluation then checked all four agreed dimensions:

| Dimension | Independent observation |
| --- | --- |
| Behavior | Seven success, invalid-input, format, empty-input, and write-failure cases preserved stdout, stderr, exit code, and exactly-once state effects. |
| Structure | Only `state_store.py` owned the append primitive; selected `process.py` called the formatting and state owners; no legacy file remained. |
| Delivery | A new artifact reconstructed only from `bundle.json` executed the same behavior cases successfully. |
| Usefulness | In a second copy, a `compact` format was added by changing only `formatting.py`; the selected entrypoint used it and the durable write still occurred exactly once. |

The unrelated untracked owner file remained byte-identical. The model did not
commit, push, install, use the network, or modify the canonical source tree.

## Pre-release payload identity reconciliation

A later review of public `main` at
`f84b22c97e49ff5eb0e777f28fb3c7cb11f0ce4b` reproduced a packaging defect:
ordinary import-based tests could create an ignored
`scripts/__pycache__/check_evidence.cpython-313.pyc`, while the old digest and
installer copied every file below the Skill directory.

The retained original forward-session evidence closes the earlier digest gap:

- `find` in the disposable operation repository listed the eight declared
  source files plus exactly that `.pyc` below the copied Skill;
- `git ls-files` showed the `.pyc` had been copied into and committed with the
  synthetic subject, so it was part of the historical directory bytes;
- the historical `8dc185ad...` digest therefore remains an accurate identity
  for the directory that was evaluated, but it is not a clean distributable
  payload identity; and
- the eight clean Git payload files produce
  `80863c9796a2364d99f43cd81d6f53c8d6059f0c303061d18362ba683411a29f`.
  `SKILL.md` remains
  `810b8756aa53174a3c11420f50871017aac0884b5eba9884b7d66f35448b5916`.

The installer now uses one explicit eight-file definition for validation,
digesting, staging, installed comparison, and receipts. Known runtime residue
is not copied or hashed; other undeclared source or executable files fail
closed. The old receipt value was not replaced with the clean value.

## Clean-payload Plan and one-request Operate follow-up

Two fresh disposable Git subjects each received only the eight declared files,
with the clean payload digest `80863c...` and no undeclared entry.

### Actual Plan run

One model turn received a planning-only request rather than a classification
question. It traced the selected `legacy` entry, mixed state writer, and declared
bundle; produced a finite end state, preserved/deliberately changed behavior,
coherent increments, protected witnesses, B/S/D/U acceptance, recovery, stop
conditions, and authority boundary; and returned the plan in its response.

Coordinator read-back confirmed the ending Git snapshot equaled the start:
tracked content remained clean, the pre-existing untracked `owner-notes.txt`
was the only status entry, and no bytecode/cache appeared.

### Single-request whole-goal Operate run

One model turn received the complete finite outcome once. Without a second
human “continue” prompt, it established fresh behavior/state witnesses, split
formatting and the durable writer, switched the real delivery selector,
reconciled the declared bundle, deleted `legacy.py`, challenged false completion,
rebuilt the artifact, and reported the whole goal complete rather than stopping
at the extraction checkpoint.

The worker's 18-case comparison observed identical exit code, stdout, stderr,
and state bytes. Coordinator-side checks then independently established:

| Dimension | Clean-payload follow-up observation |
| --- | --- |
| Behavior | Seven fixed evaluator success/failure/state cases passed through the selected entry. |
| Structure | `runner.py` composed `formatting.py` and the sole writer `storage.py`; `legacy.py` and legacy imports were absent. |
| Delivery | An artifact reconstructed only from `bundle.json` passed the same fixed cases and structural checks. |
| Usefulness | A second copy added `compact` by changing only `formatting.py`; selected-entry behavior and exactly-once state remained correct. |

`owner-notes.txt`, `entry.py`, `AGENTS.md`, and the copied Skill remained
unchanged; no file was staged or committed. This observes one-request
whole-goal follow-through on this finite synthetic shape, not general autonomous
refactoring reliability.

## Evidence boundary

- These are real model turns on public synthetic repository shapes, not the
  deterministic operation lab applying known edits.
- The coordinator used a hidden evaluator after each turn; model self-report
  was not treated as acceptance.
- Session continuation from a verified checkpoint was observed. Process crash,
  lost context, stale cited bytes, selective rollback, and OS-enforced sandbox
  behavior were not exercised by this forward run; those remain deterministic
  lab or contract evidence only.
- The clean-payload follow-up added one real Plan turn and one real Operate turn
  that completed the finite whole goal without a second prompt. It did not test
  arbitrary planning/refactoring, durable-data migration, or crash resumption;
  the small subject also does not establish reliable autonomous selection of
  multiple checkpoints for larger work.
- No private repository, production data, installed copy, activated runtime,
  GitHub CI, public release, or owner-operated target was exercised.
- The run demonstrates the observed routing, Audit, and Operate outcomes on
  these fixtures. It does not establish general refactoring ability or provider
  identity.
