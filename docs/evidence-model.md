# Evidence and completion model

[简体中文](evidence-model.zh-CN.md)

## Evidence must answer a decision or obligation

Repo Truth Audit does not collect observations because they are available. Each
file read, command, adapter, worker return, or history query must support a named
Audit decision, determine the next live edge, or test an agreed Plan/Operate
obligation.

## Proof layers

Keep these layers separate:

1. claim, instruction, or agreed-outcome surface;
2. source/configuration contract;
3. process-level behavior and state effects;
4. generated or distributed artifact identity;
5. installed/deployed identity;
6. exact runtime, edge, device, or account state;
7. owner-observed acceptance.

Evidence at one layer does not prove the next. Source can be correct while a
package is stale; an installed copy can be correct but inactive; deployment can
succeed without owner acceptance.

Package identity is defined over the declared payload, not every incidental
file below a working or installed directory. Equality of declared-payload
digests proves that selected file set, executable bits, and bytes match. It does
not prove that no runtime cache exists beside an installed payload, that the
Skill was discovered, or that it was activated. Conversely, an all-files digest
can be reproducibly wrong for delivery when ignored runtime residue is copied
and hashed on both sides.

## Audit finding trace

A reportable finding connects:

- **claim/live surface:** the statement, selector, entrypoint, or gate making it
  decision-relevant;
- **mechanism/state:** the caller, owner, mutation, artifact, persistence, or
  configuration causing current behavior;
- **contradiction/gap:** the exact disagreement or missing evidence;
- **impact:** how it changes the current decision or operation;
- **validation:** fresh source, command, fixture, or authorized observation that
  rules out a hypothetical concern.

Omit candidates that cannot close this trace.

## Adjudication vocabulary

Use only when it clarifies the decision:

- **Validated contradiction:** current live surfaces make incompatible claims or
  produce incompatible behavior.
- **False-green evidence:** a gate stays green when its claimed protected
  contract is broken.
- **Shadow path:** a reachable path can affect current state/artifacts without an
  intentional ownership or selection boundary.
- **Intentional multiplicity:** modes are explicit, isolated, versioned/owned,
  and correctly selected.
- **Non-material residue:** an old surface cannot affect runtime, distribution,
  state, or the current decision.
- **Decision-critical unknown:** missing observation can change the decision or
  a required operation obligation.
- **External/environment/policy boundary:** another owner or unavailable
  environment governs the missing observation.

These labels are not a score or mandatory report schema.

## False-green and anti-self-certification

For material green evidence, ask:

1. What exact input and selected path did it exercise?
2. What observable outcome and state effect did it assert?
3. Would the protected contract being broken make it fail?
4. Which source, artifact, installation, or runtime identity did it use?

Mutation proof is useful only in a safely controlled disposable subject. In an
Operate workflow, tests may legitimately change, but removing assertions,
adding skips, broadening tolerances, or regenerating expectations does not prove
the candidate. Accepted behavior changes require their own explicit witness.

A cited-byte match proves only the named bytes. A JSON schema pass proves only
shape. Neither proves semantics, authority, completion, or safe execution.

## Checkpoint versus whole-goal completion

A checkpoint is a coherent increment with current evidence at its claimed
layer. It can be retained and resumed. It is not completion when the original
agreed outcome still has unresolved callers, state owners, selectors,
artifacts, compatibility, retirement, or delivery obligations.

Completion requires current evidence for every applicable obligation:

- **Behavior:** agreed outputs, failures, compatibility, and state effects.
- **Structure:** the intended ownership/dependency change or retirement, not
  merely a new facade or file.
- **Delivery:** every requested manifest, package, installed, activation, or
  runtime surface selects the intended implementation.
- **Usefulness:** where material and practical, a follow-on change demonstrates
  that the original change pressure is reduced.

Exclusions are justified against the agreed goal. Passing a broad suite does
not erase an applicable structural or delivery obligation.

## Challenge and independence

Consequential completion claims should be challenged from current source with
the strongest plausible counterexample: old owner still selected, stale artifact,
duplicate state write, compatibility break, or unchanged change pressure.

Record whether the challenge was independent or a same-agent self-check. An
independent reviewer adds evidence but is not a mandatory panel for every small
change. Reviewer confidence, worker completion, and green CI remain claims until
reconciled with the actual diff and required proof surfaces.

## Recovery evidence

An operation record preserves provenance and resumption context; it does not
prove freshness or permission. On resume, classify an in-flight effect as
absent, complete, partial, concurrently changed, or unobservable before retry.

Code recovery is bounded to task-owned changes whose current postimage still
matches. Durable-state recovery needs schema/version compatibility,
backup/compensation, intervening-write, idempotency, and safe-rollback evidence.
A lost acknowledgement never proves that an external or data effect did not
happen.

## Unknowns

Write an unknown as:

~~~text
Missing observation -> claim or obligation it prevents -> decision or outcome
it can change -> exact fresh observation needed
~~~

Group unknowns by the decision they affect. If missing observation cannot change
the decision or agreed operation result, omit it or name it once as out of
scope.

## Clean audit and terminal operation states

A clean Audit result names the decision and snapshot, live selectors and truth
owners followed, proof layers reached, external boundary not observed, and why
remaining traversal cannot change the decision. It does not claim the repository
has no defects.

An Operate result is one of:

- **Complete:** the whole agreed outcome has current evidence.
- **Checkpoint:** a coherent increment is verified and remaining obligations are
  explicit.
- **Blocked:** a specific missing observation, capability, authority, or
  dependency prevents the next required step.
- **Aborted/recovered:** last known good state, retained edits, effects actually
  undone, and unresolved effects are explicit.

## Stopping

Audit stops at its decision fixed point. Plan stops when the finite outcome,
sequence, witnesses, authority boundaries, recovery, and unresolved decisions
are decision-ready. Operate stops only at Complete or an honestly reported
Checkpoint, Blocked, or Aborted/recovered state. Start/end identity is reconciled
for every mode.
