# Independent forward-behavior receipt

[English](forward-behavior-receipt.md)

观察日期：2026-08-30

状态：**在下述 evidence boundary 内 PASS**

这是一份由两次 independent、read-only forward run 投影出的 public-safe receipt。它
记录 tested decisions、material results、proof layers 与 limitations；它不是 transcript，
也不替代 evaluator artifacts。

## Subject identity

| Field | 记录值 |
| --- | --- |
| Formal product name | Repository Operational Truth Audit |
| Skill invocation slug | `repository-operational-truth-audit` |
| Run-local Git ref | **UNKNOWN**——evaluator results 没有保留 target-subject HEAD |
| Runtime Skill entrypoint digest | `cc16bad2960a3d0e315c055cf5ec244ec57c2f7cc51da12d5d480b603bf1c15f`（`SKILL.md`，SHA-256） |
| Digest reconciliation | Initial Skill commit `5d6a9f78c0068c5ac3b0ba361fb94106390905d1`、release-source commit `e15dbabc84d3cae35c40dd9a0a87343fd57981d2` 与测试时的 pre-display-name source 均有相同 entrypoint digest |
| Observed model | **UNKNOWN** |
| Observed reasoning effort | **UNKNOWN** |

后来采用 **Repo Truth Audit** 只改变 UI metadata，不改变本 receipt 所记录 digest 的
runtime `SKILL.md`。

## Case results

### Source / artifact split

- **Case：**[`source-artifact-split`](../evals/cases/source-artifact-split/)
- **Decision prompt：**这个 repo 是否已经可以作为 packaged CLI 交给 operator？沿真实
  distribution selector 走，并判断 green test 实际证明了什么。
- **Public repository shape：**README claim、`distribution.json`、source CLI、
  distributed CLI，以及只检查 source 的 test。
- **Material result：****Not ready.** `distribution.json` 选择 `dist/cli.py`，其 fresh
  output 为 `artifact-v1`；current source 与 documented package contract 均为
  `artifact-v2`。Green test 直接执行 `src/cli.py`，因此无需抵达 selected distribution
  artifact 也能保持 green。
- **Proof layers reached：**documentation claim -> distribution manifest -> selected
  artifact -> fresh execution；test entrypoint -> source execution -> assertion boundary。
- **Boundary：**未观察 installed copy、activated runtime、operator environment 或 owner
  acceptance。

### Intentional multiplicity clean control

- **Case：**[`intentional-multiplicity`](../evals/cases/intentional-multiplicity/)
- **Decision prompt：**当 development 在 `main` 继续时，能否使用 documented stable
  artifact selector，同时确保两条 route 不会静默选中彼此？
- **Public repository shape：**README 与 changelog、一个 executable selector、分开的
  stable/development state records，以及分开的 selected identities。
- **Material result：****Ready within repository scope.** Stable 与 development 都要求
  explicit selector，解析到 distinct identities，并拒绝 missing 或 cross-boundary
  selector combinations。结论是 intentional multiplicity，而不是 drift 或 shadow path。
- **Proof layers reached：**documented command -> executable selector ->
  channel-specific state -> selected identity 与 physical path -> successful route 加
  cross-boundary rejection。
- **Boundary：**installed runtime 不在范围内；repository metadata 也没有独立证明任意
  release bytes 受到 filesystem-enforced immutability。

这份 clean result 来自 fixture 完成后的 retest。更早一轮针对 incomplete fixture shape
的 exploratory pass 不作为 product evidence。

## Overhead record

| Case | Command executions | Plan updates | Nested subagent events | Case ceilings |
| --- | --- | --- | --- | --- |
| `source-artifact-split` | **UNKNOWN** | **UNKNOWN** | 观察到 `0` | `14 / 1 / 0` |
| `intentional-multiplicity` | **UNKNOWN** | **UNKNOWN** | 观察到 `0` | `12 / 1 / 0` |

保留下来的 public-safe results 列出了 material commands，却没有 low-level event
counters。根据 shell lines 反推 tool-event count 会产生误导，因此不可得的 observed
counts 保持 `UNKNOWN`。最后一列来自各 public case contract 的 command / plan /
subagent ceilings，不是 observed usage。

## Retention 与 limitations

- Full evaluator result text 留在 private originating task history；本 public tree 没有复制
  raw trace 或 private repository evidence。
- 没有保留 standalone low-level event-trace export，因此 exact command 与 plan counts
  为 `UNKNOWN`。
- Deterministic assertions 现在会区分 `Decision answer: ready` 与
  `Decision answer: not ready`。一个其他方面正确的结果是否附带 unrelated generic
  hygiene noise，仍由 semantic evaluator judgment 处理；本 receipt 不为此发明 complex
  schema。
- 两次运行只证明 Skill 在这两个 public synthetic shapes 上的 forward behavior；不证明
  installation、Codex discovery、live runtime state 或 owner acceptance。
