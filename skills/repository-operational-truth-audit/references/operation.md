# Operate — own a structural-change outcome

This reference covers both a plan and an authorized operation. Plan mode first
uses audit.md when current topology has not already been established, then
produces an implementation-ready end state, sequence, recovery boundary and
acceptance contract. It may inspect and propose commands, but it does not run
target-mutating commands and carries no latent implementation authority. In
Operate mode, remain responsible through the agreed acceptance surface; do not
stop after listing findings or a first cut.

## Choose the outcome before the technique

Identify actual change pressure: additional behavior repeatedly crosses unrelated
owners; a selected legacy path shadows a replacement; shared state prevents
separation; a distribution runs different code from the tested implementation.
File length, old names and the existence of two versions do not prove a defect.

Make the end state testable. “Separate formatting from durable writes while
preserving every supported CLI entry, then retire the old writer from current
distribution” is finite. “Clean everything” is not. Retained compatibility paths
may be correct. Distinguish observed existing behavior from desired behavior:
characterization must not quietly bless a bug or forbid an explicitly requested
behavior change. Record deliberate deviations before implementing them.

Consider a direct local refactor, extraction behind an existing seam, gradual
replacement with routing, consolidation, or deliberate retention. Use temporary
adapters only when their risk reduction earns their cost. Do not force a facade,
strangler migration, plugin system, service split or rewrite onto every target.
Explain the most credible objection to the chosen strategy. Include lasting
verification infrastructure in this choice: tests, fixtures, configuration,
startup branches and injection seams also need a present purpose. Prefer an
adequate existing seam over building a new subsystem merely for this operation;
keep new infrastructure when the actual risk or continuing contract warrants it.
A brief concrete rationale is enough, not a proof of globally minimal cost.

## Resolve authority once, escalate on changed effects

Operate applies only after the router has established a repository-level or
cross-surface structural-change problem. An isolated known-bug repair, ordinary
code review, one-claim verification, or generic hygiene request with no
repository-topology question stays in the host's normal bounded engineering
workflow; explicit edit intent does not override that product boundary.

An explicit implementation request supports ordinary local edits needed for that
outcome, including relevant tests/docs and retirement of superseded source.
Infer this bounded scope from the request; do not require a click per file.
Preserve unrelated user work. Scope-changing public-API removals, durable-data
migration/deletion, production activation, paid service calls, privileged host
changes and publication require corresponding real authorization.

A model-authored plan or a JSON permission field cannot create permission.
Re-read the live request/host authorization when resuming. Record what it covers
and where execution stops. Delegated workers receive no greater powers than
the lead and cannot independently widen the write or delivery boundary.

## Operate only — prepare an honest candidate workspace

Resolve staged, unstaged, untracked, ignored configuration and generated inputs
that affect the selected path. A HEAD checkout omits dirty work; do not test it
and present that as testing the user's actual candidate. Preserve unrelated and
concurrent dirty work; keep recoverable before-images for task-owned changes.
When the owner authorizes cleanup of selected uncommitted work, evaluate its
keep/change/retire choices rather than treating every dirty implementation as
permanent. Do not silently stash, reset, force-checkout or commit owner work.

Use an isolated worktree/export when beneficial, or an explicitly understood
in-place workspace. A worktree is a workspace organization tool, not a security
sandbox; Git metadata can be shared. Record the actual inputs copied/excluded.
Never copy credentials or private caches just to make tests convenient.

Separate control evidence from target-controlled outputs. Keep a trusted copy of
baseline witnesses and applicable obligations outside the writer's editable area
when practical; digests detect drift but do not enforce access control. If the
host cannot isolate a target test's writes, network, environment and resources,
do not present that test as safe to execute on untrusted code. Already trusted
owner-authored local checks may use the owner's established host policy with
its actual limitations recorded. Do not weaken a needed containment boundary
for an unknown package script, install hook or generated probe.

## Operate only — establish behavior and structural witnesses

Before changing implementation, exercise or inspect the actual shipping selector,
not just a convenient new function. Choose relevant valid, failure, compatibility,
and persistence observations. Record exit codes, outputs, state effects and
error ordering as appropriate. Use immutable fixture data or a copied disposable
state for replay. Never dual-run live mutating handlers on the same real data to
compare behavior; isolate each state or capture side effects without publishing.

Choose sufficient evidence for the affected risk: existing checks, direct
inspection, a disposable probe or a durable regression test. A behavior-preserving
refactor may start and end with green baseline tests. A defect repair needs a
witness that exposes the defect; a compile/setup failure alone is not that witness.

Keep baseline behavior separate from structural completion. Completion evidence
must reject a forbidden old owner, import edge, selected artifact or shared state
writer. For a directly inspectable retirement, trace selectors, callers and
packaging; do not build a permanent test harness just to restate that trace. When
an executable gate carries a consequential claim, challenge it with a representative
counterexample in a safe disposable copy where feasible. If that observation is
unavailable, state the resulting proof limit rather than treating green as enough.

Existing failures are classified before edits. Do not claim a regression is
pre-existing without baseline evidence. Do not delete assertions, skip failures,
regenerate expected outputs or broaden tolerances merely to get a green result.
A user-agreed behavior change may revise a witness; record why and validate the
revised contract separately from the refactor itself. Tests may also be consolidated
or retired with obsolete contracts: preserve distinct failure coverage for supported
behavior and update the real test entrypoints. Test count is not the objective.

## Plan increments that converge

Keep the agreed end state intact and identify its blocking dependencies. Use a
short ordered sequence or small dependency graph only when it helps execute.
Every increment names its semantic change, likely edit paths, protected paths,
required observations and a code/state recovery route. Do not use file-count or
line-count quotas as the definition of safety or progress.

A temporary bridge must have explicit selectors, state ownership and a retirement
condition. A completed bridge step does not complete replacement. Evidence that
no change is needed can close a proposed increment, but cannot silently erase an
agreed outcome. If the outcome itself should change, expose that decision.

## Operate only — the implementation loop

For each ready increment:

1. Reconcile its current source/config/selector/state inputs with the last
   verified checkpoint. If they moved, inspect the changed dependency edges.
2. Establish any missing witness, then implement one coherent increment using
   the host editor/patch tools. Keep shared state owners under one writer.
3. Inspect the actual diff, including deletes, test edits, manifests, generated
   projections and out-of-scope changes. Do not trust a worker summary as a diff.
4. Run the relevant before/after and structural checks under actual host controls.
   Build and test the delivery artifact when that is part of the contract.
5. Challenge consequential changes from current source. A fresh reviewer must
   re-read the selected path and try to disprove completion, not rubber-stamp the
   implementer's rationale. Record independence honestly; a same-agent reread is
   a self-check. Missing independent review does not block every low-risk edit,
   but cannot be reported as performed or bypass a required high-risk gate.
6. Re-pin, retain the smallest useful checkpoint and continue to the next ready
   obligation while scope and budget permit. A materially changed patch needs
   renewed affected checks; a previous approval does not cover its new bytes.

Do not require a commit per increment. Local commits, branch changes, PR creation,
push, merge and release follow the owner's actual Git policy. A verified patch
and private checkpoint can be enough. Never stage unrelated files.

If tests expose a new material dependency, re-plan rather than retrying the same
failing edits indefinitely. Reassess when verification setup starts dominating the
operation: compare the narrower credible route and expose a material scope/cost
change before continuing. Do not restart a whole workflow for each helper. On
budget exhaustion, leave a verified checkpoint or
state exactly which partial edits remain. Do not restart a fresh large audit
merely because a context window ended. See recovery.md.

## Operate only — verify the actual end state

Reconcile four obligations, scoped to the agreed goal:

- **Behavior:** required outputs, failure behavior, compatibility and state effects
  remain correct, including explicitly agreed changes.
- **Structure:** the intended owner separation, dependency removal or retirement
  occurred; a facade still delegating to the old owner is a transition only.
- **Delivery:** manifests/build/package/install/activation routes select the
  intended implementation at every surface included in the request.
- **Usefulness:** the concrete change pressure has eased, with new maintenance
  obligations accounted for. Name retired responsibilities or reduced change
  coupling and the purpose of retained tests, configuration and bridges. Where
  useful, try a small disposable follow-on change without touching unrelated
  owners. Do not use fewer lines, more tests or future reuse alone as proof.

Not every operation needs runtime deployment evidence or a follow-on probe. Name
which obligations apply and justify exclusions against the goal. A coherent large
module may remain. Intentional stable and development paths retain their owners.
Judge the agreed phase; do not demand whole-project maintenance measurements or
separate approval for every test. If the user questions a result, reconcile the
original scope, categorized diff and actual checks before revising the conclusion.
Disclose a confirmed shortfall and retain supported gains; do not manufacture
failure from a line-count increase or dismiss a concern because tests passed.

Update current source docs, operator instructions, accepted architecture and
checks affected by the actual result. Retire temporary bridges when the contract
requires it; otherwise report their continuing purpose and exit condition.
Complete only at the agreed evidence boundary, with a final snapshot and mutation
statement. If blocked at installation, a source success remains source success.

## Use tools without inheriting their verdict

Optional byte anchors from scripts/check_evidence.py validate only the cited
bytes. They do not establish full-worktree identity, semantic freshness, safe
patching, authorization, equivalence or a cross-file atomic snapshot. Do not
refresh expected hashes simply to make old evidence pass. Inspect changed
selectors and callers even when old cited implementation bytes still match.

A specialist review tool can supply a bounded defect observation. A worker
router can supply isolated work. This product owns their reconciliation into the
operation's goal and acceptance. Before choosing an auxiliary Skill or workflow,
identify the current gap it addresses and assess its prerequisites, persistent
machinery and completion gates, even if its wording does not directly conflict
with the task. Read access or an agent's method choice alone does not adopt every
coverage target, commit cadence, RED phase or delivery obligation it describes.

Follow requirements genuinely applicable through the host, user or project. Do
not claim this Skill overrides them. If a selected helper requires an indivisible
workflow that does not fit, choose another method; do not silently claim compliance
with a workflow whose required steps were skipped. Resolve a real conflict or
material scope/cost change with the owner, while making ordinary in-scope method
choices without repeated approval. No external engine or multi-agent panel is a
mandatory runtime dependency.
