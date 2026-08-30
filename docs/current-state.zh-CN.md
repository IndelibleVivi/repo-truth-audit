# Current state

[English](current-state.md)

最后核对：2026-08-30

## Product

- Product form：standalone public repository 与 standalone Codex Skill。
- Version：public release `v0.1.0`。
- Scope：完整 topology-first、decision-bounded、read-only audit contract。
- Canonical Skill：`skills/repository-operational-truth-audit/`。
- Public documentation：分开的 English 与简体中文 editions。
- Architecture：一个 renderer-neutral model，加上分开的 day-first English 与中文 SVG
  artifacts；semantic、locale、accessibility 与 render-drift checks 已存在。
- Softpowers relationship：只作为可选 companion/reference；不拥有 generation、
  bundling、installation 或 version。

## Gates

- Source：public `v0.1.0` 包含 canonical Skill、layered license files、
  paired public documentation、evidence model、controlled eval pack、architecture
  model/renderer、validators、tests 与 transactional installer。
- Deterministic validation：2026-08-30 PASS——architecture model 与 locale parity、
  deterministic SVG render check、repository/publication validator、14 个 unit tests、
  六个 fixture truth checks、fixture self-test、system Skill quick validation 与 Git
  whitespace validation。
- Independent forward behavior：2026-08-30 PASS。Artifact-split case 抵达 stale
  distributed entrypoint 与 false-green source test；clean control 把
  stable/development selection 裁定为 intentional multiplicity。
- Git source identity：canonical `0.1.0` Skill bytes 在
  `e15dbabc84d3cae35c40dd9a0a87343fd57981d2` 写入。Annotated tag object
  `235be6e839a87867b7a0758b47ce577c66380111` peeled 到 release commit
  `0180e4c23413a0691f4e895a0d64d7efaa0a12bb`。`main` 可以包含后续 status-only
  reconciliation；tag 仍是 immutable release identity。
- Local install：PASS。以上 clean source commit 已在 2026-08-30 以 transactional
  方式安装；canonical 与 installed Skill digests 均为
  `30d7ed369fad578c12d83291a17edaad4ad8c3195b2b7b31294c48ecf7ebe69e`。Local receipt
  记录 clean source identity 与 recoverable backup。
- Next-turn Codex discovery：尚未观察。
- Remote/CI：PASS。Public repository 是
  `https://github.com/IndelibleVivi/repository-operational-truth-audit`，default branch
  是 `main`；Actions run `33295744677` 在 peeled release commit 上通过全部四个
  Ubuntu/macOS、Python 3.10/3.13 jobs，并使用 Node 24 Actions。Workflow source 与
  live CI 仍是不同事实。
- Publication：PASS。GitHub Release `v0.1.0` 已于 2026-08-30 发布，不是 draft 或
  prerelease。Anonymous raw read-back 的两份 README、两份 localized SVG 与 `LICENSE`
  都与 tagged bytes 一致。从 public tag 安装到 disposable destination 后，Skill quick
  validation 通过；digest 与以上 canonical digest 相同，SUL text 也匹配 pinned
  SHA-256 `c6d0dde0f0463c800e542d7d64237ffef37f43b17004975a558604f17b5d1af1`。
- Licensing：functional materials 在 SUL-1.0 下 source-available；standalone
  documentation 与 independent diagrams 按 `LICENSING.zh-CN.md` 使用 CC BY-NC-SA
  4.0。GitHub 将 layered repository license 显示为 `Other`；权威是 path map，不是单一
  license badge。

在这里替换 superseded status，不要追加 development diary。
