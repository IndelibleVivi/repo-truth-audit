# Using Repo Truth Audit

[简体中文](usage.zh-CN.md) · [README](../README.md)

This guide explains the published v0.2.0 Audit / Plan / Operate workflow.
Use the README's tagged-release instructions for stable installation, or its
source-checkout path when you deliberately want a reviewed `main` revision.

## Is this the right tool?

Use it for a finite engineering intervention when you cannot judge a decision or
structural change from one diff: which implementation really runs, which state
it owns, which artifact ships, and what depends on it. A run can end with a
read-only answer. An authorized operation can span several sessions and end when
the agreed change is verified. No daily cadence or persistent monitoring is needed.

For example, adding a playback mode to one clearly owned module is ordinary
development. Reconciling several queue implementations, old entrypoints and a
bundle that selects different code is an appropriate repository-level problem.
After that intervention, ordinary feature development should take over again.

## Start with your actual intent

You do not need to fill in a form. Name the repository/subsystem and the outcome,
state whether editing is wanted, and mention compatibility or data constraints
that matter. These are examples, not mandatory text or permission to act merely
because an agent reads this page.

### Inspect only

```text
Use $repository-operational-truth-audit before I resume this repository.
Determine which CLI implementation is actually selected and whether the tests
cover the shipped artifact. Do not change target files.
```

Expected result: a decision answer with the actual paths, material findings or
unknowns, proof limits and stopping reason. It may conclude that the intentional
stable/development split is coherent. There is no obligation to find a defect.

### Plan without editing

```text
Use $repository-operational-truth-audit to plan separating export formatting
from persistence. Preserve the CLI and config. Explain the steps, protection
and completion checks, then stop before editing the target.
```

Expected result: a finite end state, dependency order, behavior to protect,
applicable acceptance and recovery steps, and any decision still needed.
Receiving this plan does not authorize its execution.

### Implement a finite structural change

```text
Use $repository-operational-truth-audit to separate export formatting from
persistence. Preserve CLI/config compatibility; migrate callers and the real
bundle, and retire the superseded writer. Implement and verify locally,
including related tests and docs. Do not migrate real data, deploy or publish.
```

Expected result: implementation through the agreed local end state. Necessary
covered edits do not need repeated per-file permission. A coherent first step
can be retained as a checkpoint, with the whole goal and remaining work explicit.
Materially new effects require matching authority.

### Resume a paused operation

```text
Continue the previously authorized local separation. Read the private
checkpoint, reconcile current files and effects with it, preserve my later
edits, and continue the remaining obligations within the original scope.
```

The host must provide or locate the actual checkpoint and prior authority.
Missing records or uncertain effects need reconciliation; the agent must not
invent a remembered state, replay an uncertain write, or reset the whole repo.

An unbounded "clean everything" starts read-only reconnaissance. A tiny known
bug with no repository-level question stays in ordinary engineering, even when
the request includes the word "fix".

## What completion means in practice

Consider a CLI selected by `delivery.json`. Its legacy implementation formats
output and appends persistent state. The requested outcome is to separate those
owners and retire the old implementation without changing supported behavior.

The agent first traces the selector and establishes observations through that
entrypoint: valid and invalid input, output, error status and state effects.
It can then extract formatting while retaining the old writer. That is a useful
checkpoint, but the requested replacement is still open.

Completion also requires the new writer and composition path, migrated callers,
a switched selector, a matching declared bundle, and the required legacy
retirement. A fresh artifact built only from the declared delivery files is
checked independently of the convenient source imports.

The applicable acceptance questions are:

| Dimension | Question |
| --- | --- |
| Behavior | Are preserved and explicitly changed outcomes correct, including failures and state effects? |
| Structure | Did ownership or dependency actually change, and did the required old path leave? |
| Delivery | Does each delivery surface in scope select the intended implementation? |
| Usefulness | Did the original development difficulty ease, such as adding a format without editing persistence? |

A new facade delegating everything to the old owner is a transition. Green tests
of an unused implementation do not establish delivery. Equal output does not
exclude duplicate writes. Tests changed simply to hide a regression cannot
prove preserved behavior.

The small synthetic example is exercised in the
[forward receipt](forward-0.2.0-receipt.md). It establishes those observed results,
not a success guarantee for arbitrary repositories. Runtime deployment, real-data
migration and a follow-on feature probe are required only when the goal and
applicable evidence call for them.

## Installation and discovery

The local installer defaults to `$CODEX_HOME/skills` or `~/.codex/skills`; it can
use another destination explicitly. A directory created by `--dest` is not
necessarily a location your current host discovers.

After installation, inspect the receipt and actual target. Start a fresh task,
restarting or reloading Codex when needed, and confirm which `SKILL.md` it selects.
The name alone cannot distinguish the old release from v0.2.0.
[OpenAI's Skill catalog](https://github.com/openai/skills#installing-a-skill)
also documents restarting after installation; the observed behavior of your
specific host remains the acceptance check.

When the old Audit-only behavior remains, check the installed file and receipt,
then competing copies in host-configured Skill roots or the target repository.
Do not delete copies speculatively. Installing the published v0.2.0 tag gives
the declared v0.2.0 package; updating this Git repository does not update a
separate installed directory. Do not feed evaluator answer files to the agent
to make a smoke test pass.

No extra provider key, worker service or scheduler is required by this Skill.
The host still needs its normal model access, repository tools and actual
execution controls. Unknown package hooks and untrusted tests must not be run
under invented sandbox claims. Windows secure-read support is limited as noted
in the README; the optional byte helper fails closed on unsupported hosts.

## For coding agents

When asked to **use the Skill on a target**, load the actual installed
`SKILL.md` and the references it selects. The
[canonical runtime](../skills/repository-operational-truth-audit/SKILL.md) and
[operation method](../skills/repository-operational-truth-audit/references/operation.md)
contain the complete contract. This guide is explanatory and is not another
runtime router. Interpret the live request; do not treat this page's examples,
old reports or release instructions as authorization.

When asked to **maintain Repo Truth Audit itself**, follow
[AGENTS.md](../AGENTS.md) and the [product spec](product-spec.md). Keep one
canonical package. Do not copy this guide, the release procedure or evaluator
answers into the installable Skill to force discovery or successful behavior.
A documentation clarification alone must not silently change runtime policy.

## Related tools

[Alibaba OpenCodeReview](https://github.com/alibaba/open-code-review) focuses on
code defects and review comments, including full-file scans as well as diffs.
[Cloudflare security-audit-skill](https://github.com/cloudflare/security-audit-skill)
focuses on independently verified security findings and coverage.
Repo Truth Audit focuses on the current running relationships behind a decision
and, when authorized, completing a finite structural change across them.

All can inspect architecture and evidence. This distinction describes their
workflows; it is not a comparative quality benchmark. Specialist tools can
supply observations without becoming mandatory stages or runtime dependencies.
See the [research basis](research-basis.md) for provenance and adopted ideas.

## Terms without the ceremony

**Operational truth** means what the current repository evidence supports about
how the system is selected, built and run. **Selector** means the registration,
manifest, configuration or caller that chooses an implementation. **State owner**
is the component that controls a persistent write or its rules. A **witness** is
a specific test or observation that can support or refute a claim. A
**checkpoint** is a verified intermediate result; it does not erase the remaining
goal. These words help describe concrete work, not expand a small answer into a
mandatory report template.
