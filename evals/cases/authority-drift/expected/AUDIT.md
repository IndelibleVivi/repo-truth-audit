# Evaluator reference — authority drift

Decision answer: not safe for unqualified agent re-entry.

The README declares that the product “moved beyond the original MVP” and routes
current identity through `CURRENT_HEAD.json` dated 2026-08-20. Durable
`AGENTS.md` still contains a `Current MVP` instruction that tells an agent to
prioritize only a skeleton and first commits. `docs/status.md` is older
(2026-08-17) and repeats that obsolete stage. Those instructions can change the
next implementation decision, so this is material authority drift, not merely
prose age.

The report should not infer a runtime defect; no runtime was part of this
re-entry decision.
