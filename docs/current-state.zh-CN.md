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

Source 实现与有限验收已完成：110 个 repository tests、repository／architecture／Skill
validation、六项原有 fixture self-tests、operation lab、八项意图 ground-truth 检查和八项
破坏反例通过。可选 Field Lab 离线 validation 与六项 self-tests 也通过，target-model
invocation 为 0。

两个独立 target session 使用固定 candidate，完成五个意图 Audit，以及分阶段 Plan / Operate
search 修复。协调者复核只读边界、受保护证据与修复后的 source／声明产物。
[0.3.0 forward 回执](forward-0.3.0-receipt.zh-CN.md)记录精确身份、evaluator 修正及限制：
每条件一次、没有旧版对照，独立发现的账号内容缺陷明确留在有限 search 修复范围之外。
不据此证明任意仓库效果。

临时安装与 forward 使用的九文件 payload 精确一致，两种语言 SVG 均已渲染并目视检查。
Candidate 已达到 source 交付状态；日用安装、release 与隐式发现仍属独立层。

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
