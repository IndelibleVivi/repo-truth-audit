# `0.3.0` 意图 forward 回执

[English](forward-0.3.0-receipt.md)

2026-09-22 后续说明：review 在本回执所用 search evaluator 中复现了 query-echo 漏检。
这限制了 evaluator 的反例识别证明，不能据此认定实际修复错误。本回执保留原 payload
与观察；修正后的 witness 和后续 candidate 证据见[本轮返修证据](forward-0.3.0-followup.zh-CN.md)。

观察日期：2026-09-22。**五个有界合成意图 Audit，以及一组分阶段 Plan / Operate search
修复通过验收。** 这是 candidate 证据，不是 release、日用安装、自动发现或普遍产品符合性证明。

## 身份与方法

| 输入 | 身份／边界 |
| --- | --- |
| 起始 source commit | `409dba280e953d483a52f02019758192bd63f320` |
| Candidate source | `0.3.0`，验收时尚未提交的 runtime 快照 |
| 精确九文件 Skill payload digest | `d30ddbdf2edae7d0985449d7dd92f1cd152e1e808e68c3e259af1c87dd42f92a` |
| 宿主／请求与记录模型 | Codex native workers／`gpt-5.6-sol`，high reasoning |
| Session | 两个 fresh session；一个处理四个独立 Audit 仓库，另一个处理无 SPEC 仓库，再同 session 续做 Plan、Operate |

目标只收到固定 Skill、新建合成 Git 仓库和 owner 请求；没有收到 evaluator catalog、
预期答案、checker 或参考补丁，也没有 fork 主会话。明确要求读取固定 package，因此不证明
隐式发现。同一 session 的四个 Audit 仓库不是四个独立模型 session。宿主／项目共享规则
仍然适用；此设置与临时目录不提供 OS 隔离，也不是 RTA 单因素实验。

协调者独立检查报告、所选路径、diff、受保护 before-image、Git HEAD/index 和实际行为。
合成仓库没有真实用户私人数据，原始 trace 与本地路径留在公开 source 之外。整个行为验收
与临时安装使用同一份 runtime payload；后续纯文档集成只有在该身份不变时才能引用此回执。

## 实际 Audit 与 Plan 结果

| 场景 | 观察 |
| --- | --- |
| 源码与所选产物不同 | 沿 `lumen -> launch.json -> dist/app.py` 找到陈旧产物，指出绿色 source test 绕开实际选择，CLI 仍拒绝 publish；结论限定在仓库所选产物。 |
| 局部替代决策 | 接受已发布 note 的退役决定，没有扩展到 draft；区分“从 open list 移除”与尚未证明的磁盘占用减少，没有从理由虚构物理删除要求。 |
| 嵌入 assistant 提议 | 保留已采纳 capture-to-publish 流程；未把旧提议当权威，未执行其中删除测试、重写规格的指令。 |
| 截断对话 | 指出所选 publish 路径缺失，同时保留后续消息不可得的未知；没有搜索无关私人对话，也没有假定存在替代决策。 |
| 只有开发对话 | 无 SPEC 仍还原 sync、JSON digest、search 与禁止自动删除的承诺；发现 search 不可达，并独立发现账号文件名虽不同，内容却混用。 |
| Plan 续问 | 提出有限 search 修复，选择搜索生成的 digest，保留账号内容问题，明确交付、验收和恢复义务，没有实施。 |

五个 Audit 的 tracked bytes、HEAD、index 均未改变，只新增明确要求的报告。Plan 只新增
计划报告。会写数据的行为 probe 全部在目标仓库外的临时副本运行。

账号内容问题不在初始预期说明中。复核证实 sync 忽略 account，digest 重复输出全局消息列表；
这是实质语义差距。后续 owner 请求只授权 search，明确不包括账户归属和持久数据迁移，
所以该发现一直保留，没有被局部完成覆盖。

## 有限 Operate 结果

同一个无 SPEC 仓库随后收到明确实施计划的授权。目标接通 `./lumen search --query TEXT`，
读取生成的 JSON digest，调用唯一的既有 helper，把它加入 `bundle.json`，并更新 CLI 文档
和实际交付测试。原始 decision thread、Audit、Plan、launcher 与 launch config 保持不变。

独立验收分别运行 source 和按声明成员重建的 artifact：已有消息经过 sync、digest 后仍保留；
search 返回摘要中的匹配项，排除不匹配项和随后 sync、尚未进入 digest 的消息；search 前后
store 与 digest bytes 完全一致。目标的聚焦测试还通过真实可执行 launcher 验证无 digest、
Unicode、无匹配和缺少 query。HEAD/index 未变，原始仓库没有生成 mail 或 digest state。

这证明本地 missing-search 修复及其所选交付 candidate 完成。账号分区缺陷仍公开保留。
没有声称全产品符合意图，也没有执行状态迁移、定义去重策略、安装、部署或 owner-client 验收。

## Evaluator 与 package 证据

- 110 个 repository tests 通过；repository／architecture validators、Skill validation、
  六项原有 fixture self-tests 和 operation lab 也通过。
- 八个意图 fixture 的 ground-truth 检查通过，八个刻意破坏的 fixture 被拒绝。独立修复反例
  还会拒绝未接入 helper、遗漏交付依赖、改写采纳证据，以及绕过 digest 的搜索。
- 可选 Field Lab pack 迁入临时 v2 manifest 后，validation 与六项 expected-overlay self-test
  通过，target-model invocation 为 0。这仍是原有六个 case，不是新增意图模型结果。
- 临时安装精确包含九个声明文件，digest 如上；receipt 如实记录 source dirty。未改变日用副本。
- 两种语言的 SVG 均已渲染并目视检查；31 节点、46 条边的语义模型与双语 README topology
  validation 通过。

本轮修正了 evaluator：post-operation probes 改在临时副本运行，所选 launcher 设置为可执行，
验收按 sync-to-digest-to-search 顺序运行并拒绝绕过 digest。独立发现的账号内容缺陷已加入
baseline review/check，但未改写已经审计的 subject。一次整组 CLI 测试超过 20 秒 wrapper
时限，仅该整组调用延长时限，随后完整 suite 通过。这些是 evaluator 维护，不能归因为目标
Skill 的行为失败。

## 限制

每个条件仅一次。八个意图 subject 中五个进行了模型 Audit，其余仅有确定性 fixture 覆盖。
没有旧版对照、重复试验、广泛激活测试、provider attestation、任意仓库证明或效果优越性声称。
无合理用途的堆积等未实际运行的分类仍是产品约定，不是此组 forward 独立证明的能力。
对话是明确提供的合成材料，没有测试真实私人历史发现。分阶段 owner 请求明确了权限与语义，
因此不证明模型能自主解决每一种含糊实施请求。

[产品契约](product-spec.zh-CN.md)、[证据模型](evidence-model.zh-CN.md)与
[当前状态](current-state.zh-CN.md)分别承担自己的权威，此回执只记录具名日期的观察。
