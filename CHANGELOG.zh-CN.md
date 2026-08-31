# Changelog

[English](CHANGELOG.md)

## Unreleased

- 为 tracked text files 保留 LF，并按规范化后的 POSIX relative path 排序 Skill digest
  entries，使普通 Windows source checkout 具备 deterministic behavior；同时为两个
  boundaries 加入 regression coverage。
- 将 **Repo Truth Audit** 作为 human-facing display name，并将
  `repo-truth-audit` 作为 public repository slug；formal product name 与
  `repository-operational-truth-audit` Skill slug 保持不变。
- 收紧 intentional-multiplicity clean-control canary，使以
  `Decision answer: not ready` 开头的 verdict 不再能够通过 positive assertion。
- 加入 public-safe independent forward-behavior receipt，并在 README 架构图前加入极短的
  dirty/clean result examples。
- 将当前 `main` 的 active architecture surface 替换为分别嵌入 English 与简体中文
  README 的原生 Mermaid diagrams。
- 保留 renderer-neutral model、六个 region、全部 stable node IDs、全部 30 条 semantic
  edges，以及 read-only、external-proof 与 fixed-point boundaries；同时从当前 source
  退役 fixed-canvas SVG renderer。
- 加入精确 Mermaid topology、localized edge-label、connector-kind、theme-neutrality 与
  locale-parity validation。

## 0.1.0 — 2026-08-30

- 将 Repository Operational Truth Audit 作为 independently owned、standalone Codex
  Skill 与 public source-available repository 发布。
- 加入完整的 decision-bounded、topology-first、read-only audit contract。
- 加入覆盖 artifact drift、false-green evidence、authority drift、intentional
  multiplicity、missing decision 与 unavailable external state 的 controlled behavior
  cases。
- 加入 deterministic repository、fixture、installation、architecture-model、
  localized-SVG 与 render-drift validation。
- 加入 transactional local installer，记录 source commit、dirty state、digest、backup
  与 target provenance。
- 加入分开的 English 与简体中文 README、product、evidence、architecture、research、
  current-state、licensing、changelog 与 release-note editions。
- 通过显式 path map，将 functional materials 置于 SUL-1.0，将 standalone
  documentation 与 independent diagrams 置于 CC BY-NC-SA 4.0。
