# Checkpoints, interruption and recovery

Use this reference for a multi-increment operation, uncertain write completion,
source drift, concurrent work or a resumed session. A small completed operation
needs no permanent run directory or database.

## Keep a minimal private operation record

Record the goal and agreed end state; actual authorization reference and
covered effects; snapshot/input identities; completed obligations and evidence;
current in-flight increment; owned diff/paths and observed side effects; remaining
dependencies; and the next revalidation or execution action. Identify the scope of
any fingerprint (cited files, observed inputs, full export, Git tree). A cited-file
hash is not a full-worktree pin.

Prefer a private host/session artifact outside tracked target content. Use a
small JSON or Markdown record, not a target AUDIT.md backlog. The record is a
recovery aid: it neither establishes permission nor proves its own claims. Do not
store secrets, raw messages, account tokens or unnecessary host paths in it.

## Reconcile before continuing

Resolve the current repository and candidate workspace afresh. Recover the actual
user authority; compare current source, selectors, config, state readers/writers,
build inputs, artifact identities and any relevant external observations with the
last checkpoint. Re-read affected edges, including uncited paths. Reuse unaffected
evidence only at the proof layer and snapshot it actually supports.

For an in-flight increment, determine whether its effects are absent, complete,
partially present, concurrently changed, or unobservable. Inspect before retrying.
A lost acknowledgement cannot justify repeating a data write, remote action or
install. Record an unknown effect explicitly and obtain its decisive observation.
A run record with status=complete does not override current bytes or real state.

## Code recovery and data recovery differ

For task-owned code changes, revert only the owned patch against the known
postimage, preserving user edits. If the postimage no longer matches, stop and
reconcile; no broad reset, clean, force checkout or blindly restored backup.
Do not restore an entire directory to undo one increment. A source commit is not
a backup of the user's dirty/untracked content.

For durable state, determine schema/version compatibility, backup/restore or
compensation path, whether intervening writes occurred, idempotency, and the
point after which code rollback is unsafe. Prefer staged expansion, compatible
readers/writers, verified copy/backfill, selector switch, then separately justified
retirement. This is a strategy, not a requirement for every tiny local change.
Never run it on real data without the relevant authority and actual observations.

For external effects, inspect receipts and current state without replaying the
action. Missing or ambiguous effects can require owner intervention. Do not claim
automatic crash-safe transactions, exactly-once actions or a universal rollback
engine from this protocol. Those require concrete host/adapter implementation.

## Stop in an honest state

- Complete: the whole agreed outcome has current evidence.
- Checkpoint: a coherent increment is verified; the original goal and
  remaining obligations are still recorded.
- Blocked: a specific missing observation, capability, permission or dependency
  prevents the next necessary step. Unrelated safe work may continue in scope.
- Aborted/recovered: state the last known good point, retained partial edits,
  effects actually undone and unresolved effects.

For every non-complete state make resumption actionable without redoing the whole
investigation. This protocol does not itself schedule or perform future work.
