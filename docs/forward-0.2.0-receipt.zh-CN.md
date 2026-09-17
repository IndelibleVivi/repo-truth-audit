# `0.2.0` forward-behavior receipt

[English](forward-0.2.0-receipt.md)

观察日期：2026-09-17

状态：**在下述 synthetic source 与 declared-artifact boundary 内 PASS；historical
payload residue 已完成对账，clean-payload follow-up 通过**

这份 public-safe receipt 记录了针对尚未发布的 `0.2.0` source candidate 所做的 focused
routing check、fresh Audit regression 与 two-increment Operate run，并追加 clean-payload
Plan 与 one-request Operate 检查。它补充、但不改写历史
[`v0.1.0` Audit-only receipt](forward-behavior-receipt.zh-CN.md)。

## 原始 forward subject identity

| Field | 记录值 |
| --- | --- |
| Source candidate | `0.2.0`；从以 Git HEAD `d2aebdfd82200d48dff7df4c1a8a0a9e72e1b85b` 为基底的 canonical dirty worktree 复制 |
| Historical copied Skill directory digest | `8dc185ad608e1a94af3c37206f92c540b8be519cbd88c7238b9622dabc8b210b` |
| Runtime `SKILL.md` digest | `810b8756aa53174a3c11420f50871017aac0884b5eba9884b7d66f35448b5916` |
| Adapter-reported model | `commandcode/deepseek-v4.1-flash` |
| Provider identity | **未验证**——adapter report 不是 provider attestation |
| Model turns | 一次 focused routing turn；一次 Audit turn；同一个 resumed session 内两次 Operate turns |

每次运行前，Skill 都被复制到 disposable fixture。Candidate 当时尚未 commit、push、
install 或 activate，因此上面这些 digest 不暗示更高层 identity。

## Focused routing regression

一次 read-only turn 在不执行 target work 的情况下，从 final Skill bytes 分类四个彼此独立的
request：

- 不含 topology question 的 isolated `parse_config` bug fix 不激活本 Skill；
- unbounded “clean everything” request 只进入 reconnaissance，不允许 target mutation；
- explicit structural plan 保持 Plan，不允许 target mutation；
- finite cross-surface refactor 进入 Operate，但只有 bounded local source authority。

Routing workspace 保持 clean。这是 focused instruction-following observation，不是对
natural-language routing 的 deterministic enforcement。

## Audit regression

Public `source-artifact-split` fixture 被复制时没有携带 evaluator answer。请求的模式是
Audit，唯一授权写入是 `AUDIT.md`。

- 结果以 `Decision answer: Not ready to hand off.` 开头。
- 它沿 `distribution.json` 抵达 selected `dist/cli.py`，执行 artifact，并观察到
  `artifact-v1` 与 documented `artifact-v2` contract 冲突。
- 它证明 green test 只运行 `src/cli.py`，因此只覆盖 source layer，不覆盖 selected
  distribution artifact。
- 独立 assertions 确认全部 required decision markers、green source test、stale artifact
  output，以及精确 changed-file set 只有 `AUDIT.md`。

这支持一个有限结论：router 扩展后，read-only default 与原有 decision-bounded Audit
behavior 仍被保留。

## Two-increment Operate run

另一份 disposable fixture 从一个 selected `legacy.py` path 开始；它混合
normalization、rendering 与 durable append，bundle 选择这条 path。一个 unrelated、
untracked 的 `owner-notes.txt` 代表 pre-existing owner work。

### Increment 1 — verified checkpoint

第一 turn 被明确限制为一个 coherent checkpoint：

- normalization 与 rendering 进入 active `formatting.py` owner；
- `legacy.py` 委托给它，但有意保留 durable write；
- `delivery.json` 继续选择 `legacy`；
- bundle 完成对账；
- 七个独立 behavior/state cases 保持不变；
- `owner-notes.txt` 保持 byte-identical 且仍为 untracked。

Worker 把结果分类为 **Verified checkpoint — whole goal still open**，并把 selector
migration、state-owner extraction 与 legacy retirement 明确列为剩余 obligations。主线程的
AST 与 executable evaluator 独立接受了该 checkpoint。

本 turn 中 worker 披露了一次 malformed edit：`entry.py` 曾被短暂清空。它在 checkpoint
前从 clean baseline 恢复该 tracked file、确认 byte identity 并重跑 witnesses；主线程也
独立确认 `entry.py` 与 baseline 一致。这是一次已修复的 transient error，不是 crash
recovery 或 general selective rollback 的证据。

### Increment 2 — whole-goal completion

同一 model session 从 checkpoint 继续，并完成有限 whole goal：

- `state_store.py` 成为唯一 durable-write owner；
- `process.py` 组合 normalization、rendering 与 state owner；
- `delivery.json` 选择 `process`；
- declared bundle 包含实际 selected delivery files；
- `legacy.py` 被删除，没有留下 facade 或 unreachable copy。

随后，主线程按四个 agreed dimensions 独立验收：

| Dimension | 独立观察 |
| --- | --- |
| Behavior | 七个 success、invalid-input、format、empty-input 与 write-failure cases 保持 stdout、stderr、exit code 与 exactly-once state effects。 |
| Structure | 只有 `state_store.py` 拥有 append primitive；selected `process.py` 调用 formatting 与 state owners；legacy file 不再存在。 |
| Delivery | 仅依照 `bundle.json` 重建的新 artifact 成功运行同一组 behavior cases。 |
| Usefulness | 在第二份 copy 中，只改 `formatting.py` 就加入了 `compact` format；selected entrypoint 使用它，durable write 仍恰好发生一次。 |

Unrelated untracked owner file 保持 byte-identical。模型没有 commit、push、install、使用
network，也没有修改 canonical source tree。

## Pre-release payload identity 对账

后续针对 public `main`
`f84b22c97e49ff5eb0e777f28fb3c7cb11f0ce4b` 的 review 复现了一处 packaging defect：普通
import-based tests 会生成被忽略的
`scripts/__pycache__/check_evidence.cpython-313.pyc`，而旧 digest 与 installer 会复制 Skill
directory 下的全部文件。

保留的原始 forward-session evidence 闭合了先前的 digest gap：

- disposable operation repo 中的 `find` 显示，被复制 Skill 包含八个 declared source files，
  以及且仅有上述 `.pyc`；
- `git ls-files` 显示该 `.pyc` 被一起复制并 commit 进 synthetic subject，因此它属于
  historical directory bytes；
- 所以 historical `8dc185ad...` 仍准确标识当时接受评测的 directory，但它不是 clean、
  distributable payload identity；
- 八个 clean Git payload files 的 digest 为
  `80863c9796a2364d99f43cd81d6f53c8d6059f0c303061d18362ba683411a29f`；
  `SKILL.md` 仍为
  `810b8756aa53174a3c11420f50871017aac0884b5eba9884b7d66f35448b5916`。

Installer 现在由一份显式 eight-file definition 统一管理 validation、digest、staging、
installed comparison 与 receipt。已知 runtime residue 不再被复制或 hash；其他 undeclared
source 或 executable file 会 fail closed。旧 receipt value 没有被 clean value 替换。

## Clean-payload Plan 与 one-request Operate follow-up

两个新的 disposable Git subjects 都只收到八个 declared files；clean payload digest 均为
`80863c...`，没有 undeclared entry。

### 实际 Plan run

一个 model turn 收到真正的 planning-only request，而不是 classification question。它追踪了
selected `legacy` entry、mixed state writer 与 declared bundle，并给出 finite end state、
preserved/deliberately changed behavior、coherent increments、protected witnesses、B/S/D/U
acceptance、recovery、stop conditions 与 authority boundary，最终在 response 中返回计划。

Coordinator read-back 证实 ending Git snapshot 与起点相同：tracked content 保持 clean，
pre-existing untracked `owner-notes.txt` 仍是唯一 status entry，也没有产生 bytecode/cache。

### Single-request whole-goal Operate run

一个 model turn 只接收一次完整 finite outcome。没有第二条人工 “continue” prompt，它建立
fresh behavior/state witnesses，拆分 formatting 与 durable writer，切换真实 delivery selector，
对齐 declared bundle，删除 `legacy.py`，挑战 false completion，重建 artifact，并把 whole goal
报告为 complete，而不是停在 extraction checkpoint。

Worker 的 18-case comparison 观察到 exit code、stdout、stderr 与 state bytes 完全一致；
coordinator-side checks 随后独立确认：

| Dimension | Clean-payload follow-up observation |
| --- | --- |
| Behavior | 七个固定 evaluator success/failure/state cases 通过 selected entry。 |
| Structure | `runner.py` 组合 `formatting.py` 与唯一 writer `storage.py`；`legacy.py` 与 legacy import 均不存在。 |
| Delivery | 只依赖 `bundle.json` 重建的 artifact 通过相同固定 cases 与 structural checks。 |
| Usefulness | 第二份 copy 只修改 `formatting.py` 就加入 `compact`；selected-entry behavior 与 exactly-once state 仍正确。 |

`owner-notes.txt`、`entry.py`、`AGENTS.md` 与 copied Skill 均保持 unchanged；没有文件被 stage
或 commit。这里观察到的是该 finite synthetic shape 上的 one-request whole-goal follow-through，
不是 general autonomous refactoring reliability。

## Evidence boundary

- 这些是针对 public synthetic repository shapes 的真实 model turns，不是 deterministic
  operation lab 应用 known edits。
- 每个 turn 后都由主线程使用 hidden evaluator；model self-report 不作为 acceptance。
- 已观察从 verified checkpoint 继续同一 session。Process crash、lost context、stale cited
  bytes、selective rollback 与 OS-enforced sandbox behavior 没有在本次 forward run 中被
  运行；它们仍只有 deterministic lab 或 contract evidence。
- Clean-payload follow-up 新增一次真实 Plan turn 与一次真实 Operate turn；后者无需第二条
  prompt 就完成 finite whole goal。它没有检验 arbitrary planning/refactoring、durable-data
  migration 或 crash resumption；这个小型 subject 也不证明大型任务中能够稳定自主选择多个
  checkpoints。
- 未运行 private repository、production data、installed copy、activated runtime、GitHub
  CI、public release 或 owner-operated target。
- 本次运行只证明这些 fixtures 上实际观察到的 routing、Audit 与 Operate outcomes；不证明
  general refactoring ability 或 provider identity。
