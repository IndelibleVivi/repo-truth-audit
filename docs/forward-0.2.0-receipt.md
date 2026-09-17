# `0.2.0` forward-behavior receipt

[简体中文](forward-0.2.0-receipt.zh-CN.md)

Observed: 2026-09-17

Status: **PASS within the synthetic source and declared-artifact boundary below**

This public-safe receipt records a focused routing check, a fresh Audit
regression, and a two-increment Operate run against the unreleased `0.2.0`
source candidate. It complements, but does not rewrite, the historical
[`v0.1.0` Audit-only
receipt](forward-behavior-receipt.md).

## Subject identity

| Field | Recorded value |
| --- | --- |
| Source candidate | `0.2.0`, copied from the canonical dirty worktree based on Git HEAD `d2aebdfd82200d48dff7df4c1a8a0a9e72e1b85b` |
| Complete Skill directory digest | `8dc185ad608e1a94af3c37206f92c540b8be519cbd88c7238b9622dabc8b210b` |
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

## Evidence boundary

- These are real model turns on public synthetic repository shapes, not the
  deterministic operation lab applying known edits.
- The coordinator used a hidden evaluator after each turn; model self-report
  was not treated as acceptance.
- Session continuation from a verified checkpoint was observed. Process crash,
  lost context, stale cited bytes, selective rollback, and OS-enforced sandbox
  behavior were not exercised by this forward run; those remain deterministic
  lab or contract evidence only.
- No private repository, production data, installed copy, activated runtime,
  GitHub CI, public release, or owner-operated target was exercised.
- The run demonstrates the observed routing, Audit, and Operate outcomes on
  these fixtures. It does not establish general refactoring ability or provider
  identity.
