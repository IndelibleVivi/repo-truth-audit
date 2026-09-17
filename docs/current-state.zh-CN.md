# Current state

[English](current-state.md)

最后核对：2026-09-17

## Product

- Product form：standalone public repository 与 standalone Codex Skill。
- Naming：human-facing display name 为 **Repo Truth Audit**；formal name 为
  **Repository Operational Truth Audit**；public repository slug 为
  `repo-truth-audit`；Skill invocation slug
  `repository-operational-truth-audit` 保持不变。
- Version split：canonical worktree 中是尚未发布的 `0.2.0` source candidate；最新
  public release 仍是 immutable `v0.1.0`，不存在 `0.2.0` tag 或 GitHub Release。
- Scope：一条渐进式 Audit / Plan / Operate engagement。Audit 默认 read-only；Plan
  在 mutation 前终止；Operate 只有在收到 explicit、finite implementation request 且
  effect authority 匹配时才能写入。
- Canonical Skill：`skills/repository-operational-truth-audit/`；`SKILL.md` 是 compact
  router，`references/` 下分别承载渐进式 Audit、Operation 与 Recovery 方法。
- Architecture：`docs/architecture/audit-runtime-model.json` 是 semantic authority；
  两份 localized README Mermaid views 与其保持七个 region、31 个 stable nodes、46 条
  semantic edges 的 parity。原 Audit topology 被完整保留，并接入可见的 Plan exit 与
  guarded Operate loop。
- Deterministic operation evidence：`evals/operation-lab/` 不调用 target model，只检验
  新增 operation invariants；其结果是 synthetic process evidence，不是 forward model
  evidence。
- Optional evidence helper：
  `skills/repository-operational-truth-audit/scripts/check_evidence.py` 只检查 cited-byte
  continuity，不证明 semantics、Git snapshot identity、atomicity、authorization 或
  completion。

## Gates

- Source integration：`0.2.0` candidate 已在已记录的 repository、synthetic-fixture 与
  declared-artifact boundaries 内达到 source-complete。Substantive commit
  `8b66e8d6608fdbb2ba2ab7908644a5c32061133a` 已 push 到 canonical public `main`；
  这里仍不把它描述为已 release、install、activate 或在 external target 上 owner-accepted。
- Deterministic validation：2026-09-17 maintainer-local PASS，覆盖 repository 与
  publication contracts、Audit / Plan / Operate architecture 与 localized Mermaid
  parity、全部 73 个 unit tests、六个 Audit fixtures、two-increment operation lab、
  system Skill validation 与 Git whitespace validation。Operation lab 自身报告 target-model
  invocations 为 0，并与独立 forward receipt 保持分层。
- Forward behavior：成对的
  [`forward-behavior-receipt`](forward-behavior-receipt.zh-CN.md) 只属于历史
  `v0.1.0` Audit-only evidence。独立的
  [`0.2.0` receipt](forward-0.2.0-receipt.zh-CN.md) 记录 focused target-model routing、
  fresh Audit regression 与同一 session 内的 two-increment Operate run；主线程 evaluator
  在 checkpoint 与 whole-goal B/S/D/U boundaries 均已验收。它只在 receipt 所述
  synthetic source 与 declared-artifact scope 内关闭 source-candidate forward gate。
- Checkpoint 与 completion：一个 coherent verified increment 可以在 whole goal 尚未完成
  时安全保留。Whole-goal completion 必须通过约定的 Behavior、Structure、Delivery、
  Usefulness witnesses；green source test 或 helper 文件存在都不够。
- Recovery：private continuity 与 cited evidence 只是 recovery aids，不是 authority。
  Resume 必须重新 pin exact repository state、检查被保留的 owner work、重跑受影响
  witnesses，并把 Recovered 与 Complete 分开。
- Git 与 CI：substantive commit `8b66e8d...` 已发布到 canonical `main`。GitHub Actions
  run [`35198597031`](https://github.com/IndelibleVivi/repo-truth-audit/actions/runs/35198597031)
  已在该 exact SHA 通过 Ubuntu/macOS 与 Python 3.10/3.13 的全部四个 jobs。后续
  status-only reconciliation 可以移动 `main`，但不改变 substantive source identity。
- Local install：此前验证过的 installed copy 是 immutable `v0.1.0`。`0.2.0` source
  candidate 尚未 install 或 activate，也不声称 installed/source equality。
- Next-turn Codex discovery：尚未观察 `0.2.0`。
- Release publication：GitHub Release `v0.1.0` 仍是最新 public release。Source-candidate
  工作不授权、也不暗示一个新 release。
  未来若获得 `0.2.0` release 授权，必须同时更新 README pinned install ref 与
  `PUBLIC_RELEASE_VERSION`；当前 tests 有意在 release gate 打开前拒绝该变化。
- Licensing：functional materials 按 SUL-1.0 source-available；standalone
  documentation、renderer-neutral architecture model，以及嵌入 README 的 Mermaid
  diagrams 按 `LICENSING.zh-CN.md` 使用 CC BY-NC-SA 4.0。权威是 path map，而不是
  single-license badge。

在这里替换 superseded status，不要追加 development diary。
