# Consumer-first instruction experiment - November 2026

[简体中文](README.zh-CN.md)

This is a preregistered, offline experiment package. It prepares four matched
tasks, schedules at most twelve fresh one-replicate sessions, and evaluates the
artifacts those sessions produce. The helper does not start a model or choose a
host. The coordinator must freeze this package and select the harness before the
first target-agent call.

The original registration and `execution-settings.json` preserve the first,
aborted `03e3706` cohort. Use the separate [setup recovery](setup-recovery.md),
[recovery registration](recovery-preregistration.json) and recovery settings for
the corrected cohort. Its results must remain separate from the first cohort.

## Question and status

Does a short consumer-first instruction preserve independently verified task
success, attribution, ownership, and protected inputs with less native tool or
token use than the current progressive Skill snapshot? The three arms are:

| Arm | Exposure |
| --- | --- |
| `without-skill` | Task and subject only; no RTA payload or experimental instruction |
| `progressive-rta` | The exact nine-file RTA payload below plus `instructions/progressive-rta.md` |
| `consumer-first` | The short instruction at `instructions/consumer-first.md`; no RTA payload |

This package contains no observations and reports no advantage. No target-model
call has been made. The twelve slots are exactly four tasks by three arms by one
replicate. Further replication requires a new preregistration, seed, budget, and
result-blind-integrity declaration; it cannot be added by editing the frozen
slot count.

## Frozen identity

The treatment snapshot is the repository's declared nine-file Skill payload.
Its identity is computed with `scripts/common.py::SKILL_PAYLOAD_FILES` and
recorded in `preregistration.json`. The current source payload digest is
`28b73009402e0f149c7078379a15d51cf88468c66ec092f49a59a5f6926fb211`.
The payload's executable bits and bytes, not an installed copy or a whole
directory, define this treatment. Loading the snapshot in a fresh session tests
explicit treatment use, not host discovery.

The order seed is `consumer-first-2026-11-14-v1`. Slot order is SHA-256 order
over seed, task id, and arm id. The resulting twelve slots are in
`preregistration.json` and are frozen by tests. Replace no slot after observing
an outcome.

## Tasks

| Task | Kind | Subject and accepted outcome |
| --- | --- | --- |
| `migration-recovery` | hard ownership continuation | Resume the partial receipt-CLI migration with a misleading checkpoint and later owner edit. Finish source separation, retire the old writer from CLI/bundle, preserve behavior and owner bytes, and verify source plus a freshly built delivery artifact. |
| `delivery-adoption` | hard selected-consumer change | Repair Cedar so an independent packet recipient can locate complete cited records after export, while preserving summary reading, professional judgment, source input, and the declared delivery. |
| `known-bug` | ordinary local control | Repair a small synthetic parser bug through its selected CLI and declared bundle, preserving adjacent valid input. This is not an RTA-shaped task. |
| `clean-baseline` | clean/no-change control | Audit a coherent small CLI against its accepted local behavior. Report that no change is warranted and leave every supplied byte unchanged. |

English agent prompts are in `tasks/en/`; corresponding Task prompts are in
`tasks/zh-CN/`. EN and ZH are paired versions of the same four task identities,
not translation evidence. Run the chosen language consistently within a matched
block, or preregister language as a separate blocking factor. Do not mix
languages inside one comparison without accounting for it.

## Preregistered judgments

These judgments are fixed before results:

- **Independent success:** every task-specific evaluator passes on a disposable
  copy, including the selected entry, behavior, declared delivery artifact, and
  protected inputs. The agent's `RESULT.md` or self-description is not sufficient.
- **Misattribution:** the final visible diagnosis names a mechanism or lifecycle
  fact contradicted by the evaluator's current source/state observation. A vague
  result, an unread setup limitation, or a correct description followed by a
  self-correction is not automatically misattribution; record the distinction.
- **Materially invalid edits:** a change outside the task's authorized semantic
  outcome that alters behavior, delivery, durable state, or declared ownership,
  or a task-required edit that is missing. Formatting-only noise is recorded as
  unnecessary-change evidence but is not by itself a failure.
- **Protected-input violation:** a byte change to a path the prompt names as
  protected, including an evaluator seed, supplied decision/spec, owner note, or
  clean-control product byte. Instruction-only claims of preservation do not
  substitute for byte comparison.
- **Native tool/token counts:** record only counters the actual host exposes.
  "Tool calls", executor commands, nested calls, and input/output tokens remain
  separate. Native-name fields should use the comparator's existing metrics where
  possible; aliases must not be summed. Missing counters remain `unavailable`
  with null, never zero.
- **Continuation rework:** for `migration-recovery`, record owner/reviewer work
  needed after the first returned artifact to reach the accepted result, in
  seconds when timed and otherwise null. Tool retries and intermediate agent
  errors are not human rework unless a human performed them.
- **Setup block:** dependencies, compiler, fixture preparation, permissions, or
  harness startup failed before the task could be exercised. The outcome is
  `blocked`, evidence names the exact failing boundary, and it is not counted as
  a task failure or a model effect.
- **Unread treatment:** the treatment was available but no host evidence shows
  it was read. Preserve the run as `available-unread`; a two-treatment
  comparison remains non-comparable under the receipt rules. Do not relabel it
  `loaded` after inspecting the outcome.

Failure, blocked, and unjudged sessions stay in the receipt and denominators.
No run is discarded after seeing its result.

## Human review protocol

Review is voluntary. Do not contact, recruit, or identify reviewers from this
package, and do not fabricate a review. A willing owner/reviewer may be given a
packet with run ids replaced by opaque review ids, arm labels and treatment text
removed, and task prompts/receipts separated from expected answers. Ask only the
reviewer's active elapsed time for each packet using a stopwatch they operate.

Record `human_active_seconds` for that active review time. Record agent
`elapsed_seconds` separately from the harness if available. Never infer human
minutes from report length, token count, tool count, or wall-clock overlap.
Reviewer identity, account data, private notes, and raw timestamps stay outside
tracked files. If no voluntary review occurs, all human fields remain
`unavailable`.

## Prepare, run, and grade

The coordinator chooses the harness and runs models; this package never does.
Prepare a fresh subject only into a nonexistent path:

```bash
python3 evals/experiments/2026-11-consumer-first/prepare_trial.py \
  migration-recovery /path/to/new-subject
```

The command prints task identity, prompt/subject digests, protected paths, and
the frozen expected target-model invocation count (`0`). It rejects a
destination whose lexical or resolved path overlaps a source, subject, helper,
or protected fixture path.

Use the generated prompt from `tasks/en/` or `tasks/zh-CN/`; keep expected
answers in this package. For an Operate task request `RESULT.md` and a
measurement note outside the subject. For `clean-baseline`, allow only
`INTENT-AUDIT.md` inside the subject.

Independently grade an actual returned artifact:

```bash
python3 evals/experiments/2026-11-consumer-first/verify_trial.py \
  migration-recovery /path/to/returned-subject \
  --artifact /path/to/returned.zip --output /path/to/evidence.json
```

The output path cannot overlap the candidate, evaluator fixture, or supplied
artifact. Add `--negative-control` to confirm each verifier rejects its designed
known-bad artifact; the valid adjacent control is exercised automatically.

Create an anonymous review packet without imposing it as an evidence requirement:

```bash
python3 evals/experiments/2026-11-consumer-first/prepare_review.py \
  --subject migration-recovery --arm progressive-rta --result /path/to/RESULT.md \
  --output /path/to/review-packet.json
```

Convert completed receipts with the existing comparator:

```bash
python3 scripts/compare_trials.py /path/to/completed-receipt.json \
  --baseline without-skill --candidate consumer-first --json
```

The comparator remains owned elsewhere. Compare `progressive-rta` with
`consumer-first` as a separate two-treatment call. Do not edit comparator
semantics here or silently substitute an unsupported three-arm schema.

The invocation unit is a fresh Agent subject session, not an individual API
request inside its tool loop. Local settings are frozen separately in
`execution-settings.json`: twelve sessions maximum, 180 seconds each,
three concurrent, no retries or new paid credentials. Host-reported usage does
not measure active human time. For Chinese subjects, pass `--language zh-CN` to
both preparation and verification; keep one language within each matched block.
The optional review exporter redacts known arm labels in a report draft;
check paths, names and other identity clues manually before voluntary review.

## Limits

The fixtures are trusted synthetic code executed in disposable copies; this is
not hostile-code isolation or network containment. The difficult tasks are
purposively selected, not representative. Cedar is a known research subject and
may be familiar to a model. The current payload identity proves declared bytes,
not discovery or actual reading. Exact backend model identity and native counters
depend on the harness. Twelve slots support only descriptive paired evidence.
