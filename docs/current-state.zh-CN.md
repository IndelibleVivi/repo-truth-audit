# Current state

[English](current-state.md)

最后核对：2026-09-20

## 产品与源码

Repo Truth Audit 保持一个独立 Skill，具有 Audit / Plan / Operate 三种模式。调用 slug
与 canonical path `skills/repository-operational-truth-audit/` 均未改变。Audit 保持只读，
Plan 在编辑前停止，Operate 将显式、有限的结构改造推进到适用的证据边界。

Source `0.2.1` **已发布为 v0.2.1**，截至 2026-09-20 为最新公开 release。这些细化在已合并的
[PR #5](https://github.com/IndelibleVivi/repo-truth-audit/pull/5) 中基于公开基线
`e70642fff3c09476b5a81cebde0f16c5cdb4cc16` 开发。文档安装引用固定到已核验的公开 tag，
详见[发布说明](releases/v0.2.1.zh-CN.md)。

本版细化辅助方法的适用范围、与风险相称的 witness、获授权 dirty 实现退役、长期验证设施
成本，以及受到质疑时基于证据重新判断。没有新增执行引擎、安装载荷文件、模式、覆盖率配额
或逐项测试审批。`scripts/common.py::SKILL_PAYLOAD_FILES` 的八文件定义未改；runtime bytes
已经变化，其 digest 与有限 forward 证据固定在 [0.2.1 回执](forward-0.2.1-receipt.zh-CN.md)。

Renderer-neutral 架构模型仍具有权威性，保持七个 region、31 个 stable nodes 与 46 条边。
这些细化在既有 authority、witness、increment 和 acceptance 节点内部生效，没有提议变更
拓扑或 SVG 布局。可选 byte checker 仍只证明命名 bytes，不证明语义正确、授权、隔离或启用。

## 行为证据

在既有 operation lab 下加入六个合成对照对象及六项夹具/反例测试，覆盖可选及项目强制的
test-first、被输出检查掩盖的真实重复写入、所选产物退役、获授权 dirty 清理和只读对照。
准备脚本创建新的合成 Git 仓库，只暴露目标文件和请求；评审要求与已知改法留在其输入之外。

受审 runtime head `aa84cd0c7cf84caae9055b90623f03f74bea4d10` 通过
[PR CI run 35498436856](https://github.com/IndelibleVivi/repo-truth-audit/actions/runs/35498436856)
的 Ubuntu/macOS 与 Python 3.10/3.13 四项 jobs。本地验收独立通过仓库／架构验证、91 项
单元测试、六项 fixture self-tests 与 Skill validation。可选 Field Lab pack 转入一次性 v2
manifest，未修改 source；验证及六项 expected-overlay self-tests 通过，目标模型调用为零。
后续文档 commit 仍使用自身 PR checks；此 CI 链接只固定到受审 runtime head。

**有限合成 forward 验收已通过：**九个独立 native 会话及两次只读续问，分别接受独立的
diff/source/bundle/ledger 检查。[回执](forward-0.2.1-receipt.zh-CN.md) 记录身份、实际 helper
暴露、强制 test-first 顺序、dirty before-image 保留、只读对象不变，以及完整／不完整结果
得到不同质疑结论。两版在二乘二 helper 对照中都通过，不能证明新版更优，也未独立验证没有
字面冲突时的方法选择。普通验证仍不调用网络或目标模型。

[Issue #4](https://github.com/IndelibleVivi/repo-truth-audit/issues/4) 及维护者的澄清构成本轮
改进动机，不能证明 RTA 或 TDD 导致清理失败。本版没有修改报告者的项目，也不推断有用测试
应当删除。

## 发布与安装状态

已发布的 [v0.2.0 release](releases/v0.2.0.zh-CN.md)、
[发布记录](release-preparation.zh-CN.md) 和
[0.2.0 forward 回执](forward-0.2.0-receipt.zh-CN.md) 保持原有精确历史声明。该 annotated tag
peel 到 `5d25c581a7d331329d39be9f6bace11371dd4437`。已记录的 0.2.0 安装、发现与 payload
digest 只属于那些历史 bytes，不能充当 0.2.1 安装证据。

已发布的 [v0.2.1 Release](https://github.com/IndelibleVivi/repo-truth-audit/releases/tag/v0.2.1)
经 read-back 确认为 latest、非 draft、非 prerelease。Annotated tag peel 到
`6485296b39b7fc8526713cda5e8df01c679a4ec6`；release commit 的
[四项 CI jobs 全通过](https://github.com/IndelibleVivi/repo-truth-audit/actions/runs/35503842279)。
公开 README／许可路径可读；从该 tag 安装到临时目录后，八文件集合和已验收 payload digest
完全一致。独立的临时替换安装保留了 v0.2.0 备份及无关文件。

本次发布没有升级日用 Skill 副本，也没有验证 fresh host discovery；安装与宿主运行仍是
独立观察。发布后的 main 状态更新不移动 release tag，也不修改 Skill payload。

功能材料继续按 SUL-1.0 提供 source-available 许可。独立公开文档和图示依照
[LICENSING.zh-CN.md](../LICENSING.zh-CN.md) 使用 CC BY-NC-SA 4.0。
没有内置外部 Skill 文本或代码；新对象中的可选 test-first policy 是原创合成评测材料。
