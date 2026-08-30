# Repository Operational Truth Audit

[简体中文](README.zh-CN.md)

A standalone, read-only-first Codex Skill for reconstructing what a
long-evolved repository actually operates through **today** before an owner
makes a re-entry, migration, consolidation, safe-archive, handoff, or
release-readiness decision.

Current release: `v0.1.0`

This is not a generic repository score or a public-launch checklist. It follows
decision-bearing entrypoints, selectors, authority owners, durable state,
derived artifacts, installed identities, evidence gates, and explicit external
proof boundaries. It returns validated contradictions, intentional
multiplicity, non-material residue, decision-critical unknowns, or a concise
clean-within-scope result—and then stops.

## What problem it solves

Ordinary code review begins with a bounded change. Ordinary verification begins
with a named claim. Repository Operational Truth Audit is for the moments when
neither starting point is sufficient:

- Which path is actually live after months away from this repository?
- Before a migration or safe archive, which source, state, package, and
  installed identities still matter?
- Do source, generated artifacts, distribution packages, installed copies,
  documentation, and tests describe the same operational path?
- What layer does a green test or receipt actually prove—and could the claimed
  contract be broken while that evidence stays green?
- Are two modes intentionally selected and isolated, or is one an unowned
  shadow path?
- If a restore or release claim depends on an unavailable remote schema,
  secret, dashboard setting, device, or human step, how far can the current
  decision honestly go?

## Architecture: what this diagram serves

The diagram answers one public-reader question:

> How does one read-only audit turn a concrete owner decision and an exact
> repository snapshot into a decision-bounded answer without crossing
> unobserved external boundaries?

It depicts the **audit runtime contract**. Packaging, installation, and release
of this Skill are deliberately excluded as a separate reader job.

![Repository Operational Truth Audit runtime architecture](docs/architecture/audit-runtime.en.svg)

The renderer-neutral model, stable semantic IDs, evidence mapping, and localized
artifact contract live in [`docs/architecture/`](docs/architecture/README.md).

## When to use it

Use this Skill when a concrete decision depends on reconstructing current
repository topology, especially for:

- long-idle repository re-entry;
- migration, machine move, consolidation, or archival readiness;
- source / generated artifact / package / installed-copy reconciliation;
- authority drift across current product docs, durable agent instructions,
  runbooks, status surfaces, or receipts;
- false-green gates whose assertions may not cover their claimed contract;
- ambiguous stable/development, legacy/current, local/remote, or
  source/deployment paths; or
- a repository claim whose decisive external state is currently unobserved.

## When not to use it

Use a narrower owner for:

- reviewing a diff, commit, branch, or pull request;
- verifying one already-defined claim;
- repairing a known bug;
- a dedicated license, security, compliance, or dependency audit;
- generic repository hygiene or documentation cleanup; or
- inspecting or changing a live host, account, database, browser, deployment,
  or owner-controlled surface without a repository-state decision and explicit
  authorization.

An audit request is read-only by default. It does not authorize fixes, commits,
pushes, installation, deployment, remote writes, account actions, or
publication.

## Install from the public release

Use the system Skill installer and pin the release tag:

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-installer/scripts/install-skill-from-github.py" \
  --repo IndelibleVivi/repository-operational-truth-audit \
  --path skills/repository-operational-truth-audit \
  --ref v0.1.0
```

Installation creates a derived local copy. The canonical source remains this
repository. A successful install proves installed bytes only; Codex discovery
in a later turn is a separate observable boundary.

## Validate or install from a source checkout

```bash
git clone https://github.com/IndelibleVivi/repository-operational-truth-audit.git
cd repository-operational-truth-audit

python3 scripts/validate_architecture.py
python3 scripts/render_architecture_svg.py --check
python3 scripts/validate_repository.py
python3 -m unittest discover -s tests -p 'test_*.py'
python3 scripts/selftest.py
python3 scripts/install_skill.py
```

The local installer refuses to overwrite a conflicting target. Use
`--replace` only for an intentional upgrade; the replaced copy is preserved in
a recoverable backup and the installer writes a provenance receipt.

## Invoke it

```text
Use $repository-operational-truth-audit to reconstruct this repository's
current operational truth before I resume work. Focus on which entrypoints and
artifacts are live, what the current tests actually prove, and which unknowns
can change the re-entry decision. Keep it read-only.
```

A complete run binds:

```text
one owner decision + one exact repository snapshot
  -> current authority and live selectors
  -> source / configuration / durable state
  -> generated / built / packaged / projected artifacts
  -> installed or deployed identity, only when freshly observed
  -> challenge, adjudication, and explicit external unknowns
  -> decision fixed point
  -> bounded answer + verification receipt + end re-pin
```

Tests, receipts, status documents, and successful commands are evidence
surfaces. They prove only the exact input, identity, assertion, and proof layer
they actually observed.

## Output semantics

A material finding closes this trace:

```text
claim or live surface
  -> mechanism or state
  -> contradiction or evidence gap
  -> concrete decision impact
  -> fresh validation
```

The adjudication vocabulary distinguishes:

- validated contradiction;
- false-green evidence;
- shadow path;
- intentional multiplicity;
- non-material residue;
- decision-critical unknown;
- external/environment/policy boundary; and
- clean within the explicit audit object.

These are decision meanings, not a score or a required report template. A clean
result does not claim that the repository has no defects; it means no material
contradiction or decision-critical unknown remained inside the pinned object.

## Repository map

| Path | Authority |
| --- | --- |
| `skills/repository-operational-truth-audit/` | Canonical Skill source and UI metadata |
| `docs/product-spec.md` | Complete accepted product and acceptance contract |
| `docs/evidence-model.md` | Proof, finding, unknown, clean-result, and stopping semantics |
| `docs/architecture/` | Renderer-neutral architecture model and separate English/Chinese SVGs |
| `docs/research-basis.md` | Public-safe research provenance and source decisions |
| `docs/current-state.md` | Volatile source, Git, install, CI, and publication truth |
| `evals/cases/` | Controlled behavior cases with evaluator-only expected artifacts |
| `scripts/` | Validation, deterministic SVG rendering, fixture self-test, and transactional install |
| `tests/` | Repository, architecture, fixture, and installer regressions |

Chinese editions use the `.zh-CN.md` suffix and preserve the same document
boundaries rather than combining two languages in one file.

## Validation boundaries

Ordinary validation performs no target-model invocation and no network,
browser, account, deployment, or live-system mutation. The CI workflow runs on
macOS and Ubuntu with Python 3.10 and 3.13.

Skill Field Lab may evaluate the controlled cases in disposable workspaces, but
it is optional evaluation infrastructure—not a runtime dependency and not an
owner of this Skill.

## Licensing

This repository is **source-available, not OSI open source**.

- Functional materials—including the Skill, scripts, tests, CI, evals, and
  functional repository contracts—are licensed under the
  [Sustainable Use License 1.0](LICENSE). It permits personal,
  noncommercial, and internal business use; distribution or provision to
  others must remain free of charge and noncommercial under the full terms.
- The standalone README files, changelogs, public documentation, and independent
  diagrams under `docs/` are licensed under
  [CC BY-NC-SA 4.0](LICENSE-DOCUMENTATION.md).
- The exact path map and exceptions are authoritative in
  [`LICENSING.md`](LICENSING.md). Third-party material, if later incorporated,
  remains under its own terms.

Public visibility does not erase those conditions. No external Skill text or
source code is vendored here; conceptual research provenance is documented in
[`docs/research-basis.md`](docs/research-basis.md).
