# Current state

[English](current-state.md)

最后核对：2026-09-17

## Product

- Product form：standalone public repository 与 standalone Codex Skill。
- Naming：human-facing display name 为 **Repo Truth Audit**；formal name 为
  **Repository Operational Truth Audit**；public repository slug 为
  `repo-truth-audit`；Skill invocation slug
  `repository-operational-truth-audit` 保持不变。
- Version split：canonical worktree 中是已经过验证的 `0.2.0` release target；最新
  public release 仍是 immutable `v0.1.0`，暂不存在 `0.2.0` tag 或 GitHub Release。
- Scope：一条渐进式 Audit / Plan / Operate engagement。Audit 默认 read-only；Plan
  在 mutation 前终止；Operate 只有在收到 explicit、finite implementation request 且
  effect authority 匹配时才能写入。
- Canonical Skill：`skills/repository-operational-truth-audit/`；`SKILL.md` 是 compact
  router，`references/` 下分别承载渐进式 Audit、Operation 与 Recovery 方法。
- Architecture：`docs/architecture/audit-runtime-model.json` 仍是 semantic authority。
  成对的 day-first SVG reader map 现在以 owner-approved compressed view 进入两份 localized
  README；默认可见的 Mermaid maps 保留全部七个 region、31 个 stable nodes 与 46 条 semantic
  edges。原 Audit topology 被完整保留，并接入可见的 Plan exit 与 guarded Operate loop。
- Deterministic operation evidence：`evals/operation-lab/` 不调用 target model，只检验
  新增 operation invariants；其结果是 synthetic process evidence，不是 forward model
  evidence。
- Optional evidence helper：
  `skills/repository-operational-truth-audit/scripts/check_evidence.py` 只检查 cited-byte
  continuity，不证明 semantics、Git snapshot identity、atomicity、authorization 或
  completion。
- Installable payload：`scripts/common.py::SKILL_PAYLOAD_FILES` 声明 validation、digest、
  staging、installed comparison 与 receipt 共用的八个 runtime files。已知 cache/bytecode
  residue 不属于 payload；其他 undeclared source entry 会 fail closed。Clean payload digest
  为 `80863c9796a2364d99f43cd81d6f53c8d6059f0c303061d18362ba683411a29f`。

## Gates

- Source integration：原始 `0.2.0` core integration 已公开于
  `8b66e8d6608fdbb2ba2ab7908644a5c32061133a`。后续对 `f84b22c...` public `main` 的
  pre-release review 发现 all-files hashing/copying 会吸收 ignored `.pyc`。Declared-payload
  correction 与 clean-payload forward follow-up 已公开于
  `2259892e8a9af918b131d7ec7a9a5d70949684f3`；对应四项
  [CI run `35214605650`](https://github.com/IndelibleVivi/repo-truth-audit/actions/runs/35214605650)
  已在 Ubuntu／macOS 与 Python 3.10／3.13 通过。双语 usage 与 release-preparation
  documentation 已通过 PR #2 merge commit
  `22b8007908b0feb8681794bdb449667a1d35d9ff` 集成，且未改变 declared Skill payload。
  成对 reader map 与 B/S/D/U 人话图例在 `19a679b...` 落地；Linux font overflow 在
  `c23dce842624e1e2ffc128db828174b88b2c09b1` 修正，完整 Mermaid map 则在
  `57ed5c830d7624372e967d72402ae83feafb29e3` 改为默认可见。这些 reader-facing 改动均未
  改变 declared Skill payload。
- Deterministic validation：2026-09-17 maintainer-local PASS，覆盖 repository 与
  publication contracts、Audit / Plan / Operate architecture 与 localized Mermaid
  parity、全部 85 个 unit tests（其中六项覆盖 documentation navigation 与 release
  preparation）、六个 Audit fixtures、two-increment operation lab、system Skill validation
  与 Git whitespace validation。Operation lab 自身报告 target-model invocations 为 0，
  并与独立 forward receipt 保持分层。
- Forward behavior：成对的
  [`forward-behavior-receipt`](forward-behavior-receipt.zh-CN.md) 只属于历史
  `v0.1.0` Audit-only evidence。独立的
  [`0.2.0` receipt](forward-0.2.0-receipt.zh-CN.md) 保留 focused target-model routing、
  fresh Audit regression 与 same-session two-increment Operate run；现在也把旧 directory
  digest 对账到一个被复制的 `.pyc`，并新增 clean eight-file payload 上的实际 mutation-free
  Plan 与 one-request whole-goal Operate evidence。主线程只在 receipt 所述 synthetic source
  与 declared-artifact scope 内接受 B/S/D/U。
- Checkpoint 与 completion：一个 coherent verified increment 可以在 whole goal 尚未完成
  时安全保留。Whole-goal completion 必须通过约定的 Behavior、Structure、Delivery、
  Usefulness witnesses；green source test 或 helper 文件存在都不够。
- Recovery：private continuity 与 cited evidence 只是 recovery aids，不是 authority。
  Resume 必须重新 pin exact repository state、检查被保留的 owner work、重跑受影响
  witnesses，并把 Recovered 与 Complete 分开。
- Git 与 CI：pre-release reader surfaces 已公开至
  `57ed5c830d7624372e967d72402ae83feafb29e3`。GitHub Actions run
  [`35239646950`](https://github.com/IndelibleVivi/repo-truth-audit/actions/runs/35239646950)
  已为该 exact commit 通过 Ubuntu／macOS 与 Python 3.10／3.13 全部四个 jobs。公开仓库仍为
  public、默认分支仍为 `main`；GitHub About 已更新并回读为 “Evidence-led repository
  diagnosis and verified structural change for Codex.”
- Local install：日常副本已从 `v0.1.0` transactionally upgrade，并保留 backup。Receipt
  记录 version `0.2.0`、clean source commit
  `c23dce842624e1e2ffc128db828174b88b2c09b1`，source／installed digest 均为
  `80863c9796a2364d99f43cd81d6f53c8d6059f0c303061d18362ba683411a29f`，且安装目录没有
  undeclared file。后续 commits 只改变 reader documentation。
- Next-turn Codex discovery：三个 fresh task 都从默认 user Skill root 加载 installed Skill。
  Audit 保持只读并闭合 selected-artifact contradiction；Plan 在零 mutation 下产出可施工计划；
  one-request Operate 自行完成有限 synthetic refactor、退役 legacy owner，并通过五项 behavior／
  structure／delivery／usefulness checks。主线程另行通过 selected-entry 与 exactly-once state checks。
- Release publication：GitHub Release `v0.1.0` 仍是最新 public release。Source-candidate
  已获得 publication 授权，`v0.2.0` ref 与 `PUBLIC_RELEASE_VERSION` 现在共同标识 release
  target，但 tag 存在前 install command 明确不可用。Release-note draft assertion 在本次
  pre-publication commit 继续生效，只有 tag／Release／public install 回读 gate 通过后才迁移。
- Licensing：functional materials 按 SUL-1.0 source-available；standalone
  documentation、renderer-neutral architecture model、成对 SVG reader map，以及嵌入
  README 的 Mermaid diagrams 按 `LICENSING.zh-CN.md` 使用 CC BY-NC-SA 4.0。权威是
  path map，而不是 single-license badge。

在这里替换 superseded status，不要追加 development diary。
