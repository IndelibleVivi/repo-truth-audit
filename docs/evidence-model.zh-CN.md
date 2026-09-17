# 证据与完成模型

[English](evidence-model.md)

## 证据必须回答决策或义务

Repo Truth Audit 不会因为某个观察容易获得就收集它。每次文件读取、command、adapter、
worker return 或 history query，都必须支持一个已命名的 Audit 决策、决定下一条 live edge，
或检验一个已接受的 Plan/Operate obligation。

## Proof layer

严格区分：

1. claim、instruction 或 accepted-outcome surface；
2. source/configuration contract；
3. process-level behavior 与 state effect；
4. generated 或 distributed artifact identity；
5. installed/deployed identity；
6. 精确 runtime、edge、device 或 account state；
7. owner-observed acceptance。

一层证据不会证明下一层。Source 可以正确而 package 过期；installed copy 可以正确但未
activated；deployment 可以成功但没有 owner acceptance。

## Audit finding trace

可报告 finding 必须连接：

- **claim/live surface：**使问题与决策相关的 statement、selector、entrypoint 或 gate；
- **mechanism/state：**造成当前行为的 caller、owner、mutation、artifact、persistence 或
  configuration；
- **contradiction/gap：**精确的不一致或缺失证据；
- **impact：**它如何改变当前 decision 或 operation；
- **validation：**排除纯假设担忧的新鲜 source、command、fixture 或获授权观察。

无法闭合这条 trace 的候选应省略。

## 裁定词汇

只在有助于解释决策时使用：

- **Validated contradiction：**当前 live surfaces 提出不相容 claim 或产生不相容行为。
- **False-green evidence：**所声称保护的 contract 已破坏，但 gate 仍保持 green。
- **Shadow path：**可达路径能够影响当前 state/artifact，却没有有意 ownership/selection
  boundary。
- **Intentional multiplicity：**多个 mode 明确、隔离、versioned/owned 且被正确选择。
- **Non-material residue：**旧 surface 无法影响 runtime、distribution、state 或当前决策。
- **Decision-critical unknown：**缺失观察会改变决策或一个必要 operation obligation。
- **External/environment/policy boundary：**缺失观察由仓库之外的 owner 或不可用环境管理。

这些标签不是 score，也不是强制 report schema。

## False-green 与反自证

对实质 green evidence，询问：

1. 它执行了哪个精确 input 与 selected path？
2. 它断言了哪个 observable outcome 与 state effect？
3. 被保护 contract 破坏时，它会失败吗？
4. 它实际使用了哪个 source、artifact、installation 或 runtime identity？

Mutation proof 只适用于受安全控制的一次性对象。Operate workflow 中可以合理修改 tests，
但删除断言、增加 skip、放宽 tolerance 或重新生成 expectation 都不能证明 candidate。
有意 behavior change 需要单独的显式 witness。

Cited-byte match 只证明命名 bytes；JSON schema 通过只证明 shape。两者都不证明 semantics、
authority、completion 或 safe execution。

## Checkpoint 与完整目标完成

Checkpoint 是一个在自身 claim layer 获得当前证据的 coherent increment，可以保留并续做。
当原始 accepted outcome 仍有未解决的 caller、state owner、selector、artifact、compatibility、
retirement 或 delivery obligation 时，它不是完成。

完成要求每个适用义务都有当前证据：

- **Behavior：**约定的 output、failure、compatibility 与 state effect。
- **Structure：**目标 ownership/dependency change 或 retirement，而不只是新 facade 或文件。
- **Delivery：**每个请求覆盖的 manifest、package、installed、activation 或 runtime surface
  都选择预期实现。
- **Usefulness：**在实质相关且可行时，用 follow-on change 证明原始 change pressure 降低。

任何排除都要依据 accepted goal 说明。宽泛 suite 通过不能抹去适用的 structure 或 delivery
obligation。

## Challenge 与独立性

关键完成声明应从当前 source 出发，尝试最强的可信反例：旧 owner 仍被选择、stale artifact、
重复 state write、compatibility break，或 change pressure 根本没减轻。

记录 challenge 是独立 review 还是同一 agent 的 self-check。Independent reviewer 可以增加
证据，但不是每个小改动都必须召开 panel。Reviewer confidence、worker completion 与 green CI
都只是 claim，必须与实际 diff 和所需 proof surfaces 核对。

## Recovery evidence

Operation record 保存 provenance 与 resumption context，不证明 freshness 或 permission。续做时，
先把 in-flight effect 分类为 absent、complete、partial、concurrently changed 或 unobservable，
再决定是否重试。

Code recovery 只处理当前 postimage 仍匹配的 task-owned change。Durable-state recovery 需要
schema/version compatibility、backup/compensation、intervening-write、idempotency 与
safe-rollback evidence。acknowledgement 丢失绝不证明 external 或 data effect 没有发生。

## Unknown

把 unknown 写成：

~~~text
缺失观察 -> 被阻止的 claim 或 obligation -> 它能改变的 decision 或 outcome
-> 所需精确新鲜观察
~~~

按受影响决策合并 unknown。若缺失观察无法改变决策或 accepted operation result，则省略，
或只将其标记一次为 out of scope。

## Clean Audit 与 operation terminal state

Clean Audit result 说明 decision 与 snapshot、已跟随的 live selector 与 truth owner、达到的
proof layer、未观察的 external boundary，以及为什么剩余 traversal 无法改变决策。它不声称
仓库没有 defect。

Operate result 只能是：

- **Complete：**整个 agreed outcome 拥有当前证据。
- **Checkpoint：**coherent increment 已验证，剩余义务明确。
- **Blocked：**精确缺失的观察、能力、权限或依赖阻止下一必要步骤。
- **Aborted/recovered：**last known good state、保留 edits、实际撤销的 effects 与未解决 effects
  均明确。

## 停止

Audit 在 decision fixed point 停止。Plan 在 finite outcome、sequence、witness、authority
boundary、recovery 与 unresolved decision 均已 decision-ready 时停止。Operate 只在 Complete，
或诚实报告的 Checkpoint、Blocked、Aborted/recovered 状态停止。每个 mode 都要核对 start/end
identity。
