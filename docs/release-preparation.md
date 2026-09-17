# Preparing v0.2.0

[简体中文](release-preparation.zh-CN.md) · [Draft notes](releases/v0.2.0.md)

Status: **PREPARATION ONLY**

This is a maintainer runbook, not installation authority or an automatic release
script. It prepares the source candidate already described in the
[product spec](product-spec.md). The published release remains v0.1.0 until a
new release is actually created and verified. Follow [AGENTS.md](../AGENTS.md).

## 1. Freeze and validate the candidate

Use the actual candidate checkout, preserve concurrent work and record HEAD,
branch, index/working-tree status and the declared Skill payload digest. Do not
turn an arbitrary dirty checkout into a release candidate by resetting it.

```bash
pwd -P
git rev-parse --show-toplevel
git rev-parse HEAD
git status --short --branch
python3 scripts/validate_repository.py
python3 scripts/validate_architecture.py
python3 -m unittest discover -s tests -p 'test_*.py'
python3 scripts/selftest.py
python3 evals/operation-lab/run_operation_lab.py
git diff --check
```

Run the host's system Skill validator when available, using its actual resolved
path. Missing host tooling is a recorded observation boundary, not a fabricated
PASS. Read back CI on the candidate commit; earlier CI is not evidence for new
bytes. Keep raw local paths and private logs out of public documentation.

Use `SKILL_PAYLOAD_FILES` for identity and copying. A successful normal import
must not change the declared digest or add bytecode to a staged installation.
The source candidate's eight-file digest is recorded in the
[forward receipt](forward-0.2.0-receipt.md); reconcile changes to runtime files
before reusing those model observations. Do not overwrite historical digests.
Documentation-only changes outside the payload need documentation validation,
not a claim of newly tested model behavior.

## 2. Check installation, then actual host use

From the validated checkout, first exercise the real installer in a disposable
Skill root. Disable Python bytecode writes so this command writes only to the
chosen disposable installation destination:

```bash
preview_root=$(mktemp -d)
PYTHONDONTWRITEBYTECODE=1 python3 scripts/install_skill.py --dest "$preview_root"
```

Check the exact installed file set, source/installed digest equality and receipt.
Exercise replacement in disposable space too: retain the earlier copy as backup
and verify unrelated destination content survives. A temporary directory is not
an execution sandbox and need not be discovered by the host.

Only after the owner authorizes changing the daily installation, use the actual
host Skill root and `scripts/install_skill.py --replace` for an existing copy.
Inspect the backup and receipt; do not merge directories manually. Reload/restart
the host as needed, then start fresh tasks in disposable synthetic targets:

- **Audit:** check the selected artifact; no target edits beyond an explicitly
  requested report.
- **Plan:** produce a real structural plan; compare start/end target bytes and
  owner work. A request-classification answer is insufficient.
- **Operate:** give the complete finite goal once. Check actual callers, state
  effects, declared artifact and required retirement; do not prompt it through
  each step or accept its completion claim without external checks.

Confirm the loaded Skill path/identity as well as behavior. Keep evaluator-only
answers out of the target's context. Record observed limitations and the owner's
acceptance separately. Do not run a production-data migration as a smoke test.

## 3. Prepare the release commit without premature publication claims

After those gates pass and the owner selects publication, prepare the release
metadata in a reviewed commit. Do not publish directly from a dirty worktree.

Update the release install reference and `PUBLIC_RELEASE_VERSION` together,
along with the paired READMEs, product/version status text, current-state,
changelogs and release notes that actually change. The existing repository test
hard-codes the old stable install reference: deliberately migrate it to the new
release contract and retain checks that a mismatched reference fails. Do not
remove assertions merely to get green CI. Preserve historical v0.1.0 files and
tags; do not globally replace every occurrence of the old version.

Before the tag/Release exists, label the new ref as the **release target** and
state that the install command becomes usable only after publication. Keep
current publication facts separate from that target. Draft notes may be ready
without claiming "published". Keep the `DRAFT — NOT PUBLISHED` marker and its
unconditional repository assertion intact even after `PUBLIC_RELEASE_VERSION`
becomes `0.2.0`; changing that constant does not prove publication. The
package's `VERSION` already identifies the 0.2.0 source candidate and likewise
does not prove a public release exists.

Review GitHub About metadata too. Suggested description:

> Evidence-led repository diagnosis and verified structural change for Codex.

Changing repository metadata is an authorized external write, not a side effect
of editing this guide. Keep the invocation slug and licensing unchanged.
Rerun relevant checks and obtain CI for the exact release candidate.

## 4. Publish only with real authorization

Use the owner's accepted Git/release workflow to publish the selected commit,
create a new annotated v0.2.0 tag and create its GitHub Release. The tag must peel
to that commit; the Release must refer to that tag. Do not move v0.1.0 or repair
an already published tag by silently retargeting it.

No command on this page creates a tag, changes a remote ref or publishes a
Release. Reading the runbook is never the authorization to do so.

After publication, read back the public repository/default branch, tag target,
Release state and CI, then install from the public tag into a disposable root
and compare the declared payload with the tested candidate. Verify the README,
license and package paths are publicly readable. An API success response alone
does not close all these checks.

Only after that publication/read-back gate succeeds may a status-only commit
replace the release-note draft marker with an observed published status and
migrate the corresponding repository assertion. Do not make that test change
part of the pre-publication release candidate.

Update status documents with the observations that actually happened. A later
status-only commit can move main without changing the published tag. Preserve
pending or failed gates as such. Do not label public installation as host runtime
activation or synthetic checks as general production capability.

## Completion record

Record only useful public-safe facts: selected source/tag commit, payload
identity, validation/CI, disposable tagged installation, observed host discovery,
owner acceptance, publication read-back, and remaining boundaries. Distinguish
local installation, publication and someone else's future discovery. There is
no need to build a second release scheduler or permanent per-target audit log.
