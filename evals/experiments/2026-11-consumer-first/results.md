# Consumer-first follow-up: results and limits

[简体中文](results.zh-CN.md)

Observed: 2026-11-14. The finite continuation is closed at **24 launched subject
sessions**. It did not complete the original four-task/three-arm study and did
not establish that RTA or the short instruction repays review/coordination cost.
One valid ordinary-repair pair succeeded in both arms. Both final migration arms
produced consumer-verified delivery checkpoints but failed to finish the full
Task within the deadline because the required report was absent.

## Cohort accounting

| Cohort | Frozen source/registration | Launched | Disposition |
| --- | --- | --- | --- |
| Original | `03e37060f5da720aa318d9021c03a73809fe5404`; original registration/settings | 12 | Independent, result-blind review found three fixture/oracle defects; all outcomes unjudged. Host statuses: 9 finished, 1 timeout, 2 interrupted. |
| Setup repair v2 | `3df91f43fd9a4430070c816d8e21a4648f99e355`; recovery registration/settings | 8 | The coordinator's common prompt imposed the clean task's read-only scope on implementation tasks. Six implementation outcomes remain unjudged; the two valid-scope clean controls were interrupted before their required reports. Four reservations never started. |
| Final four | `27dfe50afad667c1ad917da95dc6da79a692be0c`; final-four registration | 4 | Explicit write authority, no retries. One ordinary no-Skill/short pair and one migration full-RTA/short pair. |

The [setup recovery record](setup-recovery.md) retains the three counterexamples,
the contradictory harness clause and prior-result exposure. Registrations and
settings are historical byte identities, not descriptions silently refreshed to
new source. The first two cohorts are not pooled with the final four or turned
into model repair failures. Two stale `running` labels after v2 cancellation are
preserved alongside their reconciliation: independent PID/arguments read-back
and termination established no remaining writer. All subject processes stopped.

Portable receipts retain every launched slot and measured or missing counters:
[original twelve](aborted-observations.json), [recovery eight and four unstarted reservations](recovery-observations.json),
[final ordinary pair](final-known-bug-observations.json) and
[final migration pair](final-migration-recovery-observations.json).
Raw inputs, prompts, reports, events, subjects and review evidence remain private
outside Git. They are not publicly independently inspectable; receipts record
provenance and screened observations, not authenticated transcripts.

## Independent acceptance

| Task / arm | Host | Retained product | Full Task verdict |
| --- | --- | --- | --- |
| Ordinary / short | Finished | Selected source CLI, actual produced ZIP, candidate regressions and accurate `RESULT.md` pass | Success |
| Ordinary / no Skill | Finished | Same obligations pass | Success |
| Migration / short | 180-second timeout | Source, structure, actual ZIP and protected bytes pass; `RESULT.md` absent | Failure: full Task incomplete within the deadline; passed checkpoint retained |
| Migration / progressive RTA | 180-second timeout | Same checkpoint passes; `RESULT.md` absent | Same deadline failure |

The ordinary recipient was run on each actual ZIP before candidate tests were
executed in disposable copies. ZIP members matched the final declared bundle.
Ascending, descending and singleton positive ranges passed; zero, negative and
malformed inputs retained their error behavior. Both candidate regression scripts
passed. Both final diagnoses matched the observed defect; no contradicted causal
claim or out-of-scope semantic edit was found.

Migration checks accepted JSON/text compatibility, empty input, invalid shapes,
boolean rejection, error order and write failure for source and delivered code.
The selected runner and storage own their respective responsibilities; the old
writer is retired from source and bundle. Both later owner notes and CLI bytes
are preserved. All four runs changed **zero registered protected paths** by exact
byte comparison. This is not an audit of every external action. Fresh temporary
verification directories were explicitly permitted.

The report obligation was registered before these results. Missing `RESULT.md`
is an observed unmet Task obligation; the verdict follows that fact, not timeout
alone. A passing product evaluator is insufficient for full completion. No final
diagnosis exists for either migration, so final misattribution and human
continuation-rework measurements remain unavailable. Neither artifact was repaired
or supplied with a report after the session.

## Exposure and native measurements

The three treated final runs show completed `cat` reads of exact frozen treatment
paths with exit 0 and nonempty output. The progressive run read the Skill and
progressive references; availability of the nine-file snapshot does not mean
every byte was read. The short instruction digest is
`98bad017590772950116c4c4182fd8d135b5fe0de3bce93d66c11eed97796410`;
the unchanged nine-file RTA digest is
`28b73009402e0f149c7078379a15d51cf88468c66ec092f49a59a5f6926fb211`.
The no-Skill run received neither treatment and shows no explicit treatment read;
the ambient RTA path was disabled for the invocation. Normal host context was
not proved empty. These are explicit-exposure trials, not automatic discovery.

| Final run | Completed command items | Wall seconds | Host input tokens | Host cached input | Host output tokens |
| --- | ---: | ---: | ---: | ---: | ---: |
| Ordinary / short | 8 | 99.933 | 194907 | 160384 | 3076 |
| Ordinary / no Skill | 8 | 110.645 | 227079 | 203264 | 2998 |
| Migration / short | 14 | 180.069, censored | unavailable | unavailable | unavailable |
| Migration / progressive RTA | 16 | 180.059, censored | unavailable | unavailable | unavailable |

A command item is `item.completed` with type `command_execution`, including
nonzero exits. It is not shell subcommands, all tool calls or human minutes.
Token fields are verbatim `turn.completed` usage. Cached and reasoning fields
are retained separately, not summed; cumulative/cache and billing semantics are
unverified. No completion event exists for either timeout, so usage is null,
not zero. The requested model was `gpt-6.1-sol`, reasoning `high`, through native
Codex CLI 0.159.1 on macOS arm64; the actual backend identity was not exposed.
Sessions used existing native ChatGPT login, at most three concurrent, 180 seconds
each, no retries and no new paid credentials/services. An Agent session can
contain multiple internal API requests. Three earlier native host smoke tasks
are a separate evidence set, outside these 24 subject sessions.

The ordinary pair has equal command items, fewer reported input tokens and more
output tokens in the short arm. One purposive pair with ordinary host context,
cache variation, concurrent execution and prior harness corrections supports no
causal efficiency claim. Both migration counts stop at incomplete outcomes;
fewer commands do not establish cheaper successful delivery. The comparator
may match the two independently judged failures, but its delta has that limited
meaning. Human active time, owner review time and continuation rework were not
timed. No review packet was sent to a person and no owner benefit is inferred.
The receipt counts do not include the coordinator's setup repair/review cost.

## Reproduce the offline comparison

```bash
python3 scripts/compare_trials.py \
  evals/experiments/2026-11-consumer-first/final-known-bug-observations.json \
  --baseline without-skill --candidate consumer-first
python3 scripts/compare_trials.py \
  evals/experiments/2026-11-consumer-first/final-migration-recovery-observations.json \
  --baseline progressive-rta --candidate consumer-first
```

These commands compare stored observations and launch zero models. The original
balanced registration remains incomplete: there is no valid final Cedar pair,
completed clean-control block, completed difficult-task advantage or timed owner
review. The package/CI and fixture checks do not fill those gaps.

## Decision

Retain the stronger consumer/oracle checks and the native host observations.
Keep the installer default and canonical Skill unchanged. Keep consumer-first as
an experimental instruction, not a second installed Skill. These results justify
neither expanding the method nor replacing it with the short instruction.

A further value study would need a new registration, a matched difficult task
with enough completion time, result-blind harness-scope review, finite repetitions
and genuinely measured owner effort if review cost is the question. This is the
next research decision, not an automatic continuation or authorization for more
calls. Windows/OpenCode UI adoption and other native hosts still need their exact
environments. No release, stable tag move, merge or daily installation occurred.
