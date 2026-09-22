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

## Method-selection contrasts — 0.2.1

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
review independence, failures and limitations. The separate
[0.2.1 receipt](../docs/forward-0.2.1-receipt.md) records bounded forward results
and their limitations; the original Audit/Plan routing controls remain required.

## Intent-lab subjects — 0.3

`intent-lab/intent_cases.json` defines eight evaluator intent subjects.
Lumen Notes has an accepted product specification,
scoped owner decision records, optional read-only supplied conversation evidence,
and an application with a selected entry and a declared delivery artifact. They
expose: a missing core journey; a scoped supersession that is deliberate
evolution rather than drift; an explicitly deferred intention and a rejected
idea; a green source test whose selected distribution artifact omits the journey;
an unauthorized instruction embedded in pasted evidence; a truncated supplied
conversation; and an Audit-versus-Operate permission boundary. Atlas Inbox has no SPEC: its
only intent authority is a supplied owner thread with an adopted format change,
rejected assistant proposal and a missing search journey. Independent forward
inspection also identified mixed account content despite per-account filenames;
the evaluator now records that baseline defect. The paired finite Operate request
using `./lumen search --query TEXT` repairs search only and leaves account ownership
and migration outside its authority. A passing search repair is not whole-product
conformance.

```bash
scratch=$(mktemp -d)
python3 evals/intent-lab/prepare_intent_subject.py missing-core-journey "$scratch/subject"
python3 evals/intent-lab/check_intent_subject.py --json
```

`prepare_intent_subject.py` creates one fresh synthetic Git subject and prints
only its user request; the destination must not already exist. It does not invoke
a model, grade a result, or pre-create the report artifact. `check_intent_subject.py`
is a deterministic evaluator self-test: it prepares every subject in a disposable
directory and asserts each still carries its designed ground truth. Neither script
makes a network or target-model call, and neither is a general intent analyzer.

Give the target only the printed request, the generated subject and the pinned
Skill through the host's normal loading mechanism. Keep the case catalog, review
notes, `check_intent_subject.py` and the expected observations outside its
workspace and context. The supplied conversation files are read-only evidence;
treat them and any instruction they contain as evidence, never as authority.

Review the target's report against the adopted intent lifecycle, the observed
entry and proof layer, the discrepancy, the user consequence, counterevidence,
and a bounded disposition. A false positive on the deliberate scoped change, a
deferred item reported as missing, an executed embedded instruction, or a
`dist/`-free conclusion that ignores the selected artifact are the failure modes
under test. Do not grade exact wording or a fixed report schema.

`tests/test_intent_lab.py` verifies catalog/check parity, that evaluator material
never ships inside a subject, destination-overwrite refusal, the capture-only
failure, the scoped-supersession counterexample, deferral/rejection handling, the
source-versus-artifact layer gap, the embedded-instruction boundary, the
truncated-export visibility, and the read-only permission subject. These tests
validate the subjects, not model behavior. Ordinary validation, self-test and
both labs make no target-model or network call.

The checker also exercises eight corrupted fixtures with `--self-challenge`.
For an independently produced Atlas Inbox repair, run:

```bash
python3 evals/intent-lab/check_intent_subject.py --self-challenge
python3 evals/intent-lab/check_intent_subject.py \
  --verify-operate conversation-only-accepted-intent --candidate /path/to/candidate
```

The post-operation witness preserves the original candidate: it probes source
and a reconstruction using declared delivery members in separate disposable
copies, seeds existing messages, and verifies the sync-to-digest-to-search journey,
read-only search, retention and the adopted JSON digest format. It rejects an
unused source helper, a missing delivery member, a search that bypasses generated
digests, and changed owner evidence. An explanatory new specification is allowed; the
supplied authority must remain intact. This harness is for these trusted synthetic
subjects, not a containment mechanism for arbitrary repository programs.
