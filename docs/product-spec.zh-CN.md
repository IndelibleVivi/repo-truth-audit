# Repo Truth Audit — 产品规范

[English](product-spec.md)

状态：**0.2.1 已发布 — 有限合成 forward 检查已通过**
扩展范围经所有者确认：2026-09-17
方法选择细化获准实施：2026-09-20
source 版本：0.2.1
最新公开 release：v0.2.1
产品形态：独立 repository + 独立 Codex Skill
Skill 名称：repository-operational-truth-audit

## 1. 产品结果

Repo Truth Audit 为一个明确的所有者决策恢复长期演化仓库的当前 operational
truth。当用户明确要求结构变更时，同一个产品可以从诊断继续到有限计划、获授权的
实现、可恢复 checkpoint 与经过验证的完成状态。

产品保留三个从用户请求推断的 mode：

- **Audit：**只读重建与决策答案；
- **Plan：**给出有限的变更结果与可执行顺序，不编辑目标；
- **Operate：**在明确授权下完成结构变更，并抵达约定的证据边界。

它们是 behavior mode，不是 CLI subcommand。Audit 默认只读。Operate 不重造第二套
coding-agent 平台：它使用宿主已有的 editor、tests、Git policy、workers 与真实
permission controls，同时持续承担约定结果及其证据责任。

## 2. 工作对象与授权

每次运行都绑定一个精确仓库快照，以及一个明确的所有者决策或变更结果。记录物理路径
与 Git root、branch/HEAD、working tree 与 index 状态、相关 untracked inputs、
upstream 关系，以及实质相关的 worktree/submodule identity。

从请求推断 Audit、Plan 或 Operate。“只看不改”保持 Audit；“给我方案”保持 Plan；
明确要求 implement、refactor、extract、consolidate、replace 或 retire 时可以进入
Operate。含糊的 cleanup 语言只允许有限 reconnaissance，直到影响写权限或目标结果的
歧义被解决。

一次 Operate 请求可以覆盖完成约定本地结果所需的普通可逆 source、test、documentation、
integration 与 superseded-source retirement。公共 API 删除、durable data 迁移或
删除、production activation、privileged host 变更、付费调用、installation、账号动作、
publication 及其他实质新增效果仍需匹配的授权。Skill、plan、report、worker、receipt
或 state file 都不能创造权限。

## 3. 共享 operational-truth 方法

Audit、Plan 与 Operate 都从同一条 decision-bearing topology 开始：

~~~text
claim / authority surface
  -> 实际 entrypoint 或 selector
  -> source、configuration 或 durable-state owner
  -> generated、built、packaged 或 projected artifact
  -> installed 或 deployed identity（仅在新鲜可观察时）
  -> runtime、edge、device、account 或 owner acceptance（仅在获授权并已观察时）
  -> evidence gate 与精确 proof boundary
~~~

Traversal 只跟随能够改变决策或 operation 的边。仓库大小、scanner 可用性、文件年龄与
generic hygiene 分类不定义范围。

### ROT-01 — 精确 pin

在深入工作前 pin 住所选对象，保留并发工作，并在每个完成声明前重新 pin。

### ROT-02 — 权威解析

识别当前 source、instruction、state、artifact 与 operator owner。README、AGENTS、
runbook、status file、历史 note、generated projection 与 installed copy 不可互换。

### ROT-03 — 现役路径解析

通过真实 selector、registration、manifest、caller/import、build pipeline、持久化
reader/writer、install receipt 与 operator route 建立可达性。一次搜索未命中不能证明
retirement。

### ROT-04 — 实质 finding trace

每个 finding 都闭合 claim/live surface -> mechanism/state -> contradiction 或
evidence gap -> decision impact -> fresh validation。无法闭合的候选应省略。

### ROT-05 — False-green 挑战

对实质 green evidence，识别精确 input/path、assertion、proof layer，以及破坏所声称
invariant 是否会使 gate 失败。Mutation proof 只能在安全的一次性对象中、依赖真实宿主
控制进行。

### ROT-06 — 层级分离

保持 source、artifact、installation、activation/runtime 与 owner acceptance 分离。
一层证据不会静默证明下一层。

### ROT-07 — 多重模式与退役

多个版本或 mode 在 selector、state、ownership、identity、caller 与 compatibility/
retirement status 明确时可以同时正确。不可达 residue 不会自动成为实质问题；仍可达但
无人拥有的路径需要继续追踪。

### ROT-08 — 外部 unknown

把 unknown 写成：缺失观察 -> 被阻止的 claim -> 受影响的 decision/operation -> 所需的
精确新鲜观察。未观察的外部状态不会自动成为 repository defect。

### ROT-09 — 有界 specialist

Security、licensing、dependency、history、worker 或 live-system tools 可以提供有界
观察或实现工作。本产品负责把它们纳入整体结果，既不继承外部 verdict，也不获得更大权限。
选择辅助流程前，判断它解决的当前缺口，以及前置条件、长期设施和完成门槛是否适用。
可用或被代理选中，不会自动使完整流程生效。尊重宿主、用户和项目的适用规则；可选流程
要求不可分割的整套执行但与任务不合时，选择其他方法，不把部分执行声称为完整遵循。
普通范围内的方法选择无需反复向所有者申请批准。

### ROT-10 — Audit fixed point

当所有实质候选已裁定、没有新的 decision-relevant edge、剩余表面无法改变决策、外部
边界明确且结束快照已核对时，Audit 停止。

## 4. Plan 与 Operate contract

### ROT-11 — 有限 end state

定义真实 change pressure 与可测试 end state。文件长度、旧名字或两个合法版本本身不构成
refactor 理由。区分已观察行为与期望行为，并记录有意改变。

### ROT-12 — 诚实 candidate workspace

纳入影响所选路径的 staged、unstaged、untracked、ignored、generated 与 configured
inputs。Worktree 或临时副本只组织工作，不隔离网络、credential、process、resource 或
external state。保留无关、并发工作及可恢复的 before-image；显式授权的清理可以修改或退役
选中的 dirty 实现。不要用方便的 clean HEAD 替代实际 dirty baseline。

### ROT-13 — 受保护 witnesses

针对真实 shipping selector 建立相关的 valid、failure、compatibility 与 state-effect
witness。把 baseline behavior witness 与 structural-completion check 分开。不得为了让
候选通过而弱化断言、增加 skip、放宽 tolerance 或重新生成 expected output。

按风险选择足够的证据：现有检查、直接检查、一次性 probe 或长期回归测试。保持行为的重构
可以前后均绿；缺陷 witness 必须暴露该缺陷，测试接线失败不算。能够直接检查的退役可以
沿路径证明，无需强制新建永久测试设施。可行时以安全反例挑战承担关键结论的可执行 gate；
无法取得该观察时说明实质证明边界。允许退役或整合过时测试，同时保留受支持行为的独立
失败覆盖，并更新真正的测试入口。

### ROT-14 — 收敛的 increment

采用能够收敛到完整约定目标的最小 coherent increment。每个 increment 都说明受保护行为、
编辑范围、所需观察与 code/state recovery route。临时 bridge 必须拥有真实 selector、
state ownership、当前用途与 retirement condition。

### ROT-15 — Checkpoint 不等于完成

一个 verified increment 可以作为 checkpoint 保留；当 caller、state owner、delivery
selector 或 retirement obligation 仍未完成时，它不能替代更大的约定结果。预算耗尽只会
缩小 status claim，不会缩小原目标。

### ROT-16 — Implementation loop

每次写入前，把当前依赖与上一个 verified checkpoint 核对。实现一个 coherent increment，
检查真实 diff 与 test edits，运行当前 behavior/structure checks，从当前 source 挑战关键
结论，重新 pin，并继续所有已就绪且在授权范围内的义务。新证据出现时重新规划，避免叠加
speculative fix。验证接入开始主导整轮工作时，比较更窄的可信方法，并在继续前说明实质范围
或成本变化；不要每引入一个 helper 就重启整套工作流。

### ROT-17 — 四类验收义务

根据约定目标采用相关义务：

1. **Behavior：**输出、失败、兼容性与 state effect 正确，包括明确接受的变化。
2. **Structure：**目标 owner separation、dependency removal、selector migration 或
   retirement 真正发生；仍委托旧 owner 的 facade 只是过渡。
3. **Delivery：**请求覆盖的 manifest、package、installed copy、activation 或 runtime
   surface 在每个纳入层都选中目标实现。
4. **Usefulness：**具体 change friction 得到缓解，同时说明保留的测试、配置、接缝与 bridge
   有何用途；有帮助时，用一次性 follow-on change 验证新的边界。

并非每场 operation 都包含所有 delivery layer 或 usefulness probe。必须依据约定目标说明
哪些义务适用，以及为什么排除其余义务。成本收益判断只需简短、具体的依据，无需全项目维护
耗时测量、全局最低成本证明或逐项测试审批。行数、测试数及未来复用预期都不能单独证明收益。

### ROT-18 — 不做表演式 challenge

实质完成声明要接受一次基于当前 source 的反证尝试。诚实记录它是独立 review 还是同一 agent
的 self-check。不要默认 multi-agent fan-out，也不要把格式 validator 或 byte match 表述为
semantic review。

### ROT-19 — Recovery-aware continuity

长时或中断 operation 在 tracked target content 之外保留一份最小 private record：目标、
授权边界、input identity、已完成义务/证据、in-flight increment、owned change/effect、
剩余依赖与下一项 revalidation action。它只帮助恢复，不构成权限或证明。

续做前先观察真实 source 与 effect。acknowledgement 丢失不能证明 effect 不存在。Code
recovery 只处理 task-owned change，并以已知 postimage 为前提；并发编辑要求 reconciliation。
Durable-state recovery 还需分析 compatibility、backup/compensation、intervening write、
idempotency 与 safe-rollback point。

### ROT-20 — 诚实 terminal state

结果只能是：完整约定范围已完成；verified checkpoint 且仍有工作；因精确缺失的观察、能力、
权限或依赖而 blocked；或 aborted/recovered 并说明已观察的残留效果。不得静默缩小范围。
所有者明确选定的阶段具有自己的验收边界，不能事后扩大为全部未来建议。受到质疑时，重新核对
请求、diff 和观察，纠正确认的缺口并保留成立的收益；安抚和道歉都不能代替工程判断的依据。

## 5. 证据与确定性 helper

可选 cited-byte checker 只验证命名文件与行段 bytes。它不证明 semantics、Git identity、
完整 worktree 或 atomic snapshot、安全执行、授权、等价性或完成。缺少安全读取能力的平台
fail closed。

受控 operation lab 对合成仓库应用 evaluator 编写的已知 edits。它必须拒绝 facade-only
完成、未被使用的新实现、过期 declared artifact、重复 side effect、source drift、不安全
replay 与宽泛 recovery。Lab 通过只证明 evaluator 与反例可执行；不证明 autonomous model
能力、任意 refactor、真实 data migration 或 production safety。

未知 target-controlled build、package hook 与 probe 需要合适的 host-enforced write、network、
environment 与 resource controls。Timeout、临时目录、worktree、“dry run”或 permission
field 本身都不能提供这种边界。

## 6. 输出 contract

Audit 以 decision answer 开头，只保留实质 topology、finding/unknown、避免错误判断所需的
non-finding、proof limit、overhead receipt 与 end re-pin。

Plan 说明有限 end state、保留与有意改变的行为、授权边界、依赖顺序、witness、acceptance
obligation、recovery strategy、stop condition 与未决决策，但不编辑目标。

Operate 以用户结果开头，说明实质 changes、保留行为与已接受变化、带 source identity 的关键
checks、completion layer、剩余 unknown 与最终 workspace state。Source、commit、push、
install、activation、runtime、release 与 owner acceptance 必须分开。

## 7. 受控验收

保留原来的六个只读 dirty/clean case 与 negative routing controls。增加 deterministic
cited-evidence 和 operation-lab tests，但绝不把 evaluator-only expected artifact 或已知
patch 泄露进 Skill context。

0.2.0 source-complete acceptance 要求：

- repository、architecture、unit、fixture、operation-lab、Skill 与 whitespace validation；
- request routing 保持 Audit、Plan 与 Operate 边界；
- 一次真实 target-model Audit regression，以及一次由模型完成、再由受保护 witness 独立评估的
  multi-increment Operate forward test；
- 双语 README、AGENTS、product spec、evidence model、architecture docs、current state、
  changelog 与 runtime metadata 一致；
- 检查最终 diff 与 Git state。

Synthetic operation-lab 成功是必要的 evaluator evidence，不能代替 model forward evidence。

0.2.1 在既有 operation lab 中加入方法选择对照对象及夹具测试。声称模型行为改善前，
须在相同宿主、模型和设置下，使用新对象比较固定的基线与候选 Skill；覆盖可选及项目强制的
test-first、被输出检查掩盖的状态副作用、获授权 dirty 退役及只读对照。记录实际 helper 暴露，
检查真实修改与观察，不能按复述规则的用语评分。准备脚本与单元测试不调用目标模型；历史
forward 回执仍只支持其具名 bytes，不会自动证明当前版本。

## 8. Version、installation 与 publication

VERSION 表示当前 source version，并遵循稳定 SemVer 语法。Source `0.2.1` 已发布为最新
公开 tag `v0.2.1`。README 与 current-state 分别报告源码、验证、安装和发布状态；
文档安装引用固定到已经核验的公开 tag。

本地 installation 会先验证 source；内容不同的目标必须显式 replace；被替换的版本进入可恢复
backup；receipt 记录 source Git identity、dirty state、version 与 source/installed digests。
Installation 不证明下一 turn discovery 或 activation。

一份显式 declared file set 同时定义 source validation、digest、staging、installed comparison
与 receipt 所使用的 installable Skill payload。已知 local runtime residue 不属于这份 payload，
也不会进入 staging；其他 undeclared source 或 executable entry 必须 fail closed。因此
matching source/installed digest 只证明 declared payload 相等，不证明 activation，也不证明
installed tree 中没有后续运行生成的 residue。

Commit、push、CI、annotated tag、GitHub Release、tagged install、installed bytes、runtime
discovery 与 owner acceptance 是不同 gate。本规范不授权 installation、release、deployment、
account mutation 或 publication。

## 9. 非目标

不产出 maturity score、通用 hygiene checklist、automatic issue backlog、provider panel、
mandatory multi-agent review、第二套 scheduler/orchestration engine、通用 crash-safe rollback、
exactly-once external effect 或 loop-until-clean repair。保留单一 canonical Skill implementation
与现有 invocation slug。
