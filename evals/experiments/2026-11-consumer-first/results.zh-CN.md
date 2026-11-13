# Consumer-first 后续：结果与限制

[English](results.md)

观察日期：2026-11-14。本次有限接续已在 **启动 24 个被试会话** 后关闭。原四任务／三组
研究没有完成，也没有证明 RTA 或短指令抵偿了审阅／协调成本。有效的普通修复配对两边均
成功；最后两个 migration 组产生了 consumer 验证通过的交付检查点，但因缺少必需报告，
未能在 deadline 内完成完整 Task。

## 批次核算

| 批次 | 冻结源码／登记 | 启动数 | 裁定 |
| --- | --- | --- | --- |
| 原批 | `03e37060f5da720aa318d9021c03a73809fe5404`；原登记／设置 | 12 | 未接触结果的独立 review 发现三项 fixture/oracle 缺陷；全部结果保留 unjudged。Host 状态为 9 完成、1 timeout、2 中断。 |
| Setup 修正 v2 | `3df91f43fd9a4430070c816d8e21a4648f99e355`；修正批登记／设置 | 8 | 协调者公共 prompt 将 clean 任务只读范围误施加给实现任务。六个实现结果保留 unjudged；两个权限正确的 clean 控制也在必需报告前中断。四个预留槽位从未启动。 |
| 最后四次 | `27dfe50afad667c1ad917da95dc6da79a692be0c`；最后四次登记 | 4 | 明确写权限、无重试。普通修复为无 Skill／短指令配对；migration 为完整 RTA／短指令配对。 |

[Setup 修正记录](setup-recovery.zh-CN.md) 保留三项反例、矛盾的 harness 条款及此前
结果暴露。登记和设置是历史字节身份，不静默刷新为新源码。前两批不与最后四次混池，
也不转化成模型修复失败。v2 取消后两个残留 `running` 标签保留并另记核对：独立读取
PID／参数并终止所属进程，证明没有剩余 writer。全部被试进程已停止。

可移植回执保留每个实际启动槽位及实测／缺失计数：
[原十二次](aborted-observations.json)、[修正八次与四个未启动预留](recovery-observations.json)、
[最后普通配对](final-known-bug-observations.json)及
[最后 migration 配对](final-migration-recovery-observations.json)。原始输入、prompt、报告、
events、对象和 review 证据均留在 Git 外私有位置，公众无法独立检查这些原始记录；
公开回执记录 provenance 与筛选后的观察，不是经过认证的 transcript。

## 独立验收

| 任务／组 | Host | 留存产品 | 完整 Task 裁定 |
| --- | --- | --- | --- |
| 普通／短指令 | 完成 | 所选 source CLI、实际生成 ZIP、候选回归与准确 `RESULT.md` 均通过 | 成功 |
| 普通／无 Skill | 完成 | 相同义务均通过 | 成功 |
| Migration／短指令 | 180 秒 timeout | 源码、结构、实际 ZIP、受保护字节均通过；缺少 `RESULT.md` | 失败：deadline 内完整 Task 未完成，保留通过的检查点 |
| Migration／progressive RTA | 180 秒 timeout | 相同检查点通过；缺少 `RESULT.md` | 同样的 deadline 失败 |

普通任务先对每个实际 ZIP 运行独立接收方，之后才在一次性副本运行候选测试。ZIP 成员
匹配最终声明 bundle。正数升序、降序、单值通过；零、负数及非法输入保留错误行为。
两个候选回归脚本均通过。两份最终诊断均与实际缺陷一致，未发现被证据反驳的因果声明
或范围外语义修改。

Migration 对源码及交付代码验证 JSON／text 兼容、空输入、非法结构、bool 拒绝、错误
顺序和写入失败。所选 runner 与 storage 各自承担对应职责；旧 writer 从源码和 bundle
退役。两边均保留后续 owner note 和 CLI 字节。四次通过逐字节比较，**改变的登记受保护
路径均为零**；这不等于审计全部外部动作。新建一次性验证目录具有明确授权。

报告义务早于结果登记。缺少 `RESULT.md` 是已观察的 Task 义务未满足；失败依据是该事实，
不是单凭 timeout。产品 evaluator 通过不足以等于完整完成。两个 migration 都没有最终
诊断，最终错误归因及人工接续返工计量保持不可得。会话结束后没有替候选修产品或补报告。

## 暴露与原生计量

最后三个 treatment run 都有 completed `cat`，读取精确冻结路径、exit 0、输出非空。
progressive 组读取 Skill 和渐进 references；九文件快照可用不代表每个字节均被读取。
短指令 digest 为
`98bad017590772950116c4c4182fd8d135b5fe0de3bce93d66c11eed97796410`；
未改的九文件 RTA digest 为
`28b73009402e0f149c7078379a15d51cf88468c66ec092f49a59a5f6926fb211`。
无 Skill 组没有收到任一 treatment，也无显式读取；ambient RTA 精确路径在本次 invocation
被禁用。普通宿主 context 未被证明为空。这些是显式暴露试验，不是自动 discovery 试验。

| 最后运行 | Completed command items | Wall 秒 | Host input tokens | Host cached input | Host output tokens |
| --- | ---: | ---: | ---: | ---: | ---: |
| 普通／短指令 | 8 | 99.933 | 194907 | 160384 | 3076 |
| 普通／无 Skill | 8 | 110.645 | 227079 | 203264 | 2998 |
| Migration／短指令 | 14 | 180.069，截断 | 不可得 | 不可得 | 不可得 |
| Migration／progressive RTA | 16 | 180.059，截断 | 不可得 | 不可得 | 不可得 |

Command item 是 type 为 `command_execution` 的 `item.completed`，包括非零 exit；
不是 shell 子命令数、全部 tool calls 或人工分钟。Token 原样来自 `turn.completed` usage。
Cached 和 reasoning 字段另行保留、不相加；累计／缓存与计费语义未验证。两个 timeout
没有 completion event，因此 usage 为 null，不是零。请求模型为 `gpt-6.1-sol`、reasoning
`high`，经 macOS arm64 上 Codex CLI 0.159.1 执行；实际 backend 身份未暴露。
会话使用现有 native ChatGPT 登录，最多三个并发、每次 180 秒、无重试、无新付费凭据／
服务。一个 Agent 会话可包含多个内部 API 请求。此前三个原生宿主烟测属于独立证据组，
不在这 24 个被试会话内。

普通配对 command items 相同，短指令组报告的 input 较少、output 较多。单个有意选样
配对还受普通宿主 context、缓存、并发和此前 harness 修正影响，不支持因果效率结论。
两个 migration 计数止于未完成结果，少两条 command 不证明成功交付更便宜。比较器可以
匹配两个独立裁定的失败，但差值仅有这个有限含义。人工活跃时间、owner 审阅时间及接续
返工均未计时；未向任何人发送 review packet，不推断 owner 收益。回执计数不包含协调者
的 setup 修复／审查成本。

## 重现离线比较

```bash
python3 scripts/compare_trials.py \
  evals/experiments/2026-11-consumer-first/final-known-bug-observations.json \
  --baseline without-skill --candidate consumer-first
python3 scripts/compare_trials.py \
  evals/experiments/2026-11-consumer-first/final-migration-recovery-observations.json \
  --baseline progressive-rta --candidate consumer-first
```

命令只比较已存观察，模型调用为零。原平衡登记未完成：没有有效的最终 Cedar 配对、完成
的 clean-control block、已完成困难任务的优势，或计时的 owner review。Package／CI 及
fixture 检查不能补足这些证据。

## 判断

保留更强的 consumer／oracle 检查和原生宿主观察。Installer 默认值及 canonical Skill
保持不变；consumer-first 保留为实验指令，不成为第二个已安装 Skill。这些结果既不支持
继续扩张方法，也不支持以短指令替换它。

下一项价值研究需要新的登记、留出完整交付时间的困难任务配对、未接触结果的 harness
权限审查、有限重复；若问审阅成本，须真实测量 owner effort。这是下一研究决策，
不是自动续跑或追加调用授权。Windows/OpenCode UI 采用及其他 native host 仍需要对应
环境。本轮没有 release、移动稳定 tag、merge 或日用安装。
