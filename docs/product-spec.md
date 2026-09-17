# Repo Truth Audit — product specification

[简体中文](product-spec.zh-CN.md)

Status: **IMPLEMENTED AND RELEASED — v0.2.0**
Expanded scope accepted by owner: 2026-09-17
Source version: 0.2.0
Latest public release: v0.2.0
Product form: standalone repository + standalone Codex Skill
Skill name: repository-operational-truth-audit

## 1. Product outcome

Repo Truth Audit recovers the current operational truth of a long-evolved
repository for a concrete owner decision. When the user explicitly asks for a
structural change, the same product can continue from diagnosis through a finite
plan, authorized implementation, recovery-aware checkpoints, and verified
completion.

The product keeps three request-derived modes:

- **Audit:** read-only reconstruction and decision answer;
- **Plan:** a finite change outcome and executable sequence without target edits;
- **Operate:** an explicitly authorized structural change carried through its
  agreed evidence boundary.

These are behavior modes, not CLI subcommands. Audit remains read-only by
default. Operate does not create a second coding-agent platform: it uses the
host's editors, tests, Git policy, workers, and real permission controls while
retaining responsibility for the agreed outcome and evidence.

## 2. Engagement object and authority

Every run binds an exact repository snapshot and a concrete owner decision or
change outcome. Record the physical and Git roots, branch/HEAD, working tree and
index state, relevant untracked inputs, upstream relation, and material
worktree/submodule identity.

Infer Audit, Plan, or Operate from the request. “Inspect only” remains Audit;
“give me a plan” remains Plan; an explicit request to implement, refactor,
extract, consolidate, replace, or retire may enter Operate. Ambiguous cleanup
language permits bounded reconnaissance only until the ambiguity affecting
write authority or the intended end state is resolved.

An Operate request may cover the ordinary reversible source, test,
documentation, integration, and superseded-source retirement work needed for
its agreed local outcome. Public API removal, durable-data migration or
deletion, production activation, privileged host changes, paid calls,
installation, account actions, publication, and other materially new effects
need matching authority. A Skill, plan, report, worker, receipt, or state file
cannot create permission.

## 3. Shared operational-truth method

Audit, Plan, and Operate begin from the same decision-bearing topology:

~~~text
claim / authority surface
  -> actual entrypoint or selector
  -> source, configuration, or durable-state owner
  -> generated, built, packaged, or projected artifact
  -> installed or deployed identity, when freshly observable
  -> runtime, edge, device, account, or owner acceptance, when authorized and observed
  -> evidence gate and exact proof boundary
~~~

Traversal follows edges that can change the decision or operation. Repository
size, scanner availability, file age, and generic hygiene categories do not
define scope.

### ROT-01 — Exact pin

Pin the selected object before deep work, preserve concurrent work, and re-pin
before every completion claim.

### ROT-02 — Authority resolution

Identify current source, instruction, state, artifact, and operator owners.
README, AGENTS, runbooks, status files, historical notes, generated projections,
and installed copies are not interchangeable.

### ROT-03 — Live-path resolution

Resolve reachability through real selectors, registrations, manifests,
callers/imports, build pipelines, persistence readers/writers, install receipts,
and operator routes. A search miss does not prove retirement.

### ROT-04 — Material finding trace

Every finding closes claim/live surface -> mechanism/state -> contradiction or
evidence gap -> decision impact -> fresh validation. Omit candidates that cannot
close the trace.

### ROT-05 — False-green challenge

For material green evidence, identify the exact input/path, assertion, proof
layer, and whether breaking the claimed invariant makes the gate fail. Mutation
proof belongs only in a safe disposable subject under real host controls.

### ROT-06 — Layer separation

Keep source, artifact, installation, activation/runtime, and owner acceptance
separate. Evidence at one layer never silently proves the next.

### ROT-07 — Multiplicity and retirement

Multiple versions or modes can be correct when selectors, state, ownership,
identity, callers, and compatibility/retirement status are explicit. Unreachable
residue is not automatically material; reachable unowned paths require tracing.

### ROT-08 — External unknowns

State an unknown as missing observation -> prevented claim -> affected decision
or operation -> exact fresh observation needed. Unobserved external state is not
automatically a repository defect.

### ROT-09 — Bounded specialists

Security, licensing, dependency, history, worker, or live-system tools may
supply bounded observations or implementation work. This product owns their
reconciliation and never inherits an external verdict or greater permission.

### ROT-10 — Audit fixed point

Audit stops when all material candidates are adjudicated, no new
decision-relevant edge appears, remaining surfaces cannot change the decision,
external boundaries are explicit, and the ending snapshot is reconciled.

## 4. Plan and Operate contract

### ROT-11 — Finite end state

Define the actual change pressure and a testable end state. File length, old
names, or two legitimate versions do not by themselves justify a refactor.
Separate observed behavior from desired behavior and record deliberate changes.

### ROT-12 — Honest candidate workspace

Account for staged, unstaged, untracked, ignored, generated, and configured
inputs that affect the selected path. A worktree or temporary copy organizes
work; it is not network, credential, process, resource, or external-state
isolation.

### ROT-13 — Protected witnesses

Establish relevant valid, failure, compatibility, and state-effect witnesses
against the actual shipping selector. Keep baseline behavior witnesses distinct
from structural-completion checks. Do not weaken assertions, add skips, broaden
tolerances, or regenerate expectations merely to make a candidate pass.

### ROT-14 — Convergent increments

Use the smallest coherent increments that converge on the agreed whole goal.
Each increment has protected behavior, edit scope, required observations, and a
code/state recovery route. Temporary bridges need real selectors, state
ownership, purpose, and a retirement condition.

### ROT-15 — Checkpoint is not completion

A verified increment may be retained as a checkpoint. It does not complete a
larger agreed outcome while callers, state owners, delivery selectors, or
retirement obligations remain. Budget exhaustion narrows status, not the goal.

### ROT-16 — Implementation loop

Before each write, reconcile the current dependencies with the last verified
checkpoint. Implement one coherent increment, inspect the real diff and test
edits, run current behavioral and structural checks, challenge consequential
claims from current source, re-pin, and continue through ready in-scope
obligations. Re-plan on new evidence rather than stacking speculative fixes.

### ROT-17 — Four acceptance obligations

Apply the obligations material to the agreed goal:

1. **Behavior:** outputs, failures, compatibility, and state effects are correct,
   including explicitly agreed changes.
2. **Structure:** the intended owner separation, dependency removal, selector
   migration, or retirement actually occurred; a delegating facade is a
   transition, not completion.
3. **Delivery:** requested manifests, packages, installed copies, activation, or
   runtime surfaces select the intended implementation at every included layer.
4. **Usefulness:** the concrete change friction is reduced; when practical, a
   small disposable follow-on change demonstrates the new boundary.

Not every operation includes all delivery layers or a usefulness probe. Name
which obligations apply and justify exclusions against the agreed goal.

### ROT-18 — Challenge without theatre

Consequential completion claims receive a current-source attempt to disprove
them. Record whether that challenge was an independent review or a same-agent
self-check. Do not default to multi-agent fan-out, and do not present a format
validator or byte match as semantic review.

### ROT-19 — Recovery-aware continuity

Long or interrupted operations keep one minimal private record outside tracked
target content: goal, authority boundary, input identities, completed
obligations/evidence, in-flight increment, owned changes/effects, remaining
dependencies, and next revalidation action. It is a recovery aid, not permission
or proof.

Resume by observing actual source and effects before another write. A lost
acknowledgement does not prove absence of effect. Code recovery applies only to
task-owned changes against a known postimage; concurrent edits force
reconciliation. Durable-state recovery additionally requires compatibility,
backup/compensation, intervening-write, idempotency, and safe-rollback analysis.

### ROT-20 — Honest terminal states

Report one of: complete agreed scope; verified checkpoint with work remaining;
blocked with the exact missing observation/capability/authority/dependency; or
aborted/recovered with observed residual effects. Do not silently shrink scope.

## 5. Evidence and deterministic helpers

The optional cited-byte checker validates only named file and line-range bytes.
It does not establish semantics, Git identity, a full-worktree or atomic
snapshot, safe execution, authorization, equivalence, or completion. Unsupported
secure-read platforms fail closed.

The controlled operation lab applies evaluator-authored known edits to a
synthetic repository. It must reject facade-only completion, unused replacement,
stale declared artifacts, duplicate side effects, source drift, unsafe replay,
and broad recovery. A passing lab proves the evaluator and counterexamples run;
it does not prove autonomous model performance, arbitrary refactoring ability,
real data migration, or production safety.

Unknown target-controlled builds, package hooks, and probes require suitable
host-enforced write, network, environment, and resource controls. A timeout,
temporary directory, worktree, “dry run,” or permission field is not such a
boundary by itself.

## 6. Output contract

Audit leads with the decision answer and includes only material topology,
findings/unknowns, rejected non-findings, proof limits, overhead receipt, and
end re-pin.

Plan names the finite end state, preserved and deliberately changed behavior,
authority boundary, dependency order, witnesses, acceptance obligations,
recovery strategy, stop conditions, and unresolved decisions. It does not edit.

Operate leads with the user outcome, meaningful changes, preserved and agreed
behavior changes, decisive checks with source identities, completion layer,
remaining unknowns, and final workspace state. It distinguishes source, commit,
push, install, activation, runtime, release, and owner acceptance.

## 7. Controlled acceptance

Retain the six original read-only dirty/clean cases and their negative routing
controls. Add deterministic cited-evidence and operation-lab tests without
leaking evaluator-only expected artifacts or known patches into Skill context.

Source-complete acceptance for 0.2.0 requires:

- repository, architecture, unit, fixture, operation-lab, Skill, and whitespace
  validation;
- request routing that preserves Audit, Plan, and Operate boundaries;
- a real target-model Audit regression and a model-authored multi-increment
  Operate forward test evaluated independently from protected witnesses;
- bilingual README, AGENTS, product spec, evidence model, architecture docs,
  current state, changelog, and runtime metadata agreement;
- final diff and Git-state inspection.

Synthetic operation-lab success is necessary evaluator evidence, not a
substitute for model forward evidence.

## 8. Version, installation, and publication

VERSION identifies the current source version and follows stable semantic
version syntax. It may diverge from a later public release tag during future
development. For this release snapshot, source version and latest public tag
both identify 0.2.0; README and current-state still report their gates separately.

Local installation validates source, requires explicit replacement of different
bytes, preserves a recoverable backup, and records source Git identity, dirty
state, version, and source/installed digests. Installation does not prove
next-turn discovery or activation.

One explicit declared file set defines the installable Skill payload for source
validation, digesting, staging, installed comparison, and receipts. Known local
runtime residue is outside that payload and is never staged; other undeclared
source or executable entries fail closed. A matching source/installed digest
therefore proves equality of the declared payload only, not activation or the
absence of post-install runtime residue.

Commit, push, CI, annotated tag, GitHub Release, tagged install, installed bytes,
runtime discovery, and owner acceptance are separate gates. This specification
does not authorize installation, release, deployment, account mutation, or
publication.

## 9. Non-goals

Do not produce maturity scores, universal hygiene checklists, automatic issue
backlogs, provider panels, mandatory multi-agent review, a second scheduler or
orchestration engine, universal crash-safe rollback, exactly-once external
effects, or loop-until-clean repair. Keep one canonical Skill implementation and
the existing invocation slug.
