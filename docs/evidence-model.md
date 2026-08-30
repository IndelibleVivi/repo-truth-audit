# Evidence model

## Evidence must answer a decision

Repository Operational Truth Audit does not collect observations because they
are available. Each command, file read, adapter, or history query must support a
named claim or determine the next live edge.

## Proof layers

Keep these layers separate:

1. claim or instruction surface;
2. source/configuration contract;
3. process-level behavior;
4. generated or distributed artifact identity;
5. installed/deployed identity;
6. exact runtime, edge, device, or account state;
7. owner-observed acceptance.

Evidence at one layer does not automatically prove the next. A test can be
correct and the package stale; the package can be correct and the old installed
copy active; deployment can succeed without owner acceptance.

## Finding trace

A reportable finding has five connected elements:

- **claim/live surface:** the statement, selector, entrypoint, or gate that
  makes the issue relevant;
- **mechanism/state:** the caller, owner, mutation, artifact, persistence, or
  configuration that causes the current behavior;
- **contradiction/gap:** the exact disagreement or missing evidence;
- **impact:** how it can change the current owner decision;
- **validation:** fresh source, command, fixture, or observation that rules out
  a merely hypothetical concern.

Omit candidates that cannot close this trace.

## Adjudication vocabulary

Use only when it helps explain the decision:

- **Validated contradiction:** current live surfaces make incompatible claims
  or produce incompatible behavior.
- **False-green evidence:** a gate remains green when its claimed protected
  contract is broken.
- **Shadow path:** a reachable path can affect current state/artifacts without
  an intentional ownership or selection boundary.
- **Intentional multiplicity:** multiple modes are explicit, isolated,
  versioned/owned, and correctly selected.
- **Non-material residue:** an old surface cannot affect runtime, distribution,
  state, or the current decision.
- **Decision-critical unknown:** missing observation can change the decision.
- **External/environment/policy boundary:** the missing or rejected behavior is
  owned outside the repository mechanism being audited.

These labels are not a score or required report schema.

## False green

For every material green result, ask:

1. What exact input/path did it exercise?
2. What observable outcome did it assert?
3. Would the protected contract being broken make it fail?
4. Which artifact/runtime identity did it actually use?

Mutation proof is useful when it is safe and bounded: deliberately break the
protected invariant in a disposable copy and confirm the gate turns red. Do not
mutate the real target merely to make this point.

## Intentional multiplicity versus shadow paths

Multiplicity is normally intentional when all material questions have clear
answers:

- What selects each mode/version?
- Are their states isolated?
- Who owns each path?
- How is version or artifact identity distinguished?
- Can an unintended caller reach the old path?
- Is retirement or compatibility status current and explicit?

One ambiguous selector or shared state does not automatically prove a shadow
path; trace the actual reachability and impact.

## Unknowns

Write an unknown as:

```text
Missing observation -> claim it prevents -> decision it can change -> exact
fresh observation needed
```

Do not write “runtime unverified” twelve times. Group external boundaries by the
decision they affect. If the missing observation cannot change the decision,
omit it or name it once as out of scope.

## Clean result

A clean result says:

- which decision and snapshot were audited;
- which live entrypoints/selectors and truth owners were followed;
- which proof layer was reached;
- which external boundary remained unobserved;
- why remaining traversal could not change the decision.

Clean does not mean “the repository has no defects.” It means no material
contradiction or decision-critical unknown was found within the explicit object.

## Stopping

Stop when:

- every candidate contradiction is true, false, intentional, non-material, or
  an explicit decision-critical unknown;
- no new decision-relevant evidence edge appears;
- remaining surfaces cannot change the owner decision;
- the clean result or bounded findings can be stated without qualification
  drift;
- start/end snapshot identity is reconciled.
