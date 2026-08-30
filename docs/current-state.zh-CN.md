# Current state

[English](current-state.md)

最后核对：2026-08-30

## Product

- Product form：standalone public repository 与 standalone Codex Skill。
- Naming：human-facing display name 为 **Repo Truth Audit**；formal name 为
  **Repository Operational Truth Audit**；public repository slug 为
  `repo-truth-audit`；Skill invocation slug
  `repository-operational-truth-audit` 保持不变。
- Version：public release `v0.1.0`；当前 `main` 包含尚未另行发布的 architecture
  presentation、naming、eval-fidelity 与 public-evidence corrections，并不重打该
  release tag。
- Scope：完整 topology-first、decision-bounded、read-only audit contract。
- Canonical Skill：`skills/repository-operational-truth-audit/`。
- Public documentation：分开的 English 与简体中文 editions。
- Public forward evidence：成对的
  [`forward-behavior-receipt`](forward-behavior-receipt.zh-CN.md) 记录 tested subject
  identity、dirty/clean cases、material results、proof layers、overhead limits、
  `UNKNOWN` trace fields 与 explicit external boundaries。
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
  Result examples 位于 diagram 之前；本轮 naming/eval/evidence patch 不改变 diagram
  本身。Architecture docs、product spec、AGENTS、changelog、validators、tests 与 CI
  commands 已按这一分工完成对账。
- Eval fidelity：intentional-multiplicity clean canary 现在要求
  `Decision answer: ready`，并排除 `Decision answer: not ready`；focused regression
  test 阻止含混的 `"ready"` substring assertion 回归。
- Deterministic validation：2026-08-30 本地已对 repository/publication validation、
  architecture model 与 localized Mermaid parity、16 个 unit tests、六个 fixture truth
  checks、fixture self-test、system Skill quick validation 与 Git whitespace validation
  得到 PASS。由于 host Python runtimes 不带 PyYAML，quick validator 通过 isolated `uv`
  environment 运行；repo 或 Skill package 没有因此新增 dependency。
- Mermaid render acceptance：2026-08-30 对 public `main` architecture commit
  `9805fa52f35a3635ee66e3f651ca891de4baad23` PASS。GitHub 在 light mode 下成功
  render 两份 localized block；read-only、external-proof、fixed-point 与 end re-pin
  boundaries 均存在，中文 rendered surface 还读回了全部 30 条 localized edge labels。
  Native viewer 提供 zoom 与 pan。由于完整 topology 信息密度很高，default fit 仍然
  紧凑；在不使用 native viewer 时，不把它冒充为 large-text acceptance。
- Independent forward behavior：2026-08-30 PASS。Artifact-split case 抵达 stale
  distributed entrypoint 与 false-green source test；clean control 把
  stable/development selection 裁定为 intentional multiplicity。Public-safe receipt
  暴露 material result 与 proof boundary，并把不可得的 model、effort、command-count
  与 plan-count fields 保持为 `UNKNOWN`。
- Git release identity：canonical `0.1.0` Skill bytes 在
  `e15dbabc84d3cae35c40dd9a0a87343fd57981d2` 写入。Annotated tag object
  `235be6e839a87867b7a0758b47ce577c66380111` peeled 到 release commit
  `0180e4c23413a0691f4e895a0d64d7efaa0a12bb`；tag 保持 immutable。
- Local install：immutable `v0.1.0` PASS。Tagged 与 installed Skill digests 均为
  `30d7ed369fad578c12d83291a17edaad4ad8c3195b2b7b31294c48ecf7ebe69e`。Current
  source digest 为
  `ca4fd01e20964c87884f4fe46a1ceb0864cf23b55061c90cd5bc24558a396a3a`，因为
  `agents/openai.yaml` 现在使用更短的 display name。Runtime `SKILL.md` 仍为
  byte-identical，SHA-256 是
  `cc16bad2960a3d0e315c055cf5ec244ec57c2f7cc51da12d5d480b603bf1c15f`。Current
  `main` 未安装，因此不声称 unreleased metadata change 已达到 installed/source digest
  equality。
- Next-turn Codex discovery：尚未观察。
- Current-main CI：naming/eval/evidence patch 尚待观察。较早的 Actions run
  `33299194074` 已在 pre-patch head `6fe94527...` 通过全部四个 Ubuntu/macOS、Python
  3.10/3.13 jobs。Release run `33295744677` 另行在 peeled `v0.1.0` release commit
  上通过同一 matrix。Workflow source 与 live CI 仍是不同事实。
- Release publication：PASS。GitHub Release `v0.1.0` 已于 2026-08-30 发布，不是
  draft 或 prerelease。Anonymous tagged read-back、disposable public-tag install、
  Skill validation、digest equality 与 pinned SUL text 已验证。当前 README architecture
  correction 不暗示一个新 release。
- Current-main publication：naming/eval/evidence patch 以及 canonical remote rename 到
  `https://github.com/IndelibleVivi/repo-truth-audit` 尚待完成。Accepted architecture
  identity 仍为 `9805fa52...`，本 patch 不重写它。
- Licensing：functional materials 在 SUL-1.0 下 source-available；standalone
  documentation、renderer-neutral architecture model，以及嵌入 README 的 Mermaid
  diagrams 按 `LICENSING.zh-CN.md` 使用 CC BY-NC-SA 4.0。GitHub 将 layered repository
  license 显示为 `Other`；权威是 path map，不是单一 license badge。

在这里替换 superseded status，不要追加 development diary。
