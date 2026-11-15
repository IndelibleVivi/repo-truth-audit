# 当前状态

[English](current-state.md)

最近核对：2026-11-14

## 本地接续——2026-11-14

本地 checkout 从 clean 且与远端一致的 `research/user-outcomes-20261113`
`89e3ec6ca668233925b45b3a5d215ce572a86df2` 接续。原研究及 CI 保留原身份。
新鲜基线通过 147 tests、两个 validators、六项 fixture self-test、十三项 intent case、
十四项 packet 修复挑战、离线比较器与 Skill validation。同一固定 companion 的独立
Field Lab v2 迁移、validate 和六项 self-test 也通过；v1 pack 未改，这些检查目标调用为零。

本机 `codex-cli 0.159.1` 已通过 `skills/list` 返回临时项目 Skill 的精确路径，无发现错误。
synthetic markers 同时证明该构建仍读取旧 project/user 根目录，因此保留安装器默认值，
现代根目录继续使用显式 `--dest`。发现元数据、读取载荷与正确任务行为分别裁定，见带日期的
[宿主观察](host-compatibility.zh-CN.md)。

随后恰好三次 fresh native 调用完成 Audit、Plan 和有限 Operate。Audit/Plan 全部目标字节
不变；三次 completed tool trace 均读取 project Skill。Operate 经 manifest 所选产物交付
`artifact-v2`；在副本放回旧产物后，distribution 检查失败、source 检查仍绿。host usage
字段如实保留，不换算人工成本或生产率。

可选[安装包 probe](../evals/field/README.zh-CN.md) 在固定 PyPA sampleproject 源码上新增
构造的 wheel/editable 选择实验。八次真实 import 读取区分只改源码和重建交付，同时保留
owner 后续编辑后冻结 wheel 合法不变的邻例。wrapper 分开 setup failure 与已运行 consumer
失败；九项离线测试保护这些裁定与输出路径。

离线比较器现拒绝名为 `without-skill`、实际 exposure 却为已加载 Skill 的样本，保留污染
运行但不产生成本差值。明确比较两种已加载 treatment 仍可合法匹配。原始四组配对的结果
不变；十二项比较器测试通过。

Live 比较前，本地接续完整回归通过 **169 项 repository tests**、两个 validators、六项 fixture self-test、
十三项 intent case、十四项 packet 挑战、原配对比较器、Skill validation 与 diff 检查。
新 [consumer-first 协议](../evals/experiments/2026-11-consumer-first/README.zh-CN.md)
及执行设置已在 live 被试调用前冻结。

`03e3706` 首批因未接触结果的独立 review 发现三项 setup/oracle 缺陷而停止，尽管当时
CI 全绿。十二次启动均保留 unjudged。修复已通过独立反例及最新完整 **172 tests**。
修正批随后在八次启动后因协调者的公共 prompt 错把 clean 任务只读范围施加给实现任务
而停止；其中两个 clean 控制也在必需报告之前中断。这些属于 setup／截断观察，
不是 Agent 修复失败。

余下四次用明确写权限执行，并用尽 24 个会话上限。两个普通修复均通过源码、实际交付
ZIP、回归和报告检查；两个 migration 检查点均通过行为、结构和实际 ZIP 检查，却在时间
上限前未产生必需报告，不能记成任务完成。四次均保持登记的受保护字节。只有普通配对
比较完整任务成本。两个 migration 因缺少必需报告判为完整任务 deadline 失败；截断计数
不是成功交付成本，不推导因果或人工审阅收益。见
[结果与限制](../evals/experiments/2026-11-consumer-first/results.zh-CN.md)及
[setup 修正](../evals/experiments/2026-11-consumer-first/setup-recovery.zh-CN.md)。
被试进程全部停止，本登记不再有可用调用。四任务／三组平衡比较仍未完成。

源码交付 `03e3706`、`3df91f4`、`27dfe50` 已推送研发分支，各自 push 与 PR CI 通过。
最终回执／文档后续保持相同 task/evaluator 实现和 Skill payload；branch head 与其新鲜 CI 另行解析，
不把此前 CI 归给后来的 commit。

source 版本保持 `0.3.0`，本轮不移动稳定 tag、不 release、不 merge、不升级日用安装。
下方历史证据保留原日期，不改标成新鲜结果。

## 未发布的用户结果研究分支

`research/user-outcomes-20261113` 从 main
`9fd099b6c9e88be2d7c809b021add51a5c8d6b8f` 继续，本轮末尾已重新核对 upstream main
仍为该身份。source 版本保留 0.3.0；本轮未移动 main、公开 tag 或稳定安装 pin。
源码研发、正式发布和用户日用安装继续分别决定。

权威方法现在明确接收方、可得输入、编译器/宿主进入门槛及合法相邻用途。已测试九文件 digest：
`28b73009402e0f149c7078379a15d51cf88468c66ec092f49a59a5f6926fb211`。
临时安装匹配该 digest，回执如实记录 dirty source；不据此推断原生发现或日用升级。

### 本轮新鲜证据——2026-11-13

- 最终完整本地运行 **147 项仓库测试通过**，包含 operation lab、安装行为、16 项 task-intent、
  10 项比较器测试及受保护输出路径回归。Repository、architecture、Skill validation 和
  git diff --check 通过。
- 首次远端矩阵在 macOS/Python 3.10 暴露 Git 自动维护与 fixture 字节快照的竞态。
  真实 Git Trace2 回归现验证两个初始化器不再留下后台维护；产品 tree、本地 Git 配置和
  完整快照断言保持不变。
- 六项 fixture self-test、十三项 intent truth、十三项破坏对象拒绝通过，目标模型调用均为零。
- Cedar 最终修复自挑战 **14/14**：接受两种合法实现，拒绝十二种负例。八个在研究前 main
  被接受的候选，用该精确旧源码再次复现，最终判据全部拒绝。独立 review 另外发现两个继承的
  平台缓存通道，保留 RED/GREEN 与 ASCII locale 修复证据。
- 四组自然任务 **8/8 产物独立成功**，没有成功率优势。执行命令自报数为控制/候选
  15/15、6/13、8/10、6/10，均为 proxy；人工时间与 token 不可得。旧接续 oracle 对合法转发
  shim 的拒绝与当前任务验收分别保留。两份实际交付 ZIP 通过，两份 Cedar 也通过最终加强判据。
- 固定真实消费者矩阵通过：python-dotenv 十九次进程观察，mitt 四种 package/type/runtime
  变体，Viper 七种变体/十二次读取及 setup/仪器控制。CWR 旧 held-final 路径失败，当前真实
  runtime 状态路径通过，四项针对性负案例通过。这些是有限机制证据，不是全仓库认证或自然发现。
- 可选 Field Lab 0.2.1、commit 6f79c5717da8bc0639fa0d70f5d82b64c231b9c5 将原 v1 pack
  显式迁移到独立 v2 工作区，validate 与六项 self-test 全通过，semantic_change=false，
  目标调用为零，canonical pack 未改。

本地 Codex CLI 在只读运行路径初始化 app-server 失败，未发生模型调用。Claude Code、
Gemini CLI、OpenCode 入口只核对了文档，没有原生运行声称。当前 Codex .agents/skills 指引
与安装器保留的 .codex/skills 默认不同，仍须明确目标并观察实际选择。CWR 的新状态字段在
Windows/OpenCode 中如何显示，尚未观察。

见[完整研究](user-outcomes-study.zh-CN.md)、
[配对实验](../evals/experiments/2026-11-user-outcomes/README.zh-CN.md)、
[宿主边界](host-compatibility.zh-CN.md)、[本地 Codex 委托](codex-handoff.zh-CN.md)。
架构仍为七区域、31 节点、46 条边，未重画图，也不声称新增视觉验收。

## 较早的未发布 main 改进——2026-11-07

Main 保留 source 版本 `0.3.0` 和九文件载荷，新增尚未发布的具体任务有效性审查：分别判断
当前任务局限、历史承诺与改进提案，保留合理用途和必要专业判断，沿用 Audit / Plan / Operate
边界。Lumen 发布判据现检查正文绑定；Cedar 新增修订/摘要两用途对照及源码/重建产物修复验收。

稳定安装仍固定到冻结的公开 `v0.3.0` tag，不包含这次 main 改进。本轮不更新日用安装、tag
或 Release。当前检查和 fresh 模型观察与下方带日期的发布基线分开记录。

当时的本地检查：128 个 repository tests、repository/architecture/Skill validation、
六项 fixture self-tests、十三项 intent truth 和十三项破坏检查。四个 fresh native 审查与
两次配对实施续做均支持所选任务，两份修复均通过独立 source/artifact 检查。不宣称新增优势
或自然发现，见[任务有效性回执](task-effectiveness-followup.zh-CN.md)。当时可选 Field Lab v2
无法运行 legacy-v1 pack，未进行迁移；2026-11-13 观察到的显式迁移另记于上方。

## 已发布 v0.3.0 基线（2026-09-22）


Source `0.3.0` **已作为 v0.3.0 发布**。它加入已接受产品意图还原，以及与仓库所选行为的
双向对照。仍使用 Audit / Plan / Operate，不增加引擎、强制产品历史扫描或隐含修复权限；
调用 slug 保持 `repository-operational-truth-audit`。

新增 intent reference 纳入明确的九文件 Skill payload；source validation、staging、
installed comparison 和 receipt 共享这份定义。架构保留七区域、31 节点、46 条边；authority、
candidate trace 和 acceptance 现在包括意图生命周期、产品差距与合理演进。双语图与说明
同步反映 0.3.0 范围。

## 已冻结的发布载荷与证据（2026-09-22）

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

## 公开发布与安装（最后核验于 2026-09-22）

最新已核验公开版为 [v0.3.0](https://github.com/IndelibleVivi/repo-truth-audit/releases/tag/v0.3.0)，
于 2026-09-22 14:35:42 UTC 发布，回读为 Latest、非 draft、非 prerelease。当时仓库为 public，
默认分支为 `main`。

- 发布 commit：`6de6dae92f17efbef3cf8ad4e9e98eb6bdd5a61b`。
- Annotated tag object：`a0c5ec764d28d8fa221a0a5717f0f30c0409edc3`，peel 到该发布 commit。
- [发布 commit CI](https://github.com/IndelibleVivi/repo-truth-audit/actions/runs/35741057255)：
  Ubuntu/macOS × Python 3.10/3.13 四项全部通过。本地发布检查也通过 117 tests、两个
  validators、fixture/operation/intent 检查与 Skill validation。
- 系统安装器从公开 tag 下载到临时目录，得到明确九文件、无额外条目和上述冻结 digest。
  公开 README、license 与 package 路径均返回 HTTP 200，字节与 tag 一致。
- README 稳定安装固定到 `v0.3.0`。日用 0.2.1 未升级，八文件 digest 保持
  `e578adf48a39a00cf68c10e254e04f3336f8f104fb7282f43d78c45c82493f0b`。

Tag 保留发布前文档快照；发布后续只回写核验状态，没有移动 tag 或改变 tag 载荷。
上方未发布的 main 改进改变了当前 source 字节。
详见 [v0.3.0 发布说明](releases/v0.3.0.zh-CN.md)。

旧版 [v0.2.1](releases/v0.2.1.zh-CN.md) 于 2026-09-20 发布。Annotated tag
peel 到 `6485296b39b7fc8526713cda5e8df01c679a4ec6`；当时 release record 记录四项
[CI jobs 通过](https://github.com/IndelibleVivi/repo-truth-audit/actions/runs/35503842279)，
公开 tag 临时安装与八文件 released payload 一致。这些是历史观察，不是 v0.3.0 CI
或 activation 证据。

[0.2.1 forward 回执](forward-0.2.1-receipt.zh-CN.md)、
[0.2.0 forward 回执](forward-0.2.0-receipt.zh-CN.md) 及
[0.2.0 发布记录](release-preparation.zh-CN.md) 保留原有证据与限制，不据此声称 0.3.0
相较旧版效果更好。

本次发布不升级日用 Skill，也不证明 fresh host discovery。Source、Git 交付、安装和 runtime selection 仍是不同观察层。

许可不变：功能材料为 SUL-1.0 source-available；独立公开文档与图使用 CC BY-NC-SA 4.0，
路径边界见 [LICENSING.md](../LICENSING.md)。
