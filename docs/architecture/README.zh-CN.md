# Audit / Plan / Operate 运行架构

[English](README.md)

本目录拥有公开 Repo Truth Audit 架构背后的 semantic contract。两份本地化图直接以原生
Mermaid block 存在于根 README 中，解释一场 evidence-led engagement 如何在 Audit 或 Plan
停止，或跨过显式实施 gate，最终抵达经过验证的 Operate completion。它们不描述本 repo
自身的 packaging 或 release pipeline。

## Reader question

> Repo Truth Audit 如何把精确仓库快照与明确所有者意图转化为有界只读答案、可执行计划，
> 或经过验证完成的获授权结构变更，同时不夸大证据或外部状态？

图通过七个 region 回答：

1. 钉住所有者意图、请求终点与仓库 identity；
2. 解析当前 authority 与 reachability；
3. 穿行彼此分离的 evidence layer；
4. 挑战并裁定实质候选；
5. 在不修改目标的情况下闭合 Audit 或 Plan；
6. 获得显式授权后，建立 protected witnesses，并从 coherent increment 经过 checkpoint/
   recovery loop 抵达 whole-goal acceptance；
7. 把 external state 留在显式 fresh-observation gate 之外。

## Truth surfaces

| Surface | Authority |
| --- | --- |
| [`audit-runtime-model.json`](audit-runtime-model.json) | Renderer-neutral semantic authority：reader question、boundaries、stable IDs、nodes、edges、states、source mapping 与 render acceptance |
| [`../../README.md`](../../README.md) | 独立英文 Mermaid view |
| [`../../README.zh-CN.md`](../../README.zh-CN.md) | 独立简体中文 Mermaid view |
| [`../../scripts/validate_architecture.py`](../../scripts/validate_architecture.py) | Model、source-anchor、topology、localization、connector-kind 与 README parity validation |

JSON model 拥有 meaning；每份 README 拥有自身 locale 的精简 display copy 与 Mermaid syntax。
两图共享 region、node 与 semantic-edge IDs，每条 modeled edge 都在两图中可见。

每个内部 node 都映射到当前 repository authority：

- [`../product-spec.zh-CN.md`](../product-spec.zh-CN.md) 拥有 Audit / Plan / Operate behavior、
  effect authority、acceptance 与 terminal results；
- [`../evidence-model.zh-CN.md`](../evidence-model.zh-CN.md) 拥有 proof、adjudication、
  checkpoint、completion、recovery 与 stopping semantics；
- [`../../skills/repository-operational-truth-audit/`](../../skills/repository-operational-truth-audit/)
  拥有 runtime router 与 progressive Audit、Operation、Recovery methods；
- [`../../AGENTS.md`](../../AGENTS.md) 拥有 canonical source、write、install、privacy 与
  publication boundaries。

External-state node 保持 `unobserved_by_default`。Repository evidence 不会静默证明 runtime、
edge、device、account 或 owner acceptance。

## Connector meanings

Mermaid view 只使用三种无需依赖颜色也可分辨的 connector：

- 实线：范围内 evidence 或 implementation flow；
- 点线：有条件的 authority、specialist 或 fresh external observation；
- 粗回线：新证据重新打开诊断或下一 increment。

证据通过不会自动把 claim 升级到下一 proof layer。只要适用的 Behavior、Structure、Delivery
或 Usefulness obligation 仍未完成，verified checkpoint 就不会变成 whole-goal completion。

## Localization 与 theme contract

英文与简体中文是两张独立 Mermaid 图，不在同一 canvas 混排双语。它们保持 region、node、
semantic-edge 与 connector-kind parity，同时允许 locale-specific line break。

两图使用 Mermaid renderer defaults，不硬编码 theme colors，让 GitHub 自行适配 day/dark surface。

## 编辑与验证

先在 `audit-runtime-model.json` 改 meaning，再在同一个 change 中更新两份 README Mermaid：

```bash
python3 scripts/validate_architecture.py
python3 scripts/validate_repository.py
python3 -m unittest tests.test_architecture
```

Validator 要求七个 region、全部 stable nodes、全部 46 条 semantic edges、精确 connector kinds
与 localized edge labels、model source anchors、locale parity、top-to-bottom flow，以及可见的
只读诊断边界、显式 Operate gate、checkpoint/recovery feedback、whole-goal acceptance 与
external proof boundary。

Immutable `v0.1.0` release 仍作为早期 audit-only architecture 的历史证据。当前 `main`
使用扩展后的 README Mermaid view，服务尚未发布的 0.2.0 source candidate。
