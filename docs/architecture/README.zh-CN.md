# 审计运行架构

[English](README.md)

本目录拥有公开的 audit runtime contract 架构视图。它解释一次 read-only audit
如何抵达有决策边界的结果；它不是品牌 banner、抽象项目概念，也不是这个 repo 自身的
packaging 与 release architecture。

## Reader question

> 一次只读审计如何把明确的所有者决策与精确仓库快照转化为有决策边界的答案，并在
> 未观察的外部边界前停下？

这张图通过六个 region 回答：

1. 钉住审计对象；
2. 解析权威与可达路径；
3. 穿行彼此分开的 evidence layers；
4. 挑战并裁定 material candidates；
5. 抵达 decision fixed point 并报告；
6. 把 external state 留在明确的 fresh-observation gate 之外。

## 文件

| File | Role |
| --- | --- |
| `audit-runtime-model.json` | Renderer-neutral semantic authority：audience、question、boundary、nodes、edges、states、source mapping 与 render acceptance |
| `audit-runtime.en.svg` | 独立、day-first 的英文版 |
| `audit-runtime.zh-CN.svg` | 独立、day-first 的简体中文版 |
| `../../scripts/render_architecture_svg.py` | 确定性 visual composition 与 locale-specific line breaking |
| `../../scripts/validate_architecture.py` | Model、source-anchor、topology、localization、SVG-ID、accessibility 与 render-drift validation |

JSON model 拥有语义；renderer 拥有固定 geometry 与压缩后的 display copy。两份 SVG 是
tracked generated artifacts，GitHub 与 offline reader 无需 build step 即可显示。

## Truth sources

每个内部 node 都映射到当前 repository authority：

- [`../product-spec.zh-CN.md`](../product-spec.zh-CN.md) 拥有 accepted product behavior；
- [`../evidence-model.zh-CN.md`](../evidence-model.zh-CN.md) 拥有 proof、adjudication、
  clean、unknown 与 stopping semantics；
- [`../../skills/repository-operational-truth-audit/SKILL.md`](../../skills/repository-operational-truth-audit/SKILL.md)
  拥有 runtime workflow 与 invocation boundaries；
- [`../../AGENTS.md`](../../AGENTS.md) 拥有 repository、read-only、source/install、
  privacy 与 publication boundaries。

External-state node 被明确标记为 `unobserved_by_default`。图不会因为存在 repository
evidence，就声称 runtime、edge、device、account 或 owner-acceptance surface 已被观察。

## Connector meanings

视觉上只使用三种 connector meanings：

- teal 实线：范围内、承载证据的穿行；
- clay 虚线：可选 specialist 或经明确授权的 fresh external observation；
- teal 点状回路：新的决策相关 evidence edge 使审计重新穿行。

证据通过不会自动把 claim 升级到下一层。Source、derived artifact、
installed/deployed identity 与 external state 始终分开。

## Localization contract

英文与简体中文是两份独立 SVG，不是在同一画布上混排的 bilingual text。两版共享
region、node 与 semantic-edge IDs，但允许独立调整 labels 与 line breaks。
Renderer-neutral model 为所有 semantic labels、responsibilities、limits、edge labels、
state labels 与 primary reader question 保存两种语言的版本。

## Render 与 validate

Model 或 renderer 改变后，重新生成两份 artifact：

```bash
python3 scripts/render_architecture_svg.py
```

然后运行：

```bash
python3 scripts/validate_architecture.py
python3 scripts/render_architecture_svg.py --check
```

Validator 要求稳定 topology、有效的 repository source anchors、恰好三种 connector
meanings、精确 locale parity、直接可访问的 title 与 description、day-first surface、
当前 model digest，以及可见的 decision-bearing feedback 与 proof-boundary edges。

SVG 不包含 scripts、network dependencies、embedded raster images 或 `foreignObject`
content；它们是普通的 standalone SVG files。
