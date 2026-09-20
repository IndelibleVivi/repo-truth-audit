# Current state

[English](current-state.md)

最后核对：2026-09-20

## 产品与源码

Repo Truth Audit 保持一个独立 Skill，具有 Audit / Plan / Operate 三种模式。调用 slug
与 canonical path `skills/repository-operational-truth-audit/` 均未改变。Audit 保持只读，
Plan 在编辑前停止，Operate 将显式、有限的结构改造推进到适用的证据边界。

Source `0.2.1` 是**未发布候选版**，在
[PR #5](https://github.com/IndelibleVivi/repo-truth-audit/pull/5) 中基于公开基线
`e70642fff3c09476b5a81cebde0f16c5cdb4cc16` 开发。最新公开 release 保持 `v0.2.0`，
稳定安装仍固定到该版本。这里不声称候选版已经日常安装、合并、打 tag 或发布。

候选版细化辅助方法的适用范围、与风险相称的 witness、获授权 dirty 实现退役、长期验证设施
成本，以及受到质疑时基于证据重新判断。没有新增执行引擎、安装载荷文件、模式、覆盖率配额
或逐项测试审批。`scripts/common.py::SKILL_PAYLOAD_FILES` 的八文件定义未改；runtime bytes
已经变化，需要新 digest 和新 forward 证据。

Renderer-neutral 架构模型仍具有权威性，保持七个 region、31 个 stable nodes 与 46 条边。
这些细化在既有 authority、witness、increment 和 acceptance 节点内部生效，没有提议变更
拓扑或 SVG 布局。可选 byte checker 仍只证明命名 bytes，不证明语义正确、授权、隔离或启用。

## 候选版证据

在既有 operation lab 下加入六个合成对照对象及六项夹具/反例测试，覆盖可选及项目强制的
test-first、被输出检查掩盖的真实重复写入、所选产物退役、获授权 dirty 清理和只读对照。
准备脚本创建新的合成 Git 仓库，只暴露目标文件和请求；评审要求与已知改法留在其输入之外。

初始 runtime/fixture commit `8b5d83fcf0d0c2de3023cd9de85f4ab214eed74a` 通过了
[CI run 35497731111](https://github.com/IndelibleVivi/repo-truth-audit/actions/runs/35497731111)：
Ubuntu/macOS 与 Python 3.10/3.13 共四个 jobs 的架构、仓库、单元和 self-test 命令全部通过。
六项新夹具测试也在独立 Linux 工作环境中通过。后续文档/版本变更仍须核对自身的当前 PR
checks；这份固定结果不为后来的 bytes 背书。

**0.2.1 尚未执行目标模型 forward run。** 对象准备、夹具测试和仓库 CI 无法证明代理实际如何
选择方法或回应质疑。[评测协议](../evals/README.md) 说明如何在基线和候选版之间控制条件，
记录实际 helper 暴露、受保护的输入快照、真实 diff 和行为/产物检查。普通验证不调用网络或
目标模型。

[Issue #4](https://github.com/IndelibleVivi/repo-truth-audit/issues/4) 及维护者的澄清构成本轮
改进动机，不能证明 RTA 或 TDD 导致清理失败。候选版没有修改报告者的项目，也不推断有用测试
应当删除。

## 稳定版与后续 gates

已发布的 [v0.2.0 release](releases/v0.2.0.zh-CN.md)、
[发布记录](release-preparation.zh-CN.md) 和
[0.2.0 forward 回执](forward-0.2.0-receipt.zh-CN.md) 保持原有精确历史声明。该 annotated tag
peel 到 `5d25c581a7d331329d39be9f6bace11371dd4437`。已记录的 0.2.0 安装、发现与 payload
digest 只属于那些历史 bytes，不能充当当前候选版安装证据。

推进前需审查最终 diff 与精确 head 的检查结果，在声明的合成边界内完成独立 forward 对照，
并记录候选 payload identity。安装、fresh host discovery、合并与发布仍是由所有者授权的
独立 gate。Draft PR 不等于已发布或已通过模型行为验证的产品。

功能材料继续按 SUL-1.0 提供 source-available 许可。独立公开文档和图示依照
[LICENSING.zh-CN.md](../LICENSING.zh-CN.md) 使用 CC BY-NC-SA 4.0。
没有内置外部 Skill 文本或代码；新对象中的可选 test-first policy 是原创合成评测材料。
