# 交给本地 Codex 的完整接续委托

[English](codex-handoff.md)

准备日期：2026-11-13。把以下工作单交给能够访问仓库的本地 Codex。它应直接沿已经完成的
研究和代码继续实现与验证。目标是形成有实际价值、可移植的有限工程介入，并证明额外审阅与
协调成本值得付出。

## 接续更新——2026-11-14

本委托首次准备于 2026-11-13。本地已从 `89e3ec6ca668233925b45b3a5d215ce572a86df2`
恢复，之前研究保留历史身份。重复 probe 前先按[当前状态](current-state.zh-CN.md)
确认最新验收和剩余工作。

本地接续已完成原始源码基线、Codex 0.159.1 原生发现及显式 Audit/Plan/Operate 烟测、
临时精确路径 disable 控制，以及真实 wheel/editable 安装选择例子。installer 默认值和
canonical 九文件 Skill 未改。离线比较器现从两个方向拒绝污染的 `without-skill` exposure。
见[宿主证据](host-compatibility.zh-CN.md)、[实战 probe](../evals/field/README.zh-CN.md)
和 [consumer-first 协议](../evals/experiments/2026-11-consumer-first/README.zh-CN.md)。
新协议须先通过正/负控制并冻结实际 host 设置，再独立进行最多十二次 live 被试调用。
Windows/OpenCode UI 验收仍需精确环境，本轮没有该本地消费者。不隐含 merge、tag、release
或日用升级。

## 从这些已完成结果继续

研发分支为 `research/user-outcomes-20261113`，起点是 main
`9fd099b6c9e88be2d7c809b021add51a5c8d6b8f`。开始编辑前解析实际交付 commit 和本地改动，
不要 reset 所有者 checkout。source 版本仍为 0.3.0；公开 v0.3.0 固定在
`6de6dae92f17efbef3cf8ad4e9e98eb6bdd5a61b`。

按以下顺序阅读：

1. [AGENTS.md](../AGENTS.md)、[当前状态](current-state.zh-CN.md)、
   [研究决策](user-outcomes-study.zh-CN.md)。
2. 权威 [SKILL.md](../skills/repository-operational-truth-audit/SKILL.md) 和其渐进 references；
   涉及产品边界时查[产品合同](product-spec.zh-CN.md)与[证据模型](evidence-model.zh-CN.md)。
3. [自然试验与回执](../evals/experiments/2026-11-user-outcomes/README.zh-CN.md)、
   [实战 probe](../evals/field/README.zh-CN.md)、[宿主证据](host-compatibility.zh-CN.md)。

最确定的成果是评价器修正，尚无模型增益证明：旧 Cedar 检查接受了依赖缓存的假数据包修复。
新的接收方切断生产上下文，经源码与声明产物检查交错历史。独立 review 又发现普通平台缓存
通道及 locale 依赖，本轮保留其回归证据。离线比较器现拒绝把尚未判定的任务或不同判定口径
展示成可比较的成本提升。

四组自然任务两边均成功。自报执行次数为 15/15、6/13、8/10、6/10；人工、token 和审阅时间
不可得。摘要任务两边都正确保留专业判断。无 Skill 接续的非选中转发 shim 满足当前任务，
虽然旧 lab 要求物理删除；保留原始拒绝及适用性说明，不改写旧 lab 合同，也不把它算成 Agent 失败。

自然试验的冻结 Skill digest：
`28b73009402e0f149c7078379a15d51cf88468c66ec092f49a59a5f6926fb211`。
后续修改权威 Skill 会产生新处理身份。保留旧回执并建立新快照，共用版本号不能替代字节身份。

## 直接执行的工作单

在已交付研发成果上继续源码实现与验证。保留 Audit/Plan/Operate、按范围采纳的意图、专业
判断、合法兼容及九文件载荷。使用宿主已有工具。普通已授权源码研发与新 release、用户安装
效果分别处理。

### 1. 对齐并验证已交付工作

观察物理/Git root、branch、HEAD、dirty/index 与 remote 关系，检查实际 diff 和已有证据。
对齐后运行下面仓库门槛；只有代码、依赖或具体未决问题发生变化时才复跑外部 probe。
直接进入需要继续的实现，不重启泛泛探索或用新计划替换已完成工程。

确认生产/接收检查继续拒绝本地可成功往返的缓存假修复，实际产物检查仍能区分只改源码，
合法替代编码继续通过。保留非 UTF-8 locale 回归及输出路径保护，避免证据文件覆盖被观察产品。
预期结果变化前先审查证明边界。

### 2. 关闭最近的原生宿主未知

临时安装包已核验；本环境 Codex CLI 在只读运行路径初始化 app-server 失败，未发生模型调用。
Claude/Gemini/OpenCode 只核对了文档，没有原生任务实跑。

在本机检查宿主版本与发现根目录。当前 Codex 文档列出仓库/用户 .agents/skills，RTA 安装器
保留 CODEX_HOME/skills 或 ~/.codex/skills。用明确的临时项目目标做有限烟测，不替换日用安装。
同时记录复制载荷身份和 fresh host 实际选中路径。先检查 Audit 只读，再在可用宿主上做 Plan
控制及一个有限授权 Operate 任务。

宿主无法暴露实际选择时，显式加载与 discovery 证据分开记录。只有核对现有 override/升级
行为和原生选择后，才判断是否应改安装器默认值。优先做小而兼容的修正，不重造宿主适配层；
分发建议也不自动产生迁移为插件的产品决定。

CWR 剩余用户边界是 Windows/OpenCode 对新 lifecycle/activity 字段的显示。Linux producer
与 status CLI 已用真实 acpx 验证。若本地已有适当环境与权限，观察多工具活动在 final 前的
状态字段及界面，保留遥测不可用的合法情况。不要改上游、全局宿主配置，或为消灭历史症状而
强行修改 legacy sequence 字段。

### 3. 检查更短的介入是否更值得使用

再运行模型前，先登记小型实验。选择普通工程容易漏掉 ownership/delivery 关系的任务，同时
保留局部普通修复和 clean/no-change 控制，包含所有者后续编辑及部分迁移。记录精确任务、
初始对象、模型/配置、实际 exposure、环境和判定方法；预期答案留在受试对象和 prompt 之外。

使用无 Skill 与当前候选两组；只有需要隔离版本效果时再加稳定 release 组。随机组别顺序，
做有限 fresh 重复，启动前确定最大调用数与可用预算。已有本地模型入口不自动授权新付费凭据
或服务；若需要未授权花费，先把精确可运行计划及上限准备好，再交最终批准。仓库 CI 与 fixture
self-test 不启动 live model。

测量独立任务成功、最终错误归因、实质无效改动、受保护输入违规、宿主实际 tool/token 计数及
接续返工，定义应在看到结果前确定。若测审阅成本，准备匿名审阅包与简单计时协议，请自愿的
所有者参与；活跃人工时间与 Agent 经过时间分开。报告长度不能换算分钟，未经授权不联系别人。
保留失败、setup block、未读 treatment 和未知计量。

值得比较的是现有渐进方法与更短的“先检查消费者”指令，在相同困难任务上是否有差别。
保留完整已接受产品结果；证据尚不支持独立产品时，不创建第二个长期 Skill。如果额外流程未
改善决策或修复，却增加审阅成本，应缩短或淘汰那部分。

### 4. 只在真实案例揭示缺口时改进

Viper 已补充 Go、动态配置和有意门控能力，冻结方法完成迁移检验，无需新增规则。
AutomaticEnv 默认限制、BindEnv/default-key 成功、experimental option 和快照假修复应
继续分开裁定，不能凭一个简单 struct 的成功就全局开启实验能力。

下一个外部例子应挑战不同边界，例如生成客户端的陈旧 export、实际安装应用选择的 workspace
包、读写端分阶段部署的迁移。看结果前写清它为什么能挑战当前方法。优先深入执行一个例子，
外部项目继续只读，修改仅在一次性探针对象。

精确输入/输出/状态 invariant 具有合同依据时可形式化。采纳、取代、人工步骤用途和判据
适用性继续作为可审查判断。避免行数目标、通用等级、无界图提取及每次普通改动的强制报告。

## 命令与验证范围

在 RTA 根目录执行：

```bash
python3 scripts/validate_repository.py
python3 scripts/validate_architecture.py
python3 -m unittest discover -s tests -p 'test_*.py'
python3 scripts/selftest.py
python3 evals/intent-lab/check_intent_subject.py
python3 evals/intent-lab/check_intent_subject.py --self-challenge-repairs
python3 scripts/compare_trials.py evals/experiments/2026-11-user-outcomes/observations.json
git diff --check
```

定位本机 skill-creator/scripts/quick_validate.py 并对
skills/repository-operational-truth-audit 运行，不假定固定机器路径。完整仓库套件包含
operation-lab 行为和安装检查。Field probe 有明确依赖准备，单独可选调用。Field Lab v2
使用显式离线迁移到新实验目录，再 validate/selftest；保留原 v1 manifest 和迁移回执，目标
模型调用数为零。

这些检查不证明真实数据迁移、用户环境安装、原生 Windows 支持、宿主自动发现或模型因果优势。
记录精确新鲜观察，历史发布 CI 保持历史身份。

## 必须交回的成果

交付已实施修改和清楚判断：

- 精确研发 branch/commit、变化的职责、当前消费者、前后观察，保留无关改动和恢复信息。
- 实际命令与结果、独立反例、合法相邻用途；注明判据适用性修正。
- 匹配试验回执，缺失计量显式保留；只有真测到才报告 owner 审阅收益。普通工作同样完成时如实说明。
- 配对中英文公共合同与状态更新；原始私人证据在 Git 外，权威 Skill 保持唯一可安装来源。
- 有限下一决策；若缺环境或 owner，明确是哪一个。

在既有源码研发授权和可用权限下保存并推送研发分支；环境阻止 remote write 时保留本地成果，
说明具体阻塞。未经所有者独立决定，不合并、不移动稳定 tag、不发 release、不升级日用 Skill。
若之后提出 release，应先形成可审阅 diff、验证载荷、发布说明及明确安装/discovery 计划。
