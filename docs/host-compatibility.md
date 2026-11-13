# Host compatibility and observable adoption

[简体中文](host-compatibility.zh-CN.md)

Checked: 2026-11-13. This page separates package portability, installed bytes,
host selection and observed task behavior. See [current state](current-state.md)
for release status and [usage](usage.md#installation-and-discovery) for discovery
troubleshooting. The public `v0.3.0` tag and unreleased source remain separate
installation choices.

## What has been established

| Layer | Evidence in this round | Limit |
| --- | --- | --- |
| Standard text package | YAML frontmatter, `SKILL.md`, relative references and scripts follow the [Agent Skills format](https://agentskills.io/specification). | Format compatibility does not establish any host's activation or execution. |
| Exact payload | Source validation, digesting, staging and installed comparison share the nine-file definition in [`scripts/common.py`](../scripts/common.py). | A matching directory proves its bytes; a different host may select another directory. |
| Local installer | A fresh temporary install matched the candidate's nine-file digest and recorded dirty source. Repository tests also exercise replacement and payload identity through [`scripts/install_skill.py`](../scripts/install_skill.py). | Its default is `$CODEX_HOME/skills` or `~/.codex/skills`; `--dest` does not register a directory with a host. |
| Native research agents | Fresh agents in the research session were explicitly instructed to read the pinned candidate snapshot. No-Skill arms received the same product task without it. | This tests explicit loading. The backend model identifier, token counters and automatic discovery were not observable. |
| Local Codex CLI | `codex-cli 0.167.0-alpha.4` was present. A minimal probe failed while initializing its in-process app-server client with `Read-only file system (os error 30)`. | No target-model execution or Skill selection was established by this probe. It is an environment initialization failure, not an observed model failure. |
| Other native hosts | Official Claude Code, Gemini CLI and OpenCode discovery/activation documentation was inspected. | No native task run on these hosts was performed in this round. |
| Optional Field Lab | Explicit v1-to-v2 migration, v2 validation and all six deterministic self-tests passed on the pinned source below, with zero target invocations. | This validates migration and fixture oracles. It does not establish live adapter behavior or Skill selection. |

The natural-trial candidate has payload digest
`28b73009402e0f149c7078379a15d51cf88468c66ec092f49a59a5f6926fb211`.
This identifies that tested snapshot. Later source changes require a fresh digest;
the version string alone cannot identify unreleased behavior.

The payload contains `LICENSE.txt`, `NOTICE.md`, `SKILL.md`, `agents/openai.yaml`,
`references/audit.md`, `references/intent.md`, `references/operation.md`,
`references/recovery.md` and `scripts/check_evidence.py`. Evaluation fixtures,
expected answers, model runners and trial comparison tools are excluded.
The OpenAI interface file is host metadata; the method lives in the Markdown
package and does not require a provider service or a host-specific coordinator.

## Documented host entry points

These are local verification starting points, checked against official documents
on the date above. Installed host versions and configured overrides still need
inspection.

| Host | Documented location or entry | Fresh-task verification |
| --- | --- | --- |
| [Codex](https://learn.chatgpt.com/docs/build-skills) | Current documentation lists repository `.agents/skills/` and user `~/.agents/skills/` discovery locations. | Use `/skills` or explicitly invoke `$repository-operational-truth-audit`; inspect the selected file and restart if changes are absent. |
| [Claude Code](https://code.claude.com/docs/en/skills) | Project `.claude/skills/<name>/SKILL.md` or personal `~/.claude/skills/<name>/SKILL.md`. | Invoke `/repository-operational-truth-audit`; check the actual selected directory and reference reads. |
| [Gemini CLI](https://geminicli.com/docs/cli/skills/) | Workspace `.gemini/skills/` or `.agents/skills/`; corresponding user locations also exist. | Inspect `/skills list`; use `/skills reload` when needed, then request the named Skill and observe activation. |
| [OpenCode](https://opencode.ai/docs/skills/) | Project `.opencode/skills/`; documented compatibility roots include `.claude/skills/` and `.agents/skills/`. | Mention `@repository-operational-truth-audit`; inspect the selected base directory. Supporting files require their own reads. |

The documented Codex locations differ from this repository installer's retained
default. For the documented current host, choose an explicit destination such as
`--dest /path/to/disposable-product/.agents/skills` and verify discovery. This
round did not establish whether a particular Codex build also reads the older
root. The [older OpenAI catalog](https://github.com/openai/skills) now marks itself
deprecated and links to the current guide; its historical installation recipe
must not substitute for a current host observation.

Duplicate names can change the selected package. Retain evidence of the selected
path before investigating precedence; do not delete competing copies on a guess.
An explicit invocation, a tool trace mentioning a path and semantic application
are different observations. Record what the host actually exposes.

## A small reproducible local smoke test

Run packaging checks from the chosen RTA source checkout. This creates only a
temporary package and leaves the user's daily installation unchanged:

```bash
git rev-parse HEAD
git status --short --branch
python3 scripts/validate_repository.py
rta_preview_root=$(mktemp -d)
python3 scripts/install_skill.py --dest "$rta_preview_root"
python3 - "$rta_preview_root/repository-operational-truth-audit" <<'PY'
import sys
from pathlib import Path
sys.path.insert(0, "scripts")
from common import SKILL_DIR, SKILL_PAYLOAD_FILES, directory_digest, payload_matches
target = Path(sys.argv[1])
assert payload_matches(SKILL_DIR, target)
print("files:", len(SKILL_PAYLOAD_FILES))
print("selected payload:", directory_digest(target, SKILL_PAYLOAD_FILES))
PY
```

For a host test, use a separate disposable product directory. Copy only
`evals/cases/source-artifact-split/fixture/` into it. Place the same declared
payload in a project Skill root that the selected host documents, using
`install_skill.py --dest /path/to/disposable-product/<host-skill-root>`.
Keep `expected/` outside the subject and keep the host's normal trust and execution
controls. Temporary copies are not OS isolation for untrusted code.

Start a fresh task and use the host's explicit invocation above with this request:

> Decide whether this repository is ready to hand to an operator as a packaged
> CLI. Follow the actual distribution selector and determine what the existing
> green test proves. Keep the audit read-only except for `AUDIT.md`. State which
> Skill file you selected and which execution boundaries you could observe.

An independent reviewer then checks the report against the fixture and selected
artifact. A successful audit preserves the product files, reaches the declared
consumer and accurately bounds the green source test. The agent's statement
that it loaded a Skill is retained as self-report unless a host trace supports
that observation. Test implicit activation separately only when discovery itself
is the question. A single explicit smoke test cannot establish Audit/Plan/Operate
coverage, continuation reliability or productivity uplift.

Keep a small receipt: host/OS version, requested and observed model identity if
available, source commit/dirty state, payload digest, selected path, prompt and
subject identity, execution result, protected-file changes, and limitations.
Record unavailable counters as unavailable. This is a finite compatibility check;
it is not a required workflow for every target repository.

## Optional Field Lab v2 route

The observation used Skill Field Lab `0.2.1` at
[`6f79c5717da8bc0639fa0d70f5d82b64c231b9c5`](https://github.com/IndelibleVivi/skill-field-lab/tree/6f79c5717da8bc0639fa0d70f5d82b64c231b9c5).
Its normal commands accept v2 manifests. The explicit offline migrator accepts
RTA's legacy [`fieldlab-pack.json`](../fieldlab-pack.json); the
[migration guide](https://github.com/IndelibleVivi/skill-field-lab/blob/6f79c5717da8bc0639fa0d70f5d82b64c231b9c5/docs/MIGRATION_V1_TO_V2.md)
defines its preconditions and receipt.

From that Field Lab source checkout, choose a new output parent outside the RTA
checkout; the parent must not already exist:

```bash
python3 -m fieldlab migrate-v1 /path/to/repo-truth-audit/fieldlab-pack.json \
  --output /path/to/new-rta-lab/fieldlab.json
python3 -m fieldlab validate /path/to/new-rta-lab/fieldlab.json
python3 -m fieldlab selftest /path/to/new-rta-lab/fieldlab.json
```

The recorded migration preserved one subject and six cases, changed no source
manifest, reported `semantic_change: false`, and invoked no target agent. Its
source-manifest SHA-256 was
`fd578f58abffb88a847beb7f2e1dbdf568832e14415cbf66c4a97f5c8c82b9db`.
The resulting workspace snapshot is a dated experimental input. Later canonical
Skill edits do not update it automatically. Keep the migration receipt and
create a deliberate new snapshot when testing changed source.

Migration, `validate` and `selftest` are the observed route. Live Field Lab runs
have their own plan, adapter, execution and invocation-cap requirements; none
were used here. RTA does not acquire a Field Lab runtime dependency, a second
canonical Skill or an implicit model-calling validation step.
