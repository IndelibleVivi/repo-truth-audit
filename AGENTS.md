# Repository Operational Truth Audit repository contract

## Product and ownership

This repository is the canonical source for the standalone
`repository-operational-truth-audit` Codex Skill. It owns its Skill source,
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
owner decision. It traces decision-bearing entrypoints, selectors, authority,
state, artifacts, installed/deployed evidence, documentation, and gates. It
reports validated contradictions, intentional multiplicity, non-material
residue, or decision-critical unknowns and then stops.

It is not a generic quality score, compliance scan, public-launch checklist,
code review, one-claim verifier, automatic repair workflow, live-system audit,
or issue backlog generator.

Audit mode is read-only by default. A request to audit does not authorize fixes,
commits, pushes, installs, deploys, account actions, remote writes, browser
actions, or publication. If the user separately asks to repair a finding, treat
that as a new implementation boundary and follow the target repository's
authority.

## Truth surfaces

| Surface | Authority |
| --- | --- |
| `skills/repository-operational-truth-audit/SKILL.md` | Runtime behavior and invocation boundary |
| `docs/product-spec.md` | Complete accepted product contract and acceptance requirements |
| `docs/evidence-model.md` | Finding, clean-result, proof-layer, and stopping semantics |
| `docs/architecture/audit-runtime-model.json` | Renderer-neutral architecture semantics, stable IDs, locale copy, boundaries, and source mapping |
| `scripts/render_architecture_svg.py` | Canonical fixed geometry and condensed display composition for both localized SVGs |
| `docs/architecture/audit-runtime.*.svg` | Tracked generated English/Chinese diagrams; never edit as source |
| `docs/research-basis.md` | Public-safe research provenance and external-source decisions |
| `docs/current-state.md` | Volatile source, Git, validation, installation, and publication state |
| `evals/cases/` | Controlled behavior subjects; expected artifacts are evaluator evidence, not runtime instructions |
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
  reduced audit object, placeholder workflow, or abbreviated product is not.
- Keep one canonical Skill implementation. Do not generate or maintain a
  parallel router-owned copy.
- Keep activation discriminating. Ordinary PR review, debugging, license audit,
  security scanning, and one known verification claim must not route here.
- The audit must follow decision-bearing topology rather than raw file count.
- A finding must close the path from claim/live surface through mechanism or
  state to contradiction/gap and decision impact.
- Missing runtime observation is not automatically a repository defect.
- Intentional multiple modes remain clean when selection, ownership, state, and
  version boundaries are explicit and isolated.
- Do not add default repair, multi-agent fan-out, scores, maturity grades,
  generic hygiene lists, or durable target-repository audit backlogs.
- Expected eval artifacts must not leak into the Skill prompt or fixture.
- Architecture diagrams must answer the accepted audit-runtime reader question;
  do not replace them with a banner, abstract concept, or Skill packaging view.
- Change architecture meaning in `audit-runtime-model.json`, change composition
  in the renderer, regenerate both SVGs, and preserve semantic/localization
  parity. Never hot-edit one generated locale artifact.

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
python3 scripts/render_architecture_svg.py --check
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
the Skill.

The canonical public remote is
`https://github.com/IndelibleVivi/repository-operational-truth-audit`.
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
