# `0.3.0` candidate 返修证据

[English](forward-0.3.0-followup.md)

观察日期：2026-09-22。本轮修复已实际复现的 evaluator 漏检，检查自然对话、流程增负和
受控方法选择；不发布或升级日用 Skill。[原回执](forward-0.3.0-receipt.zh-CN.md)保留原有观察。

## 身份与边界

- 起始 source：`3c27d7810982c6a65d5eef1f0d9a054aaa685aca`。
- Source 为未发布 `0.3.0`；稳定 release／日用安装仍为 `0.2.1`。
- 九文件 candidate Skill payload：
  `02126bada7a880693ea55e73b9bd9404829c2f9b99ca2357b462506e900f492a`。
- 五个 fresh native session 请求 `gpt-5.6-sol`、high reasoning，无主对话 fork：三个产品
  对照、两个普通工作对照。修正 fixture 后，三个产品 session 各续问一次；不是 fresh 或盲测。

初始自然请求均未写 Skill 名。目标先读明确提供的可选 catalog，其中包含 candidate
描述与路径，再选择是否使用。三个正例报告读取固定 Skill 及 intent／audit references，
两个反例报告没有使用。这是给定 catalog 的受控选择，不是实际宿主自动发现证明。
Shared host／project guidance 仍适用，一个目标还报告使用 Servotab；不是 RTA 单因素实验。

目标只收到合成产品文件和请求，没有 case catalog、checker 或预期答案。原始私人对话、
附件、私有 trace 与本机路径不公开。只允许新增指定报告，或实现那个明确 bugfix；会写状态
的探针在临时副本运行。这些约定不提供 OS 隔离。

## Search evaluator：实际 RED 与 GREEN

提供的复现脚本直接导入原 checkout 的 `assert_operate_repair`，确认
`print(args.query); return 0` 能通过 source 和重建产物验收；一个从未出现过的查询仍被
原样吐出。这是实质漏检。旧 substring witness 未能证明返回值来自匹配记录。

修正后使用完整且非平凡的 digest 消息，逐一比较 JSON 数组：多个匹配、单个匹配、无匹配、
已有保留内容及仅存在于原始库的内容。**第一次 search 前**保存 store／digest bytes，每次
查询后分别比较；尚未 digest 的消息故意让两个文件不同。仍在隔离副本验证 source 与按声明
重建的交付物。

已观察结果：

- 同一附件脚本返回 `FAKE_REPAIR_REJECTED`，exit 0。
- 回归测试拒绝普通 query echo，以及语法有效的 JSON `[query]` echo。
- 拒绝绕过 digest 搜索原始库、输出正确但首次查询修改数据的实现；继续拒绝缺交付成员和
  改写 authority 的实现。
- 真正读取 digest 的参考修复通过，候选原件不变。
- 上轮 forward 实际完成的 search 修复也通过更强 witness 的 source／重建产物检查。
  evaluator 原先有洞，不等于上轮修复错误。

Atlas 原始对话证据不变。完整记录 JSON 输出写在**当前 paired Operate 请求**中，与上轮
接受的修复一致；没有伪造历史 owner 决定。账号内容混用及持久数据迁移继续留在有限 search
修复范围之外。

## 自然对话与工作流程观察

Harbor Dispatch 使用自然中文、局部采纳、相邻而未采纳的 assistant 提议，以及内部接线委托；
没有 `Adopted`／`Rejected` 标签。后续对话将当前本机演示改成逐项人工练习，同时保留
cloud／team 排除边界。增负样本与后续授权样本的实现、README 和 tests 完全相同，只有对话不同。

首轮三个独立 Audit 均选择 candidate 方法，并且：

- 还原直接派工、可选观察的正常使用约定，承认 state 模块属于实现委托，不要求逐函数批准；
- 识别每项任务的 receipt／state／confirm 前置条件造成未经接受的例行劳动，即使功能测试全绿；
- 承认后来明确授权的人工流程是在当前本机范围内合理演进，不把低摩擦变成永久要求。

目标还发现了合成“干净”样本的真实缺口：聊天承诺刷新按钮，样本只有 JSON CLI；教学流程
只检查三个字段是否存在，没有执行约定顺序。协调者复现两点，保留首轮报告和 before-images，
修正合成实现，没有丢弃发现或改写聊天。直接派工样本还移除了未采纳的人工命令和说明，并让
feature test 直接派工，不预填人工状态。

修正样本加入可选的 loopback 观察面板及已接通刷新按钮，并要求 receipt → ready → confirm。
普通 lab validation 直接执行面板 response 路径，不监听端口。另一次协调者 loopback 探针
验证 HTML、派工后的最新共享状态及读取不修改 bytes；没有观察真实浏览器点击。
原始提供对话保持 byte-identical。

三个 same-session 续问对修正样本给出的判断：

| 当前样本 | 观察判断 |
| --- | --- |
| 直接派工 | 没有已证明的当前产品偏差；直接派工、内部委托与可选刷新面板符合约定，未采纳的人工命令已退出。 |
| 未授权人工 gate | 面板缺口已关闭，但每项新派工仍被 receipt／ready／confirm 阻断，违背当前约定；功能正常、smoke 全绿不能消除差距。 |
| 相同 gate，后来明确接受 | 当前教学范围内人工顺序合理；错误顺序拒绝和真实 loopback 面板支持一致性，不把原来的低负担偏好追溯强加回来。 |

目标将剩余 target-smoke 覆盖风险与当前行为缺陷区分开。这些窄 smoke 有意保留为不足以
裁定产品一致性的证据；外层 lab 独立保护 fixture 的流程／顺序与面板 response 语义。
本轮不把合成产品升级为完整回归测试的应用。观察后更正了一处 smoke docstring；这是
comment-only 修正，不冒充新行为试验。协调者完整读取六份产品报告，独立核对原始文件、
HEAD 和 index 不变，只增加获准报告。

## 普通工作对照

| 自然请求 | 观察结果 |
| --- | --- |
| 修复一个已约定的空 query parser bug | 选择普通工作；空输入成为 argparse usage error（exit 2），非空内容及空格原样保留；只修改对应 source 文件。 |
| Review 现有两行 parser patch | 选择普通 review；发现空输入错误返回成功；目标文件无修改。 |

协调者独立核对 repository bytes、HEAD／index 与对应命令行为，也核对正例仅写报告的边界。
方法使用／未使用来自目标自报；文件与行为检查本身不证明完整 instruction-read trace。

## 证据范围

原八项 intent subjects 保留，新增三项流程样本。十一项确定性 ground-truth 检查及十一项
破坏反例通过，target-model／network calls 均为 0；它们验证 fixture，不证明模型理解。
完整测试和交付状态见[当前状态](current-state.zh-CN.md)。

临时安装与 candidate 九文件精确一致，receipt 如实标记未提交 source snapshot；不据此
声称日用安装、tag、GitHub Release 或宿主发现。

每条件一次，没有旧版对照；修正样本采用已有上下文的 same-session 续问。不外推普遍触发率、
相较旧版效果、任意仓库有效性、浏览器验收或全部差距类别。原有精确采纳与反向举证规则保留；
没有新增引擎、模式、强制历史档案或审计 backlog。
