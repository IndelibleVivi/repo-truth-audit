# Repository Operational Truth Audit — product specification

[简体中文](product-spec.zh-CN.md)

Status: **ACCEPTED FOR COMPLETE IMPLEMENTATION**
Accepted by owner: 2026-08-30
Product form: standalone repository + standalone Codex Skill
Skill name: `repository-operational-truth-audit`

## 1. Product outcome

The product reconstructs the current operational truth of a long-evolved
repository for one concrete owner decision. It follows live, decision-bearing
topology across repository surfaces, validates cross-surface contradictions,
separates intentional multiplicity from shadow paths, and stops when additional
traversal cannot change the decision.

The complete outcome includes:

- a discriminating standalone Skill;
- a stable evidence and stopping contract;
- controlled behavior cases covering dirty and clean outcomes;
- deterministic repository, architecture, and fixture validation;
- a reversible local installation path with source provenance;
- separate English and Simplified Chinese public documentation editions;
- a day-first architecture SVG pair derived from one renderer-neutral semantic
  model;
- accurate user, agent, current-state, and research documentation;
- no ownership or runtime dependency on Softpowers.

## 2. Audit object

Every run binds two things:

1. an exact repository snapshot: physical root, branch, HEAD, working-tree
   state, upstream relation, and relevant submodule/worktree identity; and
2. an owner decision: re-entry, migration, consolidation, safe archival,
   handoff, release readiness, or another decision that makes current
   operational truth material.

If the decision cannot be recovered from the request or repository context,
the Skill performs bounded reconnaissance and asks for that decision. It does
not silently launch an exhaustive audit.

## 3. Truth topology

The Skill may follow these layers only as they become decision-relevant:

```text
claim / authority surface
  -> entrypoint or selector
  -> source, configuration, or durable state owner
  -> generated, built, packaged, or projected artifact
  -> installed or deployed identity, when freshly observable
  -> runtime, edge, device, or owner acceptance, when freshly observable
  -> evidence gate and exact proof boundary
```

Topology controls traversal. Repository size, available scanners, and generic
file categories do not define scope.

## 4. Functional requirements

### ROT-01 — Exact start pin

Before deep traversal, record the physical root, Git root, branch/HEAD,
working-tree state, upstream relation when present, and the selected owner
decision. Preserve concurrent work and do not mutate the target.

### ROT-02 — Authority resolution

Identify current source and instruction owners before treating README, AGENTS,
runbooks, status documents, receipts, generated projections, or historical
notes as truth. Recency, detail, and authorship do not self-authorize a surface.

### ROT-03 — Live-path resolution

Determine reachability through actual selectors: command registration, package
metadata, manifests, imports/callers, build pipelines, service/config owners,
persistence readers/writers, install receipts, or documented operator routes.
A single search miss cannot prove absence.

### ROT-04 — Cross-surface trace

Every material candidate must close this path:

```text
claim or live surface
  -> mechanism / state
  -> contradiction or evidence gap
  -> concrete decision impact
```

Findings without this trace are omitted.

### ROT-05 — False-green detection

Determine what each test, gate, receipt, status line, or successful command
actually observes. A green result is false evidence when the protected contract
can be broken while that result remains green.

### ROT-06 — Artifact and projection identity

Keep canonical source, generated projection, package/distribution artifact,
installed copy, activated runtime, and owner acceptance separate. Verify each
only when the current decision reaches that layer.

### ROT-07 — Intentional multiplicity

Multiple modes or versions remain clean when they have explicit selectors,
isolated state, distinct ownership/version identity, documented purpose, and no
unintended caller. Do not label multiplicity as drift merely because two paths
exist.

### ROT-08 — Shadow-path judgment

Report a shadow path only when it remains reachable, can affect current state or
artifacts, and lacks an intentional current ownership/selection boundary.
Harmless unreachable residue is non-material.

### ROT-09 — External and hidden state

When a repository claim depends on unavailable remote schema, account state,
secret, dashboard setting, deployment, device, or human step, identify the
exact missing observation and whether it can change the decision. Do not invent
a repository defect or flood the result with irrelevant blockers.

### ROT-10 — Private-repository applicability

Re-entry, migration, consolidation, and archival are first-class decisions.
Public-release hygiene must never become a default audit center.

### ROT-11 — Clean result

A clean result names the decision, snapshot, live surfaces checked, proof layers
reached, explicit non-observations, and stopping reason. It stays short.

### ROT-12 — Stopping

Stop when candidate contradictions are adjudicated, no new decision-relevant
evidence edge appears, remaining surfaces cannot change the owner decision, and
the external boundary is explicit.

### ROT-13 — Read-only default

Audit authorization permits analysis, target-local read-only commands, and a
private or explicitly requested report artifact. It does not authorize repair,
target-repository documentation changes, issue creation, commit/push, install,
deployment, remote/account writes, or publication.

### ROT-14 — Specialist adapters

Invoke security, license, dependency, history, agent-surface, or live-system
adapters only when their observation can change the decision. The adapter owns
the observation and limitations; this product owns decision adjudication.

### ROT-15 — No corporate audit machinery

Do not produce maturity scores, universal hygiene checklists, lens matrices,
automatic backlogs, default `AUDIT.md`, reviewer panels, worktree fixers, or
repair loops. Do not turn every unknown into an issue.

### ROT-16 — Overhead receipt

Report the decision-bearing surfaces opened, tests/adapters run, external edges
not observed, and where traversal stopped. The receipt demonstrates topology-
bounded work rather than a low number for its own sake.

### ROT-17 — End re-pin

Re-read HEAD and working-tree state before finalizing. Distinguish task-owned
changes from concurrent user work and narrow any claim whose snapshot moved.

### ROT-18 — Privacy

Keep credentials, private raw evidence, chats, account data, host identifiers,
and unnecessary personal paths out of reports and fixtures. Public-safe case
shapes must be synthetic or redacted.

## 5. Invocation boundary

Positive triggers include explicit operational-truth audit, long-idle repo
re-entry, migration/archive readiness, source/artifact/install reconciliation,
and uncertainty about which path or authority is currently live.

Negative routing includes bounded code review, one-claim verification, known
bug repair, licensing, security/compliance scanning, generic documentation
cleanup, and live-host inspection without a repository-state decision.

Automatic invocation is allowed because the description is discriminating.
The Skill must not attract every request containing the word “audit.”

## 6. Output contract

Lead with the decision answer. Include only sections that carry material truth:

1. audit object and pinned state;
2. current live topology and explicit external boundary;
3. adjudicated findings/unknowns, each with the complete trace;
4. intentional multiplicity and rejected/non-findings when they prevented a
   wrong decision;
5. clean result when applicable;
6. verification and overhead receipt;
7. end re-pin and mutation statement.

Do not force a fixed schema onto a small result. A clean small repository may
need only a few paragraphs.

## 7. Controlled acceptance cases

The repository must retain cases for:

- source tests green while the distributed artifact is stale;
- a presence-only gate that stays green after a safety-order violation;
- durable agent instructions that contradict current product authority;
- stable release and current development modes that are intentionally isolated;
- a vague “full audit” request with no owner decision;
- a restore claim that depends on unavailable external state.

Expected artifacts are evaluator-only evidence. They must never be supplied to
the target Skill as hidden instructions.

## 8. Installation and source identity

Local installation must:

- validate source before mutation;
- refuse a conflicting target unless replacement is explicit;
- stage and atomically replace the Skill directory;
- preserve a replaced target in a recoverable backup;
- record version, source Git commit when available, source dirty state, source
  Skill digest, installed digest, target, backup, and time;
- avoid claiming next-turn discovery from file installation alone.

## 9. Acceptance

Source-complete acceptance requires:

- repository validator passes;
- architecture model, English/Chinese SVG parity, and deterministic render
  checks pass;
- unit and fixture self-tests pass;
- system Skill quick validation passes;
- controlled fixtures are confirmed to carry their intended dirty/clean truth;
- at least one independent forward test reaches a material cross-surface result
  without generic hygiene noise and treats intentional multiplicity cleanly;
- README, AGENTS, product spec, evidence model, current state, architecture docs,
  and changelog agree;
- final diff and Git state are inspected.

Installed acceptance additionally requires an install receipt, exact digest
equality between source and installed Skill, and a clean source commit identity.
Next-turn discovery remains a later observable boundary.

Publication acceptance additionally requires:

- selected layered license texts, path map, and notices agree;
- a public-safety scan finds no private paths, credentials, raw evidence, or
  unrelated material;
- public remote visibility, default branch, and the exact release commit are
  freshly read back;
- CI passes on the public commit;
- the annotated `v0.1.0` tag and GitHub Release resolve to the same peeled
  commit;
- the tagged public Skill path installs to a disposable destination and its
  identity validates; and
- source, commit, push, tag, release, installed bytes, and later discovery
  claims remain separate.
