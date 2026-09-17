# Audit / Plan / Operate 运行架构

[English](README.md)

本目录拥有公开 Repo Truth Audit 架构背后的 semantic 与 presentation contract。两份根 README
先嵌入对应 locale 的 reader-first SVG overview，再保留默认展开的原生 Mermaid 完整拓扑图。
两层视图共同解释一场 evidence-led engagement 如何在 Audit 或 Plan 停止，或跨过显式实施
gate，最终抵达经过验证的 Operate completion。它们不描述本 repo 自身的 packaging 或
release pipeline。

## Reader question

> Repo Truth Audit 如何把精确仓库快照与明确所有者意图转化为有界只读答案、可执行计划，
> 或经过验证完成的获授权结构变更，同时不夸大证据或外部状态？

Reader overview 把答案压缩为所有者问题、被钉住的运行现实、停止边界、三种 mode outcome、
Operate 验收、checkpoint／completion 分流与外部证明边界。完整 Mermaid 图保留七个 region：

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
| [`repo-truth-audit-overview.en.svg`](repo-truth-audit-overview.en.svg) 与 [`repo-truth-audit-overview.zh-CN.svg`](repo-truth-audit-overview.zh-CN.svg) | 成对的 day-first reader map：有意压缩的 presentation，不是第二份 semantic authority |
| [`../../README.md`](../../README.md) | English overview embed、B/S/D/U 人话图例与完整 Mermaid view |
| [`../../README.zh-CN.md`](../../README.zh-CN.md) | 简体中文 overview embed、B/S/D/U 人话图例与完整 Mermaid view |
| [`../../scripts/validate_architecture.py`](../../scripts/validate_architecture.py) | Model、source-anchor、完整 Mermaid topology、connector-kind、SVG accessibility/safety、embed order 与 locale parity validation |

JSON model 拥有 meaning。SVG pair 是受维护的 editorial projection：可以压缩常规 topology，
但不能改变 mode、gate、proof boundary 或 completion claim。每份 README 拥有自身 locale 的
精简 prose 与 Mermaid syntax；完整图共享 region、node 与 semantic-edge IDs，每条 modeled edge
都在两份 Mermaid 中可见。

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

## 完整图的 connector meanings

Mermaid view 只使用三种无需依赖颜色也可分辨的 connector：

- 实线：范围内 evidence 或 implementation flow；
- 点线：有条件的 authority、specialist 或 fresh external observation；
- 粗回线：新证据重新打开诊断或下一 increment。

证据通过不会自动把 claim 升级到下一 proof layer。只要适用的 Behavior、Structure、Delivery
或 Usefulness obligation 仍未完成，verified checkpoint 就不会变成 whole-goal completion。

## Localization 与 theme contract

英文与简体中文分别使用独立 SVG 与 Mermaid，不在同一 canvas 混排双语。SVG 共享 semantic
group IDs，同时允许 locale-specific type metrics 与 line break；Mermaid 保持 region、node、
semantic-edge 与 connector-kind parity。

已验收的 SVG overview 明确 day-first，并携带 warm paper background 以稳定渲染。完整图使用
Mermaid renderer defaults，不硬编码 theme colors，让 GitHub 自行适配 day/dark surface。

## 编辑与验证

先在 `audit-runtime-model.json` 改 meaning，再在同一个 change 中更新两份 README Mermaid；
如果该 meaning 会出现在压缩 reader map 中，也同时更新两份 SVG：

```bash
python3 scripts/validate_architecture.py
python3 scripts/validate_repository.py
python3 -m unittest tests.test_architecture
```

Validator 要求七个 region、全部 stable nodes、全部 46 条 semantic edges、精确 connector kinds
与 localized edge labels、model source anchors、locale parity、top-to-bottom flow，以及可见的
只读诊断边界、显式 Operate gate、checkpoint/recovery feedback、whole-goal acceptance 与
external proof boundary。它还要求两份 SVG 可访问、standalone、semantic group 一致，并在两份
README 中保持 overview 先于 detail 的嵌入顺序。

Immutable `v0.1.0` release 仍作为早期 audit-only architecture 的历史证据。已经发布的
`v0.2.0` 使用成对 reader overview 与默认可见的完整 README Mermaid view。
