# Evidence model

[English](evidence-model.md)

## Evidence 必须回答一个决策

Repository Operational Truth Audit 不会因为观察容易取得就收集它。每个 command、
file read、adapter 或 history query，都必须支持一个具名 claim，或决定下一条 live edge。

## Proof layers

始终分开这些层：

1. claim 或 instruction surface；
2. source/configuration contract；
3. process-level behavior；
4. generated 或 distributed artifact identity；
5. installed/deployed identity；
6. 精确的 runtime、edge、device 或 account state；
7. owner-observed acceptance。

一层 evidence 不会自动证明下一层。Test 可以正确而 package 已陈旧；package 可以正确而
旧 installed copy 仍然 active；deployment 可以成功而 owner acceptance 尚未发生。

## Finding trace

可报告的 finding 有五个彼此连接的元素：

- **claim/live surface：** 让问题与当前决策相关的 statement、selector、entrypoint 或
  gate；
- **mechanism/state：** 造成当前行为的 caller、owner、mutation、artifact、
  persistence 或 configuration；
- **contradiction/gap：** 精确的不一致或缺失 evidence；
- **impact：** 它如何改变当前 owner decision；
- **validation：** 排除纯假设担忧的新鲜 source、command、fixture 或 observation。

无法闭合这条 trace 的 candidate 不进入报告。

## Adjudication vocabulary

只在能够解释 decision 时使用：

- **Validated contradiction：** 当前 live surfaces 提出不相容 claim，或产生不相容
  behavior。
- **False-green evidence：** 被声称保护的 contract 已破坏，而 gate 仍然 green。
- **Shadow path：** 一条 reachable path 能影响当前 state/artifacts，却没有有意的
  ownership 或 selection boundary。
- **Intentional multiplicity：** 多种 mode 是显式的、隔离的、具备 version/owner，且被
  正确选择。
- **Non-material residue：** 旧 surface 无法影响 runtime、distribution、state 或当前
  decision。
- **Decision-critical unknown：** 缺失 observation 能够改变 decision。
- **External/environment/policy boundary：** 缺失或被拒绝的 behavior 由当前被审计
  repository mechanism 之外的 owner 负责。

这些 labels 不是 score，也不是必填 report schema。

## False green

对每个 material green result 追问：

1. 它运行了哪个 exact input/path？
2. 它 assertion 的 observable outcome 是什么？
3. 被保护的 contract 破坏后，它会失败吗？
4. 它实际使用了哪个 artifact/runtime identity？

Mutation proof 在安全且 bounded 时有价值：在 disposable copy 中故意破坏 protected
invariant，并确认 gate 变红。不要为了证明这一点而 mutation 真实 target。

## Intentional multiplicity 与 shadow path

当所有 material questions 都有明确答案时，multiplicity 通常是 intentional：

- 什么选择每个 mode/version？
- 它们的 state 是否隔离？
- 谁拥有每条 path？
- version 或 artifact identity 如何区分？
- unintended caller 能否到达 old path？
- retirement 或 compatibility status 是否当前且明确？

一个 ambiguous selector 或 shared state 不会自动证明 shadow path；必须追踪真实
reachability 与 impact。

## Unknowns

按照以下形式写 unknown：

```text
Missing observation -> 它阻止的 claim -> 它能改变的 decision -> 所需的 exact
fresh observation
```

不要重复十二次“runtime unverified”。按它们影响的 decision 对 external boundaries
分组。如果缺失 observation 不能改变 decision，就省略它，或只说明一次 out of scope。

## Clean result

一份 clean result 说明：

- 被审计的是哪个 decision 与 snapshot；
- 沿着哪些 live entrypoints/selectors 与 truth owners 穿行；
- 抵达了哪个 proof layer；
- 哪个 external boundary 没有被观察；
- 为什么继续穿行无法改变 decision。

Clean 不等于“repository 没有 defects”。它表示在 explicit audit object 内，没有发现
material contradiction 或 decision-critical unknown。

## Stopping

在以下条件成立时停止：

- 每个 candidate contradiction 已被裁定为 true、false、intentional、non-material，
  或显式 decision-critical unknown；
- 不再出现新的 decision-relevant evidence edge；
- 剩余 surfaces 无法改变 owner decision；
- clean result 或 bounded findings 可以在不发生 qualification drift 的情况下表述；
- start/end snapshot identity 已核对。
