# Behavior evaluation

These cases test whether the Skill reconstructs decision-bearing repository
truth instead of producing a generic repository checklist.

Each case contains:

- `fixture/`: synthetic target repository evidence visible to the target;
- `prompt.md`: the user request visible to the target;
- `case.json`: machine assertions and execution limits; and
- `expected/AUDIT.md`: evaluator-only reference judgment.

The expected artifact is not an instruction surface. It must never be copied
into the target workspace, prompt, Skill context, or target-model transcript.
Fixture self-tests prove only that each synthetic repository still carries its
designed dirty or clean state; they do not claim that a model detected it.

The six cases cover:

1. source tests green while the distributed artifact is stale;
2. a presence-only gate that stays green despite unsafe operation ordering;
3. current product authority contradicted by durable agent instructions;
4. stable release and current development modes that are intentionally split;
5. a vague audit request that must stop for a missing owner decision; and
6. a restore claim whose decisive dependency is external and unobserved.

`activation-prompts.csv` separately protects invocation boundaries. Ordinary
validation and pack self-test make no target-model or network call.
