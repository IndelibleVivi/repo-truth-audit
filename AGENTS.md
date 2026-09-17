# Repository Operational Truth Audit repository contract

## Product and ownership

This repository is the canonical source for **Repo Truth Audit**, formally
**Repository Operational Truth Audit**, and the standalone
`repository-operational-truth-audit` Codex Skill. The human-facing display name
and public repository slug may be shorter; the Skill invocation slug and
canonical package path remain unchanged. This repository owns its Skill source,
behavior contract, fixtures, validation, installation helper, documentation,
version, and future release cadence.

Softpowers, Skill Field Lab, or another engineering router may reference this
project as a companion. They do not own, generate, bundle, install, replace, or
version its bytes. Do not add a second same-named Skill copy to another
repository.

The canonical Skill is:

```text
skills/repository-operational-truth-audit/
```

The installed user Skill is a derived deployment. Never edit an installed copy
as source.

## Product boundary

The Skill reconstructs repository-observable operational truth for one concrete
owner decision and, when the user explicitly asks for implementation, can carry
a bounded structural change through current-source diagnosis, planning,
implementation, recovery-aware checkpoints, and verified completion. Audit,
Plan, and Operate are request-derived behavior modes, not CLI subcommands or a
parallel orchestration engine.

It is not a generic quality score, compliance scan, public-launch checklist,
ordinary code review, one-claim verifier, universal automatic fixer,
live-system audit, or issue backlog generator.

Audit mode is read-only by default, and Plan mode does not edit the target. A
request to audit or plan does not authorize fixes, commits, pushes, installs,
deploys, account actions, remote writes, browser actions, or publication. An
explicit Operate request may authorize the local code, test, documentation, and
superseded-source changes required for its finite outcome; public API removal,
durable-data mutation, production activation, paid or privileged actions,
publication, and other materially new effects still require matching authority.

## Truth surfaces

| Surface | Authority |
| --- | --- |
| `skills/repository-operational-truth-audit/SKILL.md` | Runtime behavior and invocation boundary |
| `docs/product-spec.md` | Complete accepted product contract and acceptance requirements |
| `docs/evidence-model.md` | Finding, checkpoint/completion, proof-layer, acceptance, and stopping semantics |
| `docs/architecture/audit-runtime-model.json` | Renderer-neutral Audit/Plan/Operate architecture semantics, stable IDs, locale copy, boundaries, and source mapping |
| `README.md` and `README.zh-CN.md` Mermaid blocks | Active localized architecture views and concise display composition |
| `scripts/validate_architecture.py` | Model/source-anchor validation plus exact Mermaid topology, connector-kind, and locale-parity checks |
| `docs/research-basis.md` | Public-safe research provenance and external-source decisions |
| `docs/forward-behavior-receipt.md` | Public-safe independent forward-test evidence, observed proof layers, and explicit trace limits |
| `docs/current-state.md` | Volatile source, Git, validation, installation, and publication state |
| `evals/cases/` and `evals/operation-lab/` | Controlled behavior subjects and deterministic operation rehearsal; expected artifacts and known patches are evaluator evidence, not runtime instructions |
| `scripts/common.py::SKILL_PAYLOAD_FILES` | Exact installable Skill payload shared by source validation, digesting, staging, installed comparison, and receipts |
| `scripts/` and `tests/` | Deterministic validation and local installation behavior |
| installed Skill directory and install receipt | Installed bytes only; not source authority or proof of next-turn discovery |

Do not let README summaries, expected eval outputs, historical evidence, or an
installed copy silently override the product spec and canonical Skill.

## Before changing source

Resolve the exact repository and preserve existing work:

```bash
pwd -P
git rev-parse --show-toplevel
git status --short --branch
```

Do not reset, clean, overwrite, or stage unrelated changes. Keep private
research packets and raw target-repository evidence outside this Git tree.

## Implementation rules

- Preserve the complete accepted contract. Simpler machinery is welcome; a
  reduced audit object, handoff-only workflow, first-cut-only result, or
  abbreviated product is not.
- Keep one canonical Skill implementation. Do not generate or maintain a
  parallel router-owned copy.
- Keep activation discriminating. Ordinary PR review, debugging, license audit,
  security scanning, and one known verification claim must not route here.
- Audit and operation diagnosis must follow decision-bearing topology rather
  than raw file count.
- A finding must close the path from claim/live surface through mechanism or
  state to contradiction/gap and decision impact.
- Missing runtime observation is not automatically a repository defect.
- Intentional multiple modes remain clean when selection, ownership, state, and
  version boundaries are explicit and isolated.
- Do not turn Audit or Plan into implicit repair. Do not add default multi-agent
  fan-out, scores, maturity grades, generic hygiene lists, durable
  target-repository audit backlogs, or a second provider/orchestration engine.
- In Operate mode, preserve the whole agreed outcome across increments.
  Distinguish a verified checkpoint from completion, and verify the applicable
  behavior, structure, delivery, and usefulness obligations before closing.
- Treat operation records, byte receipts, worktrees, timeouts, and permission
  fields as evidence or workflow aids, never as authorization, OS isolation,
  exactly-once execution, or universal rollback guarantees.
- Expected eval artifacts must not leak into the Skill prompt or fixture.
- Keep one explicit Skill payload definition. Known runtime residue may be
  excluded from payload identity and staging; any other undeclared source or
  executable entry must fail validation, and unexpected installed content must
  not satisfy the unchanged check.
- Architecture diagrams must answer the accepted evidence-led change reader
  question across Audit, Plan, and Operate; do not replace them with a banner,
  abstract concept, or Skill packaging view.
- Change architecture meaning in `audit-runtime-model.json`; change localized
  composition in both README Mermaid blocks in the same edit. Preserve stable
  IDs, exact edge topology, connector kinds, and localization parity. Use
  renderer-default theming rather than fixed colors so GitHub can adapt to day
  and dark surfaces.

## Documentation impact

Update:

- `README.md` when user-facing scope, invocation, installation, or limitations change;
- the paired `.zh-CN.md` edition whenever an English public document's
  substantive contract changes, and vice versa;
- `AGENTS.md` when ownership, source/install boundaries, validation, or publication gates change;
- `docs/product-spec.md` when accepted behavior or acceptance changes;
- `docs/evidence-model.md` when proof or adjudication semantics change;
- `docs/current-state.md` when version, source completeness, installation, Git, or publication status changes;
- `CHANGELOG.md` for user-visible behavior changes.

Keep tracked documentation portable. Do not publish local absolute paths,
private repository names, private raw evidence, credentials, account state, or
host identifiers.

## Validation

Run after meaningful changes:

```bash
python3 scripts/validate_repository.py
python3 scripts/validate_architecture.py
python3 -m unittest discover -s tests -p 'test_*.py'
python3 scripts/selftest.py
python3 "/path/to/skill-creator/scripts/quick_validate.py" \
  skills/repository-operational-truth-audit
git diff --check
```

When Skill Field Lab is already available, also validate and self-test the
subject pack. That companion remains optional and must not become a runtime
dependency or start a target-model invocation during ordinary validation.

## Installation and publication

Local installation is a separate reversible gate. Use
`scripts/install_skill.py`; verify the install receipt and installed digest
afterward. Installed bytes do not prove that a running Codex turn has discovered
the Skill. Validation, hashing, staging, installed comparison, and receipts must
all use `SKILL_PAYLOAD_FILES`; do not restore whole-directory `copytree` or
all-files hashing that can absorb ignored runtime cache into the package.

The canonical public remote is
`https://github.com/IndelibleVivi/repo-truth-audit`.
Functional materials are source-available under SUL-1.0. Standalone public
documentation and independent diagrams are under CC BY-NC-SA 4.0. Follow the
exact path map in `LICENSING.md`; do not describe this project as OSI open
source or silently widen either grant. The Skill package must carry the exact
SUL text and its package-local notice.

Public source, commit, push, CI, annotated tag, GitHub Release, tagged public
install, installed bytes, and later Codex discovery are separate gates. For a
release, verify the public visibility/default branch, peeled tag commit, release
target, CI result, raw license/README paths, and a disposable tagged install.
External research sources were used conceptually; no external Skill text or
code is vendored here.

Before commit, inspect the intended and staged diffs, stage exact paths, and
keep private continuity, raw audit evidence, generated run artifacts, and
secrets out of Git.
