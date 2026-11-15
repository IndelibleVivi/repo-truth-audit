# Four paired engineering tasks — November 2026

[简体中文](README.zh-CN.md)

This directory holds an offline, reproducible experiment, not a model runner or
installed Skill dependency. Read the [study](../../../docs/user-outcomes-study.md)
for field mechanisms and product decisions.

## Observed result

Eight fresh native agents completed four task pairs. The independently verified
outcome was success for both arms of every pair. There was no observed success-rate
gain. Self-reported executor counts were equal on mitt and higher for the candidate
on the other three tasks. No time, token, monetary-cost or human productivity
improvement can be calculated from this evidence.

| Task | No Skill outcome | Candidate outcome | Executor calls, no Skill / candidate | Inclusive tool calls, no Skill / candidate |
| --- | --- | --- | --- | --- |
| Typed mitt unsubscribe | Success | Success | 15 / 15 | 24 / 25 |
| Cedar revision packet repair | Success | Success | 6 / 13 | 14 / 22 |
| Summary-only read-only audit | Success | Success | 8 / 10 | 14 / 16 |
| Resume partial storage migration | Success | Success | 6 / 10 | 14 / 21 |

Counts are **proxy** observations from each agent's measurement report. Executor
calls count `exec_command`, not shell statements or every child process. Inclusive
tool counts include orchestration wrappers and nested calls and are therefore
not independent units of work. The comparator retains them without computed
deltas. Exact backend model ID, token usage, task-attributable elapsed time,
owner review time and active human time were not exposed or recorded.

The final visible diagnoses were independently read: no wrong attribution was
found in that limited scope. There was no authenticated trace of all hidden
reasoning or filesystem effects. Unnecessary-change counts are unavailable;
the final diffs were qualitatively reviewed without inventing a numerical
definition after observing the results. Both summary reports preserve the product
bytes and legitimate expert judgment. Their sizes were 2,703 and 2,950 Unicode
characters; these are not review-time measurements.

Two intermediate errors remain in the receipt: the mitt control initially
compiled its CommonJS runner without `esModuleInterop`, then corrected that setup;
the resume candidate had one orchestration syntax error before a nested tool ran.
Neither task was discarded. Full mitt development lint/Mocha was unavailable in
the supplied task environment; actual compiler, negative type controls, generated
declarations and package runtime were independently checked.

## Identity, treatment and limits

RTA source baseline: `9fd099b6c9e88be2d7c809b021add51a5c8d6b8f`.
Frozen treatment payload:
`28b73009402e0f149c7078379a15d51cf88468c66ec092f49a59a5f6926fb211`.
Both arms ran in the same Linux workspace with Python 3.12.14 and Node 24.22.1;
mitt used TypeScript 4.9.5. Native agents started with `fork_turns=none`, inherited
the session's model/settings and had no explicit model override. Matching that
recorded configuration does not prove an exact backend model identity.

Each agent receives only its task and directory. Candidate agents additionally
receive the frozen Skill and an explicit instruction to load it. Controls have no
RTA payload. Shared general model knowledge cannot be removed. Agents may inspect
and change the authorized subject but may not read other trials, evaluator code or
solutions, access the network, delegate, contact upstream, publish or install
globally. These are instruction scopes on a shared filesystem, not OS sandboxes.

The four pairs are purposively selected, unrandomized, with one run per arm per
task and no stable-release arm. They are task-level observations, not eight
independent estimates of one treatment effect. The real historical mitt defect
may be familiar to a model. Explicit Skill loading does not test implicit discovery.
The local Codex CLI failed at app-server initialization before a model call;
these results are from native research agents, not `codex exec`.

The [observations JSON](observations.json) contains matching input identities,
exposure, independently judged outcomes, metric provenance and unavailable data.
Its evidence locators are relative to the separately delivered research evidence
packet, not files required by the comparator. Raw reports, patches and per-run
consumer results stay outside the Git source tree. Cedar/summary identities were
reconstructed from the original Git tree and verified against the generator;
resume matches both pretrial receipts; mitt matches the retained original
template. These are documented provenance checks, not timestamp authentication.

## Task inputs

| Case | Owner task | Independent result boundary |
| --- | --- | --- |
| `mitt` | Make the supplied typed application stop wildcard listeners while named listeners continue; carry the fix to its actual local package | Independent compiler, invalid-type controls, runtime sequence and freshly generated declaration |
| `cedar` | Export the complete records needed for source/revision review; preserve input, ordering, ordinary summary reads and human judgment | Fresh source and declared artifact recipients, packet only, producer removed, two crossed histories |
| `summary` | Judge the accepted summary meeting use; do not import a revision-review requirement; write only the audit report | Original product bytes, independent packet reading, then separate semantic report review |
| `resume` | Finish previously authorized ownership separation; retire legacy from CLI/bundle; preserve output, failures, state effects and later owner edits | Source, newly reconstructed artifact and the actual delivered ZIP; selected owner structure and error order |

Prepare fresh synthetic subjects from the RTA repository root. Destinations must
not exist. The scripts call no model and copy no evaluator answers:

```bash
python3 evals/experiments/2026-11-user-outcomes/prepare_trial.py cedar /path/to/new-cedar
python3 evals/experiments/2026-11-user-outcomes/prepare_trial.py summary /path/to/new-summary
python3 evals/experiments/2026-11-user-outcomes/prepare_trial.py resume /path/to/new-resume
```

For mitt, prepare the pinned source/package seed using the
[field instructions](../../field/README.md), then:

```bash
python3 evals/experiments/2026-11-user-outcomes/prepare_trial.py mitt /path/to/new-mitt \
  --mitt-source /path/to/mitt --consumer-seed /path/to/mitt-consumer
```

The helper writes the four-line typed consumer input and reconstructs the exact
source from commit `6b41670516ed8e8b738612f60491995470aa63b3`
and copies the prepared dependencies without fetching them. The original task
and application instructions are [mitt-task.md](mitt-task.md) and
[mitt-consumer.md](mitt-consumer.md). These are English experimental inputs;
translation would create a new prompt identity, not the same trial.

Create each arm independently and compare its returned input digests before
running a fresh agent. Expose only `TASK.md` and the subject to the control.
For a candidate, copy the exact nine-file payload using
`scripts/common.py::copy_payload` into a separate readable location, record its
digest, and add the explicit loading instruction. Keep evaluator files and
expected outputs outside its context. Preserve the same authority and task;
do not tell one arm the diagnosis or demand extra reporting only from it.

For repair tasks request `RESULT.md` and a measurement report describing actual
available counters. For the read-only summary task, allow `INTENT-AUDIT.md` in
the subject and put measurements outside it. Record the exact routing instruction
in future harness receipts; this round records exposure and task identity but
does not claim a fully exported host transcript.

## Independent regrading

These checks operate on disposable copies of trusted experimental subjects.
They do not provide hostile-code containment. The mitt compiler comes from the
evaluator's immutable seed, not a compiler the target can modify.

```bash
python3 evals/experiments/2026-11-user-outcomes/verify_trial.py mitt /path/to/mitt-result \
  --consumer-seed /path/to/immutable-consumer-seed --output /path/to/evidence/mitt.json
python3 evals/experiments/2026-11-user-outcomes/verify_trial.py cedar /path/to/cedar-result \
  --output /path/to/evidence/cedar.json
python3 evals/experiments/2026-11-user-outcomes/verify_trial.py summary /path/to/summary-result \
  --output /path/to/evidence/summary.json
python3 evals/experiments/2026-11-user-outcomes/verify_trial.py resume /path/to/resume-result \
  --artifact /path/to/the-agent-delivered.zip --output /path/to/evidence/resume.json
```

The summary command verifies the technical contract only. Read its report to
judge adoption, scope and the absence of invented obligations. The resume
command's `--artifact` matters: reconstructing a good artifact does not establish
that the agent's claimed delivered ZIP contains it.

The resume control legitimately retained a file consisting only of a docstring
and `from runner import process`. The actual task says: “Retire legacy.py from
the selected CLI and the declared bundle.” Both exclude it; it contains no old
implementation or writer. The original operation-lab checker explicitly demanded
file deletion and rejects this output. The verifier reports both
`original_lab_structure` and `task_contract_structure`; it never hides that
rejection or changes the old lab's own contract. Scanning unrelated build tools
for `.open` would also overreach this task's production-owner question.

Four negative controls challenged the new verifier: unrepaired mitt and Cedar,
the partial migration, and a product mutation during summary Audit. All were
rejected. Its positive cases include all eight real agent outputs and the valid
forwarding shim. This is evidence about these probes, not universal grading.

## Compare without inventing missing effort

```bash
python3 scripts/compare_trials.py evals/experiments/2026-11-user-outcomes/observations.json
python3 scripts/compare_trials.py evals/experiments/2026-11-user-outcomes/observations.json --json
```

Receipts contain one run per arm/block, a task and subject digest, harness/model/
settings/environment identity, explicit Skill exposure, independently judged
outcome and evidence locators. Each measurement is `observed`, `proxy` or
`unavailable`; the last requires null. Missing arms, failed or blocked tasks and
mismatches stay visible. Only matched, observed measurements produce deltas.
Changing the labels does not authenticate the underlying observations.

For a stronger next study, preregister a small task set and comparable budgets,
randomize arm order, use multiple fresh repetitions, log actual host counters,
and separately time willing owner review. Include clean/no-change decisions and
continuation with later edits. Choose tasks before seeing which arm wins; keep
all run outcomes and setup failures. Start with a few tasks whose ownership or
delivery ambiguity makes RTA plausible, plus ordinary-work controls. Stop or
shorten the method if additional reports and coordination outweigh the observed
decision or repair benefit. Do not run a new model study during ordinary tests.
