# Independent forward-behavior receipt

[简体中文](forward-behavior-receipt.zh-CN.md)

Observed: 2026-08-30

Status: **PASS within the evidence boundary below**

> **Historical evidence boundary:** this receipt applies only to the
> `v0.1.0` Audit-only runtime identified below. The `0.2.0` source candidate
> changes the runtime contract to Audit / Plan / Operate and is not validated
> by these runs. See [`current-state.md`](current-state.md) for the active gate.

This is a public-safe projection of two independent, read-only forward runs. It
records the tested decisions, material results, proof layers, and limitations;
it is not a transcript or a replacement for the evaluator artifacts.

## Subject identity

| Field | Recorded value |
| --- | --- |
| Formal product name | Repository Operational Truth Audit |
| Skill invocation slug | `repository-operational-truth-audit` |
| Run-local Git ref | **UNKNOWN** — the evaluator results did not retain a target-subject HEAD |
| Runtime Skill entrypoint digest | `cc16bad2960a3d0e315c055cf5ec244ec57c2f7cc51da12d5d480b603bf1c15f` (`SKILL.md`, SHA-256) |
| Digest reconciliation | The entrypoint digest is identical at initial Skill commit `5d6a9f78c0068c5ac3b0ba361fb94106390905d1`, release-source commit `e15dbabc84d3cae35c40dd9a0a87343fd57981d2`, and the tested pre-display-name source |
| Observed model | **UNKNOWN** |
| Observed reasoning effort | **UNKNOWN** |

The later **Repo Truth Audit** display-name change alone affected UI metadata,
not the runtime `SKILL.md` whose digest is recorded here. The subsequent
`0.2.0` runtime expansion does change `SKILL.md` and lies outside this receipt.

## Case results

### Source / artifact split

- **Case:** [`source-artifact-split`](../evals/cases/source-artifact-split/)
- **Decision prompt:** Is this repository ready to hand to an operator as a
  packaged CLI? Follow the actual distribution selector and determine what the
  green test proves.
- **Public repository shape:** README claim, `distribution.json`, source CLI,
  distributed CLI, and a source-only test.
- **Material result:** **Not ready.** `distribution.json` selected
  `dist/cli.py`, whose fresh output was `artifact-v1`; current source and the
  documented package contract said `artifact-v2`. The green test directly
  executed `src/cli.py`, so it remained green without reaching the selected
  distribution artifact.
- **Proof layers reached:** documentation claim -> distribution manifest ->
  selected artifact -> fresh execution; test entrypoint -> source execution ->
  assertion boundary.
- **Boundary:** no installed copy, activated runtime, operator environment, or
  owner acceptance was observed.

### Intentional multiplicity clean control

- **Case:** [`intentional-multiplicity`](../evals/cases/intentional-multiplicity/)
- **Decision prompt:** Can the documented stable artifact selector be used
  while development continues on `main`, without either route silently
  selecting the other?
- **Public repository shape:** README and changelog, one executable selector,
  separate stable/development state records, and separate selected identities.
- **Material result:** **Ready within repository scope.** Stable and development
  required explicit selectors, resolved to distinct identities, and rejected
  missing or cross-boundary selector combinations. The result was intentional
  multiplicity, not drift or a shadow path.
- **Proof layers reached:** documented command -> executable selector ->
  channel-specific state -> selected identity and physical path -> successful
  route plus cross-boundary rejection.
- **Boundary:** installed runtime was out of scope; repository metadata did not
  independently prove filesystem-enforced immutability of arbitrary release
  bytes.

This clean result is the post-fixture-completion retest. An earlier exploratory
pass over an incomplete fixture shape is not used as product evidence.

## Overhead record

| Case | Command executions | Plan updates | Nested subagent events | Case ceilings |
| --- | --- | --- | --- | --- |
| `source-artifact-split` | **UNKNOWN** | **UNKNOWN** | `0` observed | `14 / 1 / 0` |
| `intentional-multiplicity` | **UNKNOWN** | **UNKNOWN** | `0` observed | `12 / 1 / 0` |

The retained public-safe results list material commands but not low-level event
counters. Reverse-engineering a tool-event count from shell lines would be
misleading, so unavailable observed counts remain `UNKNOWN`. The final column
records the command / plan / subagent ceilings from each public case contract,
not observed usage.

## Retention and limitations

- Full evaluator result text remains in the private originating task history;
  no raw trace or private repository evidence is copied into this public tree.
- A standalone low-level event-trace export was not retained, which is why the
  exact command and plan counts are `UNKNOWN`.
- Deterministic assertions now distinguish `Decision answer: ready` from
  `Decision answer: not ready`. Whether an otherwise correct result adds
  unrelated generic hygiene noise remains a semantic evaluator judgment; this
  receipt does not invent a complex schema for it.
- These runs prove forward behavior on the two public synthetic shapes. They do
  not prove installation, Codex discovery, live runtime state, or owner
  acceptance.
