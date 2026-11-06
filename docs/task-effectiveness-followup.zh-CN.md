# 具体任务有效性后续 — 2026-11-07

[English](task-effectiveness-followup.md)

状态：**未发布的 main 源码与受控观察；没有日用安装或 release**。

Main 现在允许具体产品任务的有效性问题独立构成 Audit 决策，不要求先证明历史违约。
当前任务局限、已采纳承诺与改进提案分别举证。既有三模式、九文件载荷与写权限边界保留。

## Lumen：拒绝空白的交付简报

旧 evaluator 接受了正文为空的 Markdown 发布物；正常与还原运行包含原观察。新增回归先
得到 RED：空白、固定第一条内容和两条混合内容均未被拒绝。修正后，通过所选入口发布
两条不同观察，每份成品必须绑定自身内容且不混入另一条；第一条发布后第二条草稿仍保留。
正文正确且带合法 Markdown 包装的输出仍被接受。

这保护合成案例的发布合同，本身不证明通用自然语言忠实性或模型表现改善。

## Cedar：两种当前用途的匹配对照

两个新样本的应用、launcher、manifest、数据、worksheet、README、原 programme 和摘要
测试逐字相同，只有当前用途笔记和请求不同。一项任务要求从导出 packet 定位来源修订
影响，另一项只要求晨会读摘要、保留专家复核。原 programme 接受摘要交接，未承诺修订定位。

本地 store 保存 source/revision 关系，但正常 export 丢弃它，独立 worksheet 补足修订
任务；同样的投影仍足以服务摘要用途。样本、truth/candidate 检查留在现有
[intent lab](../evals/README.md)，没有另建评测引擎。

四个 fresh native session 均请求 `gpt-6.1-sol`、high reasoning，不继承主会话历史。每次
只提供一个样本仓库、该任务的相同范围请求、显式 Skill 路径与专属探针目录，不提供
evaluator notes、隐藏输入或已知修复。两个修订任务 session 随后各在相同有限实施请求下续做。

| 任务 | 公开载荷 baseline | main 载荷 candidate |
| --- | --- | --- |
| 修订任务 Audit | 找到导出交接损失、worksheet 补救，保留专家判断，不虚构旧承诺 | 相同且有证据的结论 |
| 摘要任务 Audit | 在既定用途内 clean，不强加修订定位 | 相同且有证据的结论 |
| 获授权修订实现 | 正常导出变为自足 packet，通过独立 source/artifact 见证 | 相同且有证据的结果 |

协调者完整阅读四份审查成品、检查两份真实修复 diff，并对两者运行独立 candidate checker。
隐藏记录在摘要不变时交换引用关系；判据从所选 CLI 导出，移走输入 store，再只凭 packet
检查摘要与完整原论证 records：source 和 revision 同时匹配、多条/零命中、重复引用、顺序
及状态不变；同时按声明重建 artifact。另有不同 packet 布局的正控，以及空白、常量、局部、
混入、忽略版本和修改状态的负控。两份修复中的历史 programme/use/data 原件不变；两份
摘要目标只有获准新增的报告。

这些观察支持所选合成任务上的兼容与完成，**没有证明相对 baseline 的新增优势**。保留
源码细化，是为了明确任务与承诺的区别，不宣传为实测准确率提升。每个审查条件只有一次，
没有随机顺序或真实用户，也未独立测量 token、费用、提问负担或长期维护收益。显式选择
Skill 不等于宿主自动发现；读取指令属于目标自报，没有独立完整 trace。宿主还提供共同
工程规则；记录的是 native 模型选择，没有额外 provider attestation。

## 身份与检查

以声明的九文件 payload digest 标识对照中的方法字节：

- Baseline，来自 source `3d096ade61c8abc4c3a1bab3575f30c4023075b5`：
  `02126bada7a880693ea55e73b9bd9404829c2f9b99ca2357b462506e900f492a`。
- Candidate/当前 source：
  `636ed87aa88b67f358850de36beae904f799b1f9c06ceb06481fe28222043d1a`。

最终声明载荷与实际参与对照的 candidate 一致。这只证明 source 身份，不证明安装或激活。
原始报告和本地运行产物保持私有，不在这里发布私人讨论或目标导出原件。

Fresh 检查通过：**128 个 repository tests**、repository/architecture/Skill validation、
六项原 fixture self-tests、十三项 intent truth 和十三项破坏反例。两份真实模型修复均通过
`check_intent_subject.py --verify-operate task-export-handoff --candidate PATH`。确定性命令
不调用模型。双语 SVG 文案经过结构检查，并在本地缩略图检查了变更文字；不称为新的完整布局验收。

本机 Field Lab v2 拒绝仓库中 legacy-v1 的 `fieldlab-pack.json`：可选 validate 与 selftest
均在离线检查开始前退出 2。因此这两项**在该 companion 版本下未验证**。没有迁移、安装
旧 companion 或额外模型调用；上面的独立 RTA 检查不依赖 Field Lab。
