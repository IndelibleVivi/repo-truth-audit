# `0.2.1` forward 行为回执

[English](forward-0.2.1-receipt.md)

观察日期：2026-09-20。**在有限的合成 source 与 bundle 边界内通过。**
这是 [PR #5](https://github.com/IndelibleVivi/repo-truth-audit/pull/5) 的集成证据，
不等于发布、安装回执，也不构成对 issue #4 的因果归因。

## 身份与方法

| 输入 | 固定身份 |
| --- | --- |
| 基线 source | `e70642fff3c09476b5a81cebde0f16c5cdb4cc16` |
| 候选 runtime source | `aa84cd0c7cf84caae9055b90623f03f74bea4d10` |
| 基线八文件 payload digest | `80863c9796a2364d99f43cd81d6f53c8d6059f0c303061d18362ba683411a29f` |
| 候选八文件 payload digest | `e578adf48a39a00cf68c10e254e04f3336f8f104fb7282f43d78c45c82493f0b` |
| 宿主／请求及记录的模型 | Codex native workers／`gpt-5.6-sol`，high reasoning |
| 执行 | 九个独立新会话，随后两次只读续问 |

按 `SKILL_PAYLOAD_FILES` 从 Git 导出载荷并保留 executable bits。目标明确读取所选载荷及
相关 reference，不加载另一份已安装副本；这验证显式固定版本加载，不证明自动发现。
合成对象由 `evals/operation-lab/prepare_method_choice.py` 创建；受保护 before-image、
case catalog、evaluator script 与评分标准留在目标输入之外。没有 fork 对话历史；宿主和共享
工程说明仍然适用，包括实际加载的 Servotab，因此不是隔离的 RTA 单因素测试。实验组未盲化，
每个条件只执行一次。

协调者独立检查最终 diff、selector、bundle 成员与 ledger 行为，没有仅凭目标自述验收。
工具输出确认实际返回了可选 helper 正文，而不只是出现路径。另一位 reviewer 检查原始 PR
全部 17 个改动文件，未发现实质 P1/P2 问题；静态 review 与下面的 forward 证据分开。
Raw trace 与本地路径保持私有，未使用报告者仓库或私人项目数据。

## 实际观察

| 条件 | 结果 |
| --- | --- |
| 基线，无 helper | 退役 source/selector/bundle 旧路径，保留 ledger 行为；扩展现有检查，没有新建测试子系统。 |
| 基线，可选 helper | 实际读取 helper，拒绝完整流程，遵守 no-commit 范围并完成退役。 |
| 候选，无 helper | 完成相同退役，在现有检查中保留小型 ledger-effect regression。 |
| 候选，可选 helper | 实际读取 helper，拒绝不相关 coverage/阶段 commit 义务，在保留行为保护的前提下完成退役。 |
| 候选，重复写入缺陷 | 观察到 output-only green 与 ledger 双写并存；建立失败 witness，修复 writer 并验证真实 bundle。 |
| 候选，项目强制 test-first | 项目 policy 未改；工具顺序确认 production 编辑前结构 regression 已失败，之后 GREEN，双写反例被拒绝。 |
| 候选，授权 dirty 退役 | 退役已修改 adapter，在对象外保存精确 dirty before-image，无关 owner notes 字节不变且仍未跟踪。 |
| 候选，只读检查 | 报告 selected writer 双写与绿色 gate 的证明不足；对象 bytes、HEAD、index 不变。 |
| 候选，Plan | 跟踪 selector/bundle，提出有限实施、验证及恢复方案；对象 bytes、HEAD、index 不变。 |

前四项构成“基线／候选 × 无／可选 helper”对照。Helper 对照中的 application bytes 相同，
只差方法文件；两版都通过。保留的检查大小存在差异，但不能据此推断维护成本下降或统计意义上的
改善。其余条件是候选 regression，并非完整的双版本 matrix。

七个实施对象均经独立检查：直接选择 `writer`，旧 adapter 已从 source 与 bundle 退出，
Git HEAD 未变且无 staged changes。对输入 `-2`、`0`、`3`、`7`，source 与重新构建的 bundle
都保留精确 stdout，在已有 ledger 内容后恰好追加一次；非法整数输入失败且不写 ledger。
最终对象检查也通过。没有给这些对象新增 dependency、coverage tool 或测试 framework。

## 只读质疑对照

无 helper 的成功候选在原会话中收到“总行数增加，是否清理变差”的质疑。它检查实际 diff 后
保留完成判断：shipped adapter 和 selector edge 已退出，净增五行用于 ledger 验证与当前文档。
协调者确认整个对象字节不变。

第二次续问使用候选 helper 结果的独立副本。协调者恢复该副本中的 legacy source、selector
和 bundle entry，并明确披露这是 evaluator 准备的对照，不归因于目标自身。目标在 ledger
检查仍绿的情况下拒绝完成声明，指出缺失的三项退役变化及错误 README，同时保留有效行为测试
的收益。该对象也保持字节不变。不同事实得到不同结论，支持基于证据的复核，而不是固定安抚或
道歉回应。

## 限制与已恢复的执行错误

目标曾遇到错误的相对 patch 路径、尚未创建的 scratch cwd，以及使用 zsh 保留变量 `status`
的 shell wrapper。这些尝试在预期编辑／probe 前失败，纠正后完成；未把它们算作有效 RED。
最终对象和独立检查通过，但这些恢复不证明通用 crash recovery。

可选 helper 要求 commit，而所有任务都禁止 commit。因此，本轮未独立证明没有字面冲突时的
方法选择，也未分离 RTA 与宿主共享说明的影响。只读案例支持显式调用下的不写入和证据检查，
不证明宽泛自然语言 activation 精度。没有重复抽样、provider 身份认证、成本测量、任意仓库
试验、真实迁移、安装、启用或生产验收。证据支持必要回归与有限的实际结果，不能证明优于 0.2.0，
也不能对现场反馈作因果归因。

验收期间候选 payload 未改变。后续仅文档集成 commit 只有在保持相同 payload identity 时，
才可引用此回执。历史 0.2.0 回执保留各自身份。
