# 审计运行架构

[English](README.md)

本目录拥有公开 audit-runtime architecture 背后的 semantic contract。两份 localized
diagram 本身直接位于 repo 根目录的两份 README 中，并使用原生 Mermaid。它们解释一次
read-only audit 如何抵达有决策边界的结果；它们不是品牌 banner、抽象项目概念，也不是
这个 repo 自身的 packaging 与 release architecture。

## Reader question

> 一次只读审计如何把明确的所有者决策与精确仓库快照转化为有决策边界的答案，并在
> 未观察的外部边界前停下？

两张图通过六个 region 回答：

1. 钉住审计对象；
2. 解析权威与可达路径；
3. 穿行彼此分开的 evidence layers；
4. 挑战并裁定 material candidates；
5. 抵达 decision fixed point 并报告；
6. 把 external state 留在明确的 fresh-observation gate 之外。

## Truth surfaces

| Surface | Authority |
| --- | --- |
| [`audit-runtime-model.json`](audit-runtime-model.json) | Renderer-neutral semantic authority：reader question、boundaries、stable IDs、nodes、edges、states、source mapping 与 render acceptance |
| [`../../README.md`](../../README.md) | 独立英文 Mermaid view |
| [`../../README.zh-CN.md`](../../README.zh-CN.md) | 独立简体中文 Mermaid view |
| [`../../scripts/validate_architecture.py`](../../scripts/validate_architecture.py) | Model、source-anchor、topology、localization、connector-kind 与 README parity validation |

JSON model 拥有语义；每份 README 拥有本 locale 的精简 display copy 与 Mermaid
syntax。两版共享 region、node 与 semantic-edge IDs，并显示 model 中的每一条 edge。

三条 `~~~` link 被明确声明为 layout-only constraints。它们使用 Mermaid invisible-link
syntax，在 README 宽度下纵向排列 challenge branches；不会增加 semantic relation，也
不会改变 model 的 30 条 edge topology。

每个内部 node 都映射到当前 repository authority：

- [`../product-spec.zh-CN.md`](../product-spec.zh-CN.md) 拥有 accepted product
  behavior；
- [`../evidence-model.zh-CN.md`](../evidence-model.zh-CN.md) 拥有 proof、
  adjudication、clean、unknown 与 stopping semantics；
- [`../../skills/repository-operational-truth-audit/SKILL.md`](../../skills/repository-operational-truth-audit/SKILL.md)
  拥有 runtime workflow 与 invocation boundaries；
- [`../../AGENTS.md`](../../AGENTS.md) 拥有 repository、read-only、source/install、
  privacy 与 publication boundaries。

External-state node 是 `unobserved_by_default`。Repository evidence 绝不会静默证明
runtime、edge、device、account 或 owner acceptance。

## Connector meanings

Mermaid view 使用三种不依赖颜色也能识别的 connector meaning：

- 实线箭头：范围内、承载证据的穿行；
- 点线箭头：可选 specialist 或经明确授权的新鲜外部观察；
- 粗回箭头：新的决策相关证据会重新打开 traversal。

证据通过不会自动把 claim 升级到下一层。Source、derived artifact、
installed/deployed identity 与 external state 始终分开。

## Localization 与 theme contract

英文与简体中文是两张独立 Mermaid diagram，不是在同一画布上混排 bilingual text。
两版共享 region、node、semantic-edge 与 connector-kind parity，同时允许各自换行。

图中使用 Mermaid renderer defaults，不写死 theme colors。GitHub 因而可以分别适配
day 与 dark surface，而不是保留固定 SVG palette 或固定画布的微缩文字。

## 编辑与验证

Architecture meaning 变更时先改 `audit-runtime-model.json`，并在同一个 change 中同步
两份 README Mermaid block。运行：

```bash
python3 scripts/validate_architecture.py
python3 scripts/validate_repository.py
python3 -m unittest tests.test_architecture
```

Validator 要求六个 region、全部 stable nodes、全部 30 条 semantic edges、精确的
connector kinds 与 localized edge labels、model source anchors、locale parity、
top-to-bottom flow，以及清楚可见的 read-only、external-proof 与 fixed-point feedback
boundaries。

Immutable `v0.1.0` release 仍是早期 SVG edition 的历史证据；当前 `main` 以 README
Mermaid views 作为 active public architecture surface。
