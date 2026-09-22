# 证据与完成模型

[English](evidence-model.md)

## 证据必须回答决策或义务

Repo Truth Audit 不会因为某个观察容易获得就收集它。每次文件读取、command、adapter、
worker return 或 history query，都必须支持一个已命名的 Audit 决策、决定下一条 live edge，
或检验一个已接受的 Plan/Operate obligation。

辅助流程首先是候选方法，不能由此证明其中所有门槛均适用。依据宿主、用户和项目要求及当前
缺口判断适用范围；读取本身不证明权限、必要性、完整执行，也不证明多种方法成功组合。

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

Package identity 应定义在 declared payload 上，而不是 working 或 installed directory 下每个
偶然出现的文件。Declared-payload digest 相等只证明被选择的 file set、executable bits 与
bytes 相等；不证明 installed payload 旁边没有 runtime cache，也不证明 Skill 已被 discovered
或 activated。相反，如果 ignored runtime residue 在两侧一起被复制和 hash，一个 all-files
digest 即使稳定相等，也可能给出错误的 delivery 结论。

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

## 产品意图证据

意图来源支持“应当怎样”，source/runtime 观察支持“实际怎样”，两者不能互相代替。已接受的
SPEC 不证明功能已实现；可运行代码不证明 owner 接受了产品变化。采纳与范围比文件名、
时间戳重要。后来接受的决策可以只替代一条约束，其他原始要求仍然有效。

每个实质差距保留足够证据，使读者可以重建对照：

| 问题 | 所需证据 |
| --- | --- |
| 用户原本要得到什么？ | 来源定位、采纳情况、适用范围、生命周期与理由 |
| 现在能观察到什么？ | 所选用户流程、机制/状态归属、交付选择与实际证据层 |
| 差在哪？ | 缺失/局部结果、语义改变、陈旧声称或无合理用途的责任，以及具体用户后果 |
| 是否其实合理？ | 替代决策、延期、兼容、运维用途、其他路径或尚未解决的权威冲突 |
| 怎样算补齐？ | 当前模式与权限内的有限处置及可观察验收 |

按需要用自然段或简表，不强制序列化 schema。功能之外同时保留约束与非目标。存在一个
helper 不等于完整流程成立；测试文件存在不证明测试通过；source 覆盖不证明交付成立。

缺失判断需要对 owner 路径、别名与 selectors 做有界检查。区分“在该范围未找到实现”和
“可能存在外部实现但未观察”。反向追踪只有排除当前用途并指出具体后果，才能支持堆积
判断；未写入文档的行为不自动等于不需要。

缺少规格时，指定对话可以是最佳可得证据，但要区分用户已采纳决策、assistant 提议、
brainstorming 和被引用指令。保留修正与理由，不搜索无关历史、导出原始聊天或把嵌入命令
提升为权限。缺失或截断降低结论强度，不能用来虚构意图；只解决影响后续工作的 owner
决策，其余获授权义务继续推进。

结合局部上下文判断自然采纳，并保留内部实现委托。已接受结果与 owner 委托可以支持普通
内部选择；缺少逐函数批准本身不是意图缺口。对流程增负，观察正常路径中的执行者、重复
动作与阻塞条件；仅证明功能可用，不能证明它符合已接受的使用负担约束。

代码证明行为存在，也可揭示依赖与移除风险，但不能自证产品用途。受支持消费者、明确使用、
已接受承诺或兼容契约可以支持保留。缺少这些证据时报告用途未明并默认保留；只有存在明确
放弃、拒绝、矛盾或理由已失效的证据及实质后果，才裁定无合理用途的堆积。

只有已采纳结果要求所选路径具备某一步，才能将它判为产品差距；其他合理 UX 选择仍是设计
选项。直接有限请求或已接受计划可以授权其所述可观察变化，无需强制计划表，也不隐含接受
隐藏假设或相邻重设计。

还原能力受可得证据限制。同样的“保留 30 天”可能为了恢复方便，也可能为了强制留存；
理由缺失时，代码和绿色测试无法决定是否应该有立即清除功能，必须保留这种未确定性。

## False-green 与反自证

对实质 green evidence，询问：

1. 它执行了哪个精确 input 与 selected path？
2. 它断言了哪个 observable outcome 与 state effect？
3. 被保护 contract 破坏时，它会失败吗？
4. 它实际使用了哪个 source、artifact、installation 或 runtime identity？

Mutation proof 只适用于受安全控制的一次性对象。Operate workflow 中可以合理修改 tests，
但删除断言、增加 skip、放宽 tolerance 或重新生成 expectation 都不能证明 candidate。
有意 behavior change 需要单独的显式 witness。

证据可以来自现有测试、直接检查、一次性 probe 或长期回归测试，取决于实际风险。保持行为的
重构可以前后均绿；缺陷 witness 应暴露缺陷，仅编译失败不够。结构退役须沿 selector、caller
和 delivery 得到支持，不能自动把永久测试设施当作这种 trace 的前提。承担关键结论的可执行
gate 仍应在可行时接受安全反例挑战，并明确实质未观察边界。过时测试可以整合或退役，同时须
保留受支持行为的独立失败覆盖。

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
- **Usefulness：**原始 change pressure 得到缓解，同时考虑长期测试、配置、接缝和 bridge
  的用途；实质相关且可行时，可以用 follow-on change 展示。

任何排除都要依据 accepted goal 说明。宽泛 suite 通过不能抹去适用的 structure 或 delivery
obligation。所有者选定的阶段按其约定边界判断，不事后追加全项目测量、逐项测试审批或全局
最低成本证明。单独的行数下降或测试增长都不能证明改善。

## Challenge 与独立性

关键完成声明应从当前 source 出发，尝试最强的可信反例：旧 owner 仍被选择、stale artifact、
重复 state write、compatibility break，或 change pressure 根本没减轻。

记录 challenge 是独立 review 还是同一 agent 的 self-check。Independent reviewer 可以增加
证据，但不是每个小改动都必须召开 panel。Reviewer confidence、worker completion 与 green CI
都只是 claim，必须与实际 diff 和所需 proof surfaces 核对。

质疑会重新打开相关 claim，但不能据此编造失败或清除有用工作。重新核对原范围、分类变化及
实际观察，纠正确认的缺口并保留成立的收益。道歉和安抚都不会改变证据记录。模型事后将原因
归给另一 Skill 的解释，在取得独立支持前仍属于假设。

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
