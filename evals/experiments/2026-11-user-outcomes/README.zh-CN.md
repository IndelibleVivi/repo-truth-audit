# 四组配对工程任务——2026 年 11 月

[English](README.md)

本目录是可离线复现的实验，不启动模型，也不进入安装 Skill。真实机制与产品决策见
[研究报告](../../../docs/user-outcomes-study.zh-CN.md)。

## 已观察结果

八个 fresh native Agent 完成四组任务；每组两边都通过独立验收，未观察到成功率增益。
自报执行命令数在 mitt 相同，其余三组候选更多。本轮不能计算时间、token、金钱或人工生产力提升。

| 任务 | 无 Skill 结果 | 候选结果 | 执行命令：无 Skill / 候选 | 含编排工具：无 Skill / 候选 |
| --- | --- | --- | --- | --- |
| mitt 类型化取消订阅 | 成功 | 成功 | 15 / 15 | 24 / 25 |
| Cedar 修订数据包修复 | 成功 | 成功 | 6 / 13 | 14 / 22 |
| 纯摘要只读审计 | 成功 | 成功 | 8 / 10 | 14 / 16 |
| 部分存储迁移接续 | 成功 | 成功 | 6 / 10 | 14 / 21 |

这些计数来自各 Agent 的计量报告，标为 **proxy**。执行次数指 exec_command，不代表 shell
语句或所有子进程；含编排计数同时包含 wrapper 与 nested calls，不能当成独立工作单位。
比较器保留它们而不计算 measured delta。精确后端模型、token、可归因经过时间、所有者
审阅时间与人工活跃时间均未暴露或记录。

最终可见诊断已独立阅读，在该范围未发现错误归因；没有完整隐藏推理或所有文件效果的认证记录。
无效改动数量保持未知，最终 diff 做了定性审查，没有看完结果后发明计数口径。两份摘要报告
保留产品字节和合法专业判断，长度为 2,703 与 2,950 Unicode 字符；长度不代表审阅耗时。

保留两项中间失败：mitt control 首次编译 CommonJS runner 缺 esModuleInterop，之后修正；
resume candidate 一次编排语法错误未进入 nested tool。未因此剔除任务。受试环境缺 mitt
完整开发依赖，未运行其完整 lint/Mocha；独立检查了真实编译器、无效类型、生成声明和 package 运行时。

## 身份、处理与限制

RTA 起点为 `9fd099b6c9e88be2d7c809b021add51a5c8d6b8f`，冻结候选 digest：
`28b73009402e0f149c7078379a15d51cf88468c66ec092f49a59a5f6926fb211`。
两边使用同一 Linux workspace、Python 3.12.14、Node 24.22.1；mitt 用 TypeScript 4.9.5。
Native Agent 以 fork_turns=none 启动，继承会话模型/设置，无显式模型 override。
匹配配置记录不证明精确后端模型身份。

每位 Agent 只得到自己的任务和目录；候选另得冻结 Skill 并被明确要求读取，控制组无 RTA
载荷。共享的通用模型知识无法移除。允许检查和修改获授权对象，禁止读取其他 trial、判据及答案，
禁止网络、委派、联系上游、发布和全局安装。目录限制是共享文件系统上的指令约束，不构成 OS 沙箱。

四对案例为有意选取、未随机排序，每任务每组一次，没有稳定 release 组。它们是不同任务的
观察，不能作为同一处理效果的八次独立估计。真实历史 mitt 问题可能已为模型所知。显式读取
不检验自动发现。本地 Codex CLI 在模型调用前初始化失败；这些运行来自 native research agents。

[observations.json](observations.json) 包含输入身份、exposure、独立结果、计量来源和未知值。
其中 evidence locator 相对于另行交付的研究证据包，不是比较器必需的本地文件。原报告、补丁
和逐次结果在 Git 树外。Cedar/summary 初始身份由原始 Git tree 重建并与生成器核对；resume
匹配两份运行前回执；mitt 匹配保留的原始模板。这些是注明来源的核对，不冒充时间戳认证。

## 任务输入

| 案例 | 用户任务 | 独立判定边界 |
| --- | --- | --- |
| mitt | 使所附类型化应用停止通配订阅，继续命名订阅；修复进入实际本地 package | 独立编译器、错误类型控制、运行序列及源码重生成声明 |
| cedar | 导出来源/修订复核所需完整记录，保留输入、顺序、摘要读取及人工判断 | 源码和声明产物的 fresh 接收方，只收到包；删除生产者；交错历史 |
| summary | 判断已接受摘要晨会用途，不引入修订复核要求，仅写审计报告 | 原产品字节、独立读包，再单独审读报告语义 |
| resume | 完成已授权职责拆分，旧实现退出 CLI/bundle，保留输出、错误、状态效果和后续 owner 编辑 | 源码、新组装产物和实际交付 ZIP；所选 ownership 与错误顺序 |

在 RTA 根目录准备全新合成对象，目标目录必须不存在。工具不调用模型，也不复制评价答案：

```bash
python3 evals/experiments/2026-11-user-outcomes/prepare_trial.py cedar /path/to/new-cedar
python3 evals/experiments/2026-11-user-outcomes/prepare_trial.py summary /path/to/new-summary
python3 evals/experiments/2026-11-user-outcomes/prepare_trial.py resume /path/to/new-resume
```

mitt 先按[实战说明](../../field/README.zh-CN.md) 准备固定源码与 package seed：

```bash
python3 evals/experiments/2026-11-user-outcomes/prepare_trial.py mitt /path/to/new-mitt \
  --mitt-source /path/to/mitt --consumer-seed /path/to/mitt-consumer
```

helper 写入四行类型化消费者输入，并从
`6b41670516ed8e8b738612f60491995470aa63b3` 重建精确源码，复制已准备依赖，不抓取网络。
任务和应用说明在 [mitt-task.md](mitt-task.md) 与 [mitt-consumer.md](mitt-consumer.md)。
这两份是英语实验输入；翻译会产生新 prompt identity，不再是同一个 trial。

分别准备两组，并在 fresh Agent 启动前比较返回 digest。控制组只见 TASK.md 和对象。候选组
用 scripts/common.py::copy_payload 复制精确九文件到单独可读位置，记录 digest，再加显式
读取指令。评价器和预期输出留在上下文外；两边权限和任务一致，不能单给一边诊断或额外报告负担。

修复任务请求 RESULT.md 与说明实际可得计数的计量报告；summary 只允许对象内 INTENT-AUDIT.md，
计量写在外部。以后应在宿主回执中保存完整 routing instruction；本轮记录 exposure 和任务身份，
未声称已导出完整宿主 transcript。

## 独立复验

工具在可信实验对象的一次性副本运行，不提供恶意代码隔离。mitt 的编译器来自 evaluator
不可变 seed，不使用受试者可以修改的编译器。

```bash
python3 evals/experiments/2026-11-user-outcomes/verify_trial.py mitt /path/to/mitt-result \
  --consumer-seed /path/to/immutable-consumer-seed --output /path/to/evidence/mitt.json
python3 evals/experiments/2026-11-user-outcomes/verify_trial.py cedar /path/to/cedar-result \
  --output /path/to/evidence/cedar.json
python3 evals/experiments/2026-11-user-outcomes/verify_trial.py summary /path/to/summary-result \
  --output /path/to/evidence/summary.json
python3 evals/experiments/2026-11-user-outcomes/verify_trial.py resume /path/to/resume-result \
  --artifact /path/to/the-agent-delivered.zip --output /path/to/evidence/resume.json
```

summary 命令只核对技术合同；须阅读报告判断采纳、范围及是否捏造义务。resume 的 artifact
参数有实际意义：评价器重新打出正确包，不证明 Agent 声称交付的 ZIP 正确。

resume control 合法保留的文件只有说明和 from runner import process。任务要求旧文件退出
所选 CLI 与 bundle，两者确已排除它，也没有旧实现或写入。原 operation lab 明确要求物理删除，
因而拒绝这份输出。verifier 分别输出 original_lab_structure 与 task_contract_structure，
保留拒绝，不改变旧 lab 自己的合同。扫描无关构建工具的 .open 也会越过当前生产 owner 问题。

四个负控制分别是未修 mitt、未修 Cedar、半迁移、summary 只读中修改产品，均被拒绝。
正例包括全部八份真实 Agent 产物和合法 forwarding shim。这个结果只支持本组 probe。

## 比较时不补造成本

```bash
python3 scripts/compare_trials.py evals/experiments/2026-11-user-outcomes/observations.json
python3 scripts/compare_trials.py evals/experiments/2026-11-user-outcomes/observations.json --json
```

每份回执含一个 arm/block、任务与对象 digest、harness/model/settings/environment 身份、
Skill exposure、独立结果和证据定位。计量分 observed、proxy、unavailable，最后一项要求 null。
缺组、失败、阻塞和条件不匹配均继续可见，只有匹配的成对 observed 值计算差值。标签本身不认证事实。

下一轮先登记小型任务集与相同预算，随机组别顺序、多次 fresh 重复、记录宿主实际计数，并单独
计时自愿参加的 owner 审阅。包含 clean/no-change 与后续编辑的接续任务。选样在结果前完成，
保留全部任务结果和 setup 失败。优先选 ownership/delivery 歧义确有方法需要的任务，同时保留
普通工作控制。额外报告和协调抵消结果收益时，应缩短或停用方法。普通测试不启动新模型实验。
