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
