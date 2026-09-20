# Behavior and operation evaluation

The original cases test whether Audit reconstructs decision-bearing repository
truth instead of producing a generic checklist. The separate operation lab
tests whether deterministic witnesses can distinguish a safe checkpoint from
whole-goal completion; it does not test autonomous model behavior.

Each case contains:

- `fixture/`: synthetic target repository evidence visible to the target;
- `prompt.md`: the user request visible to the target;
- `case.json`: machine assertions and execution limits; and
- `expected/AUDIT.md`: evaluator-only reference judgment.

The expected artifact is not an instruction surface. It must never be copied
into the target workspace, prompt, Skill context, or target-model transcript.
Fixture self-tests prove only that each synthetic repository still carries its
designed dirty or clean state; they do not claim that a model detected it.

The six read-only cases cover:

1. source tests green while the distributed artifact is stale;
2. a presence-only gate that stays green despite unsafe operation ordering;
3. current product authority contradicted by durable agent instructions;
4. stable release and current development modes that are intentionally split;
5. a vague audit request that must stop for a missing owner decision; and
6. a restore claim whose decisive dependency is external and unobserved.

`activation-prompts.csv` protects Skill invocation boundaries.
`mode-prompts.csv` records Audit / Plan / Operate / reconnaissance routing
expectations and the rule that target mutation belongs only to explicit Operate.
These CSV controls describe evaluator expectations; file presence does not prove
that a model follows them.

`operation-lab/run_operation_lab.py` applies evaluator-authored known edits to a
synthetic manifest-selected CLI. It protects behavior, structure, declared
artifact selection, preservation of unrelated content, drift detection,
selective code recovery, and a small usefulness probe. The first extraction is
deliberately only a checkpoint; the second increment switches the actual
selector and retires the legacy owner.

The lab's known patches and assertions are evaluator material, not target
instructions. A PASS proves only that this harness and its counterexamples ran.
It does not prove model mode inference, planning, safe editing, arbitrary
refactoring, durable-data migration, installation, or production behavior.

Ordinary validation, pack self-test, and the operation lab make no target-model
or network call.

## Method-selection contrasts — 0.2.1 candidate

`operation-lab/method_choice_cases.json` defines six evaluator cases.
`operation-lab/prepare_method_choice.py` creates one fresh synthetic Git subject
and prints only its user request. It does not invoke a model or grade a result.
The optional test-first policy is original synthetic material, not an external
Skill copy or a reproduction of the private project in issue #4.

```bash
scratch=$(mktemp -d)
python3 evals/operation-lab/prepare_method_choice.py retire-optional-test-first "$scratch/subject"
```

The destination must not already exist. The script creates a synthetic baseline;
selected cases then contain a modified tracked adapter and unrelated untracked
owner notes. Git and temporary directories are not an OS sandbox. Use suitable
host controls for actual agent execution and do not expose real owner data.

Give the target only the printed request, the generated subject and the pinned
Skill through the host's normal loading mechanism. Keep the case catalog, review
criteria, fixture builder and unit-test reference edits outside its workspace
and context. Retain protected before-images separately from target-writable data.

Compare baseline and candidate Skill bytes in fresh sessions under the same
host, model and settings. Pair the no-helper and optional-helper cases on their
identical application bytes; record whether the helper was actually read. An
available-but-unread helper does not test response to its instructions. Keep
project-required test-first as a separate authority condition. Do not substitute
those runs for one another or infer causation from a single uncontrolled session.

Review actual source/config/test changes, chosen selectors, built bundle members,
ledger effects, observed RED/GREEN commands and retained infrastructure. Preserve
the valid existing behavior; a setup failure is not a defect witness. Both a
small structural check and a justified lasting regression are admissible. Do not
score a test/file count, exact final wording or a claim that costs were considered.
A stage falsely called complete while its old selector remains must be rejected.

The complaint follow-up is a second read-only turn on the actual resulting
candidate. Evaluate whether the agent reconciles its diff and evidence, retains
supported gains and corrects a real shortfall. Test an incomplete candidate as a
contrast rather than teaching a fixed reassuring answer. Record any evaluator
preparation of that contrast; it is not an agent's earlier work.

`tests/test_method_choices.py` verifies fixture separation, false-green state
effects, a known valid retirement and its broken-selector counterexample, actual
project-policy placement, dirty Git inputs and refusal to overwrite a destination.
These six tests validate the subjects, not model behavior. Any future forward
receipt must state exact identities, actual helper exposure, observed changes,
review independence, failures and limitations. No 0.2.1 forward result is claimed
by the current files; the original Audit/Plan routing controls remain required.
