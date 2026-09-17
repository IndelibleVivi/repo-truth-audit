# `0.2.0` forward-behavior receipt

[English](forward-0.2.0-receipt.md)

观察日期：2026-09-17

状态：**在下述 synthetic source 与 declared-artifact boundary 内 PASS**

这份 public-safe receipt 记录了针对尚未发布的 `0.2.0` source candidate 所做的 focused
routing check、fresh Audit regression 与 two-increment Operate run。它补充、但不改写历史
[`v0.1.0` Audit-only receipt](forward-behavior-receipt.zh-CN.md)。

## Subject identity

| Field | 记录值 |
| --- | --- |
| Source candidate | `0.2.0`；从以 Git HEAD `d2aebdfd82200d48dff7df4c1a8a0a9e72e1b85b` 为基底的 canonical dirty worktree 复制 |
| Complete Skill directory digest | `8dc185ad608e1a94af3c37206f92c540b8be519cbd88c7238b9622dabc8b210b` |
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

## Evidence boundary

- 这些是针对 public synthetic repository shapes 的真实 model turns，不是 deterministic
  operation lab 应用 known edits。
- 每个 turn 后都由主线程使用 hidden evaluator；model self-report 不作为 acceptance。
- 已观察从 verified checkpoint 继续同一 session。Process crash、lost context、stale cited
  bytes、selective rollback 与 OS-enforced sandbox behavior 没有在本次 forward run 中被
  运行；它们仍只有 deterministic lab 或 contract evidence。
- 未运行 private repository、production data、installed copy、activated runtime、GitHub
  CI、public release 或 owner-operated target。
- 本次运行只证明这些 fixtures 上实际观察到的 routing、Audit 与 Operate outcomes；不证明
  general refactoring ability 或 provider identity。
