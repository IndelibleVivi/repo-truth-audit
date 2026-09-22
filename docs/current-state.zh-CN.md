# 当前状态

[English](current-state.md)

最近核对：2026-09-22

## 产品与源码

Source `0.3.0` 是**未发布 candidate**。它加入已接受产品意图还原，以及与仓库所选行为的
双向对照。仍使用 Audit / Plan / Operate，不增加引擎、强制产品历史扫描或隐含修复权限；
调用 slug 保持 `repository-operational-truth-audit`。

新增 intent reference 纳入明确的九文件 Skill payload；source validation、staging、
installed comparison 和 receipt 共享这份定义。架构保留七区域、31 节点、46 条边；authority、
candidate trace 和 acceptance 现在包括意图生命周期、产品差距与合理演进。双语图与说明
同步反映候选范围。

## Candidate 证据

Source 已完成本轮返修：完整记录 search witness 拒绝 query echo；自然局部采纳、内部委托
与例行人工步骤纳入方法；frontmatter 并列运行事实和产品意图入口，覆盖新建小仓库。
原有 Audit / Plan / Operate 与精确采纳、反向举证规则保留。

117 个 repository tests 通过；repository／architecture／Skill validation、六项原有
fixture self-tests、operation lab、十一项意图 ground-truth 与十一项破坏反例通过。
可选 Field Lab 离线 validation 与六项 self-tests 通过，没有 target-model 调用。

附件脚本对原 `3c27d78` 复现 query-echo 漏检，修正后拒绝假搜索；上轮真正完成的 search
修复通过加强后的 source／重建产物 witness。原始 Atlas 对话未改。
[原 0.3.0 回执](forward-0.3.0-receipt.zh-CN.md)保留历史观察并补充限制；
[本轮返修回执](forward-0.3.0-followup.zh-CN.md)说明新的精确身份、自然对话结果、
合成样本被审计发现的缺口与修正、普通 bugfix／review 反例，以及证据局限。

五个 fresh native session 在可选 candidate catalog 下完成三个产品对照和两个普通工作
对照；修正样本后，三个产品 session 各续问一次。不是八次独立试验，也不是宿主隐式发现。
保留原报告；不得把目标工作流中的测试覆盖限制当成当前功能缺失。

本轮 source／forward snapshot／临时安装的九文件 payload 一致：
`02126bada7a880693ea55e73b9bd9404829c2f9b99ca2357b462506e900f492a`。
安装 receipt 如实记录 dirty source。架构拓扑与双语 SVG 本轮未改变；此前视觉验收属于
原回执，不作为本轮新验收。Source 交付、日用安装、release 与 host discovery 分开记录。

## 稳定版与安装

最新已核验公开版仍为 [v0.2.1](releases/v0.2.1.zh-CN.md)，2026-09-20 发布。Annotated tag
peel 到 `6485296b39b7fc8526713cda5e8df01c679a4ec6`；当时 release record 记录四项
[CI jobs 通过](https://github.com/IndelibleVivi/repo-truth-audit/actions/runs/35503842279)，
公开 tag 临时安装与八文件 released payload 一致。这些是历史观察，不是 candidate CI
或 activation 证据。README 稳定安装命令继续固定到该版本。

[0.2.1 forward 回执](forward-0.2.1-receipt.zh-CN.md)、
[0.2.0 forward 回执](forward-0.2.0-receipt.zh-CN.md) 及
[0.2.0 发布记录](release-preparation.zh-CN.md) 保留原有证据与限制，不据此声称 0.3.0
相较旧版效果更好。

本候选工作不升级日用 Skill、不创建 release tag、不发布 GitHub Release，也不证明 fresh
host discovery。Source、Git 交付、安装和 runtime selection 仍是不同观察层。

许可不变：功能材料为 SUL-1.0 source-available；独立公开文档与图使用 CC BY-NC-SA 4.0，
路径边界见 [LICENSING.md](../LICENSING.md)。
