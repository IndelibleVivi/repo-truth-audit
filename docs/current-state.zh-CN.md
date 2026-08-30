# Current state

[English](current-state.md)

最后核对：2026-08-30

## Product

- Product form：standalone public repository 与 standalone Codex Skill。
- Version：public release `v0.1.0`；当前 `main` 包含尚未另行发布的 architecture
  presentation correction，并不重打该 release tag。
- Scope：完整 topology-first、decision-bounded、read-only audit contract。
- Canonical Skill：`skills/repository-operational-truth-audit/`。
- Public documentation：分开的 English 与简体中文 editions。
- 当前 `main` 的 architecture：一个 renderer-neutral semantic model，加上两份
  localized README 各自的一张原生 Mermaid diagram。两版均保留六个 region、21 个
  stable nodes、30 条 semantic edges、精确 connector-kind parity，以及明确的
  read-only、external-proof 与 fixed-point boundaries。
- 历史 release architecture：immutable `v0.1.0` 包含更早的 localized SVG pair 与
  deterministic renderer。Tagged bytes 继续作为 release evidence；generated SVG 与
  renderer 已从当前 source 退役，而不是作为平行 active path 继续维护。
- Softpowers relationship：只作为可选 companion/reference；不拥有 generation、
  bundling、installation 或 version。

## Gates

- Current source：localized README Mermaid blocks 是 active public architecture
  views；`docs/architecture/audit-runtime-model.json` 仍是 semantic authority。
  Architecture docs、product spec、AGENTS、licensing map、changelog、validators、
  tests 与 CI commands 已按这一分工完成对账。
- Deterministic validation：2026-08-30 本地 PASS——architecture model、source
  anchors、精确 Mermaid topology、localized edge labels、connector-kind 与 locale
  parity、repository/publication validation、15 个 unit tests、六个 fixture truth
  checks、fixture self-test、system Skill quick validation 与 Git whitespace
  validation。
- Mermaid render acceptance：local renderer 与 public GitHub README rendering 是
  两个不同 proof layer，必须分别从精确 rendered output 记录；syntax/model parity
  本身不是 visual acceptance。
- Independent forward behavior：2026-08-30 PASS。Artifact-split case 抵达 stale
  distributed entrypoint 与 false-green source test；clean control 把
  stable/development selection 裁定为 intentional multiplicity。
- Git release identity：canonical `0.1.0` Skill bytes 在
  `e15dbabc84d3cae35c40dd9a0a87343fd57981d2` 写入。Annotated tag object
  `235be6e839a87867b7a0758b47ce577c66380111` peeled 到 release commit
  `0180e4c23413a0691f4e895a0d64d7efaa0a12bb`；tag 保持 immutable。
- Local install：`v0.1.0` PASS。Canonical 与 installed Skill digests 均为
  `30d7ed369fad578c12d83291a17edaad4ad8c3195b2b7b31294c48ecf7ebe69e`。Mermaid
  correction 不改变 Skill package bytes，因此不产生新的 install 或 next-turn
  discovery claim。
- Next-turn Codex discovery：尚未观察。
- Release CI：PASS。Actions run `33295744677` 在 peeled `v0.1.0` release commit 上
  通过全部四个 Ubuntu/macOS、Python 3.10/3.13 jobs。Mermaid correction 的 live CI
  必须从其精确 pushed `main` commit 读取；workflow source 与 live CI 仍是不同事实。
- Release publication：PASS。GitHub Release `v0.1.0` 已于 2026-08-30 发布，不是
  draft 或 prerelease。Anonymous tagged read-back、disposable public-tag install、
  Skill validation、digest equality 与 pinned SUL text 已验证。当前 README architecture
  correction 不暗示一个新 release。
- Licensing：functional materials 在 SUL-1.0 下 source-available；standalone
  documentation、renderer-neutral architecture model，以及嵌入 README 的 Mermaid
  diagrams 按 `LICENSING.zh-CN.md` 使用 CC BY-NC-SA 4.0。GitHub 将 layered repository
  license 显示为 `Other`；权威是 path map，不是单一 license badge。

在这里替换 superseded status，不要追加 development diary。
