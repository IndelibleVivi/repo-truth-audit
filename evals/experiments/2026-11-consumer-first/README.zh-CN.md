# Consumer-first 指令实验——2026 年 11 月

[English](README.md)

这是一个预注册、离线运行的实验包。它准备四个配对任务，最多安排十二次 fresh
单重复会话，并评估这些会话实际产生的产物。工具不启动模型，也不选择宿主；协调者在
第一次目标 Agent 调用前冻结此包并选定 harness。

原预注册及 `execution-settings.json` 保留中止的 `03e3706` 首批身份。修正批请查看独立的
[setup 修正](setup-recovery.zh-CN.md)、[修正批预注册](recovery-preregistration.json)
及修正批设置；[最后四次登记](final-four-preregistration.json) 记录最终权限修正。各批分别报告。

## 问题与状态

较短的 consumer-first 指令，能否在当前 progressive Skill 快照之外，保持独立验证的
任务成功、归因、ownership 和受保护输入，同时减少原生工具或 token 成本？三个组：

| 组 | 暴露 |
| --- | --- |
| `without-skill` | 仅任务与对象；无 RTA 载荷或实验指令 |
| `progressive-rta` | 下方精确九文件 RTA 载荷，加 `instructions/progressive-rta.md` |
| `consumer-first` | `instructions/consumer-first.md` 的短指令；无 RTA 载荷 |

原十二个槽位严格是四任务 × 三组 × 一次重复。本次接续已关闭，在三批中共
**启动 24 个被试会话**。前两批因 setup／harness 缺陷停止；最后四次得到一组完成的
普通修复配对，以及两个缺少必需报告的已验证 migration 检查点。见
[结果与限制](results.zh-CN.md)：平衡研究仍未完成，也不证明生产率优势。
冻结登记保留历史身份，继续调用须有新的预注册与预算。

## 冻结身份

处理快照是本仓库声明的九文件 Skill 载荷。身份由
`scripts/common.py::SKILL_PAYLOAD_FILES` 计算并写入 `preregistration.json`。
当前源 payload digest 为
`28b73009402e0f149c7078379a15d51cf88468c66ec092f49a59a5f6926fb211`。
身份包括声明文件的可执行位与字节，不采用 installed copy 或整目录哈希。在 fresh
会话中加载快照只检验显式处理，不检验宿主自动发现。

顺序 seed 为 `consumer-first-2026-11-14-v1`。槽位按 seed、task id、arm id 的
SHA-256 排序，完整顺序写在 `preregistration.json` 并由测试冻结。看到结果后不得替换槽位。

## 任务

| 任务 | 类型 | 对象与已接受结果 |
| --- | --- | --- |
| `migration-recovery` | 困难 ownership 接续 | 从具有误导 checkpoint 与后续 owner 编辑的半迁移继续。完成源码分工，使旧 writer 退出 CLI/bundle，保留行为与 owner 字节，并验证源码和新构建交付物。 |
| `delivery-adoption` | 困难选中消费者变更 | 修复 Cedar，使独立 packet 接收方能定位引用某修订来源的完整记录；保留摘要读取、专业判断、源输入与声明交付。 |
| `known-bug` | 普通局部控制 | 通过所选 CLI 与声明 bundle 修复小型合成 parser bug，并保留相邻有效输入。这不是 RTA 型任务。 |
| `clean-baseline` | clean/no-change 控制 | 按已接受本地行为审计一个一致的小 CLI，报告无需改动，并保持所有输入字节不变。 |

英文任务在 `tasks/en/`，中文 Task 在 `tasks/zh-CN/`。EN/ZH 是同一任务身份的
配对版本，不支持翻译效果。匹配 block 内须使用同一语言；若语言本身是变量，须将其
预注册为独立分层因素，不能在同一比较中随意混用。

## 预注册判定

以下判定在结果前固定：

- **独立成功：** 在一次性副本中通过全部任务验收，包括所选入口、行为、声明交付和
  受保护输入。Agent 的 `RESULT.md` 或自述不足以判定成功。
- **错误归因：** 最终可见诊断中的机制或生命周期事实，被 evaluator 的当前源码/状态
  观察否定。含糊结论、已披露的 setup 限制，或先错后自行更正不等于必然错误归因；
  须记录区分。
- **实质无效改动：** 超出授权语义结果并改变行为、交付、持久状态或声明 ownership
  的修改，或缺少任务必需修改。仅格式噪声计入额外改动证据，但不单独判失败。
- **受保护输入违规：** prompt 标明的路径发生字节变化，包括 evaluator seed、提供的
  decision/spec、owner note 或 clean-control 产品字节。仅声称保留不算，须比字节。
- **原生工具/token 计数：** 只记录实际宿主暴露的计数。tool calls、executor
  commands、nested calls、input/output tokens 分别保留。能在比较器现有 metric
  中记录时不得混算别名；缺失值为 `unavailable` + null，绝不变成零。
- **接续返工：** `migration-recovery` 从首次返回产物到达到接受结果所需的 owner/
  reviewer 工作，计时时记秒，否则 null。工具重试与 Agent 中间错误不属于人工返工，
  除非确有人执行。
- **Setup block：** 依赖、compiler、fixture 准备、权限或 harness 启动在任务可运行前
  失败。结果记 `blocked`，证书记录具体失败边界，不计任务失败或模型效应。
- **Unread treatment：** treatment 可获得，但宿主没有证明其已读。运行保留为
  `available-unread`；按回执规则双 treatment 比较不成立。不得在看到结果后把标签改成
  `loaded`。

失败、阻塞和未判定会话留在回执与分母中。看到结果后不得剔除。

## 人工审阅协议

审阅完全自愿。不得从本包招募、联系或识别审阅者，也不得虚构审阅。愿意参加的
owner/reviewer 只拿到匿名 packet：run id 替换为不透明 review id，隐去 arm 标签和
treatment 文本，并把任务 prompt、回执与预期答案分开。仅记录审阅者自行操作的 active
review stopwatch 时间。

该主动时间写为 `human_active_seconds`；Agent 的 `elapsed_seconds` 从 harness
单独取得。不得由报告长度、token、工具数或墙钟重叠推算人工分钟。审阅者身份、账号数据、
私人笔记和原始时间戳不得进入 tracked files。若没有自愿审阅，全部人工字段保持
`unavailable`。

## 准备、运行与评分

协调者选择 harness 并运行模型；本包不会运行。只向不存在的新路径准备对象：

```bash
python3 evals/experiments/2026-11-consumer-first/prepare_trial.py \
  migration-recovery /path/to/new-subject
```

命令输出任务身份、prompt/subject digests、protected paths 和冻结的
目标模型调用数（`0`）。destination 的词法或解析路径若与 source、subject、
helper 或 protected fixture 重叠，会被拒绝。

使用 `tasks/en/` 或 `tasks/zh-CN/` 的 prompt；预期答案留在本包内。Operate 任务
要求 `RESULT.md` 和对象外的计量记录；`clean-baseline` 只允许对象内新增
`INTENT-AUDIT.md`。

独立评分实际返回产物：

```bash
python3 evals/experiments/2026-11-consumer-first/verify_trial.py \
  migration-recovery /path/to/returned-subject \
  --artifact /path/to/returned.zip --output /path/to/evidence.json
```

输出路径不能覆盖 candidate、evaluator fixture 或提供 artifact。加
`--negative-control` 可确认每个 verifier 会拒绝设计的已知坏产物；相邻有效控制会
自动执行。

生成匿名审阅包不应成为强制证据：

```bash
python3 evals/experiments/2026-11-consumer-first/prepare_review.py \
  --subject migration-recovery --arm progressive-rta --result /path/to/RESULT.md \
  --output /path/to/review-packet.json
```

完成回执交给现有 comparator：

```bash
python3 scripts/compare_trials.py /path/to/completed-receipt.json \
  --baseline without-skill --candidate consumer-first --json
```

comparator 归其他 lane 所有。`progressive-rta` 与 `consumer-first` 另作双处理调用。
不得在此修改比较语义，或暗中改为不支持的 three-arm schema。

调用单位是 fresh Agent 被试会话，不是会话 tool loop 内单次 API 请求。
原批执行设置冻结于 `execution-settings.json`：最多十二会话、每次 180 秒、三并发、
不重试、不启用新付费凭据。host usage 不等于人工活跃时间。中文对象的 prepare 与 verify
都应传 `--language zh-CN`；同一匹配 block 保持一种语言。可选审阅导出器只对报告草稿
隐去已知组名；自愿审阅前仍须人工检查路径、姓名等其他身份线索。

## 限制

Fixture 是在一次性副本中运行的可信合成代码；不构成恶意代码隔离或网络限制。困难任务
是有意选取，不代表总体分布。Cedar 是已知研究对象，模型可能熟悉。payload identity
只证明声明字节，不证明发现或实际阅读。精确后端模型和原生计数取决于 harness。
十二槽位只支持描述性配对证据。
