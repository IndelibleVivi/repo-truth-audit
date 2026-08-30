# Current state

[English](current-state.md)

最后核对：2026-08-30

## Product

- Product form：standalone public repository 与 standalone Codex Skill。
- Version：source-complete `0.1.0` release candidate。
- Scope：完整 topology-first、decision-bounded、read-only audit contract。
- Canonical Skill：`skills/repository-operational-truth-audit/`。
- Public documentation：分开的 English 与简体中文 editions。
- Architecture：一个 renderer-neutral model，加上分开的 day-first English 与中文 SVG
  artifacts；semantic、locale、accessibility 与 render-drift checks 已存在。
- Softpowers relationship：只作为可选 companion/reference；不拥有 generation、
  bundling、installation 或 version。

## Gates

- Source：source-complete `0.1.0` publication candidate 包含 canonical Skill、layered license files、
  paired public documentation、evidence model、controlled eval pack、architecture
  model/renderer、validators、tests 与 transactional installer。
- Deterministic validation：2026-08-30 PASS——architecture model 与 locale parity、
  deterministic SVG render check、repository/publication validator、14 个 unit tests、
  六个 fixture truth checks、fixture self-test、system Skill quick validation 与 Git
  whitespace validation。
- Independent forward behavior：2026-08-30 PASS。Artifact-split case 抵达 stale
  distributed entrypoint 与 false-green source test；clean control 把
  stable/development selection 裁定为 intentional multiplicity。
- Git source identity：release source 是包含此状态的 repository commit。它尚未被 tag、
  push 或从 public remote read back；这里不声称 public identity。
- Local install：较早的 release-candidate Skill 仍处于 installed 状态。由于
  package-local license 与 notice 会改变 Skill digest，最终 `0.1.0` installation 与
  source/installed digest equality 等待 clean release commit。
- Next-turn Codex discovery：尚未观察。
- Remote/CI：public remote 与 public CI result 尚未创建或观察。Workflow source 不等于
  CI proof。
- Publication：owner 已授权 public repository，并选择 functional materials 使用
  SUL-1.0、standalone documentation 与 diagrams 使用 CC BY-NC-SA 4.0。Source
  preparation 正在进行；public visibility、tag、GitHub Release 与 tagged public install
  仍是分开的 pending gates。

在这里替换 superseded status，不要追加 development diary。
