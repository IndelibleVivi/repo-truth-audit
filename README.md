# Repository Operational Truth Audit

一个独立的、read-only-first Codex Skill：当一个 repo 已经演化很久，而 owner
需要 re-entry、迁移、归档、合并、handoff 或 release decision 时，重建它**今天实际
由哪些路径、状态、artifacts 与 gates 组成**，并把 repo 能证明的事实与尚未观察的
runtime truth 分开。

当前版本：`0.1.0-rc1`，完整 source candidate；尚未公开发布。

## 它解决什么

普通 code review 从一个 bounded change 开始；普通 verification 从一个已知 claim
开始。Repository Operational Truth Audit 用在这两个起点都不存在或不充分的时候：

- 几个月没碰这个 repo，现在应从哪里继续？
- migration、machine move 或 safe archive 前，哪些路径仍然 live？
- source、generated artifact、package、installed copy、docs 与 tests 是否讲同一件事？
- 一个 green gate 究竟证明了哪一层，会不会在关键 contract 被破坏后仍然 green？
- 两套 mode 是 intentional selection，还是一条没人承认的 shadow path？
- repo 声称可恢复，但 remote schema、secret、dashboard setting 或 manual step 无法观察时，当前 decision 还能下到哪里？

它会返回 validated finding、intentional multiplicity、non-material residue、
decision-critical unknown，或一份短的 clean-within-scope 结论。它不输出 maturity
score，也不会默认制造修复 backlog。

## 什么时候不要用

- review 一个 diff、commit、branch 或 PR；
- verify 一个已经明确的 claim；
- 修复一个已知 bug；
- 做 license、security、compliance 或 dependency 专项审计；
- 只想要 generic repo hygiene checklist；
- 未经授权检查或改变 live host、account、database、browser 或 deployment。

这些任务各自有更窄、更准确的 owner。这个 Skill 不把所有“audit”字样都吸进来。

## 示例请求

```text
Use $repository-operational-truth-audit to reconstruct this repository's current
operational truth before I resume work. Focus on which entrypoints and artifacts
are live, what the current tests actually prove, and which unknowns can change
the re-entry decision. Keep it read-only.
```

```text
在迁移这台 Mac 前，用 $repository-operational-truth-audit 检查这个 repo 的 source、
generated package、installed copy、local state 和 recovery docs 是否仍然对得上。
不要修，先告诉我哪些结论是真的、哪些没有观察到。
```

## Truth path

```text
owner decision + exact snapshot
  -> live entrypoints / selectors / authority
  -> source / config / persistence
  -> generated or distributed artifact
  -> installed / deployed evidence (only when observed)
  -> runtime / owner acceptance (separate boundary)
  -> decision-bounded judgment and clean stop
```

Tests、receipts 和 status docs 是 evidence surfaces；它们只证明自己实际观察的
layer。一个 test 绿，不自动证明 package、installed runtime 或 owner acceptance。

## Local installation

在 repo root 运行：

```bash
python3 scripts/validate_repository.py
python3 -m unittest discover -s tests -p 'test_*.py'
python3 scripts/selftest.py
python3 scripts/install_skill.py
```

若目标目录已经存在且内容不同，installer 会拒绝覆盖；明确升级时使用
`--replace`。安装是 derived deployment，canonical source 始终在本 repo 的
`skills/repository-operational-truth-audit/`。

Codex 通常在下一轮 discovery 时看到新安装的 Skill。Install receipt 与 digest 只
证明 installed bytes，不冒充当前 turn 已激活。

## Repository map

| Path | Role |
| --- | --- |
| `skills/repository-operational-truth-audit/` | Canonical Skill source and UI metadata |
| `docs/product-spec.md` | Complete product and acceptance contract |
| `docs/evidence-model.md` | Proof, finding, unknown, clean-result, and stopping semantics |
| `docs/research-basis.md` | Public-safe research provenance and source decisions |
| `docs/current-state.md` | Current source/Git/install/publication truth |
| `evals/cases/` | Controlled behavior cases with hidden expected artifacts |
| `scripts/` | Repository validation, fixture self-test, and transactional local install |
| `tests/` | Deterministic contract and installer regressions |

## Validation

Ordinary validation performs no target-model invocation and no network or live-system action:

```bash
python3 scripts/validate_repository.py
python3 -m unittest discover -s tests -p 'test_*.py'
python3 scripts/selftest.py
```

Skill Field Lab is an optional evidence companion. Its validation/self-test may exercise the
controlled cases in disposable workspaces, but Repository Operational Truth Audit does not
depend on Field Lab at runtime and never starts a live target-model run implicitly.

## Ownership and publication

This is a standalone project. Softpowers may later recommend it, but does not generate,
bundle, install, or version it.

The repository currently has **no public license and no remote release**. Visibility or local
availability is not permission to redistribute. Publication, a GitHub remote, release tags,
and public license terms remain separate owner decisions.
