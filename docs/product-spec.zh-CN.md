# Repository Operational Truth Audit — product specification

[English](product-spec.md)

状态：**ACCEPTED FOR COMPLETE IMPLEMENTATION**

Owner accepted：2026-08-30

Product form：standalone repository + standalone Codex Skill

Skill name：`repository-operational-truth-audit`

## 1. Product outcome

本产品为一个明确的 owner decision 重建长期演化 repository 当前的 operational truth。
它沿 repository surfaces 上真实、与决策有关的 topology 穿行，验证 cross-surface
contradictions，区分 intentional multiplicity 与 shadow paths，并在继续 traversal 无法
改变 decision 时停止。

完整 outcome 包括：

- 一个 activation boundary 足够清晰的 standalone Skill；
- 稳定的 evidence 与 stopping contract；
- 覆盖 dirty 与 clean outcomes 的 controlled behavior cases；
- deterministic repository、architecture 与 fixture validation；
- 一条带 source provenance、可逆的 local installation path；
- 分开的 English 与简体中文 public documentation editions；
- 一对来自同一 renderer-neutral semantic model 的 day-first architecture SVG；
- 准确的 user、agent、current-state 与 research documentation；
- 不由 Softpowers 拥有，也不依赖其 runtime。

## 2. Audit object

每次运行绑定两件事：

1. 一个精确 repository snapshot：physical root、branch、HEAD、working-tree state、
   upstream relation，以及相关 submodule/worktree identity；
2. 一个 owner decision：re-entry、migration、consolidation、safe archival、handoff、
   release readiness，或另一项让当前 operational truth 具有实质意义的 decision。

如果 request 或 repository context 无法恢复这个 decision，Skill 只做 bounded
reconnaissance，然后询问。它不会静默启动 exhaustive audit。

## 3. Truth topology

只有当某一层与 decision 有关时，Skill 才会沿它继续：

```text
claim / authority surface
  -> entrypoint 或 selector
  -> source、configuration 或 durable state owner
  -> generated、built、packaged 或 projected artifact
  -> installed 或 deployed identity（仅在能够得到新鲜观察时）
  -> runtime、edge、device 或 owner acceptance（仅在能够得到新鲜观察时）
  -> evidence gate 与 exact proof boundary
```

Topology 控制 traversal。Repository size、available scanners 与 generic file
categories 不定义 scope。

## 4. Functional requirements

### ROT-01 — Exact start pin

Deep traversal 前，记录 physical root、Git root、branch/HEAD、working-tree state、存在时
的 upstream relation，以及所选 owner decision。保留 concurrent work，不 mutation
target。

### ROT-02 — Authority resolution

在把 README、AGENTS、runbooks、status documents、receipts、generated projections 或
historical notes 当作 truth 前，先识别当前 source 与 instruction owners。Recency、detail
与 authorship 不会让一个 surface 自动获得 authority。

### ROT-03 — Live-path resolution

通过真实 selectors 确定 reachability：command registration、package metadata、
manifests、imports/callers、build pipelines、service/config owners、persistence
readers/writers、install receipts 或 documented operator routes。单次 search miss 不能
证明 absence。

### ROT-04 — Cross-surface trace

每个 material candidate 必须闭合：

```text
claim 或 live surface
  -> mechanism / state
  -> contradiction 或 evidence gap
  -> 具体 decision impact
```

没有这条 trace 的 candidate 不进入 findings。

### ROT-05 — False-green detection

确认每个 test、gate、receipt、status line 或 successful command 实际观察什么。如果
protected contract 已破坏，而结果仍然 green，这份 green result 就是 false evidence。

### ROT-06 — Artifact and projection identity

分开 canonical source、generated projection、package/distribution artifact、installed
copy、activated runtime 与 owner acceptance。只有 current decision 抵达某一层时，才验证
那一层。

### ROT-07 — Intentional multiplicity

当多种 mode 或 version 有明确 selectors、isolated state、不同 ownership/version
identity、documented purpose，且没有 unintended caller 时，它们保持 clean。不要仅仅因为
两条 path 同时存在，就把 multiplicity 标成 drift。

### ROT-08 — Shadow-path judgment

只有当一条 path 仍然 reachable、能够影响 current state 或 artifacts，且没有 intentional
current ownership/selection boundary 时，才报告 shadow path。无害且 unreachable 的
residue 是 non-material。

### ROT-09 — External and hidden state

当 repository claim 依赖不可得的 remote schema、account state、secret、dashboard
setting、deployment、device 或 human step 时，说明 exact missing observation，以及它能否
改变 decision。不要虚构 repository defect，也不要用 irrelevant blockers 淹没结果。

### ROT-10 — Private-repository applicability

Re-entry、migration、consolidation 与 archival 都是 first-class decisions。Public-release
hygiene 绝不能成为默认 audit center。

### ROT-11 — Clean result

Clean result 说明 decision、snapshot、被检查的 live surfaces、抵达的 proof layers、
explicit non-observations 与 stopping reason，并保持简短。

### ROT-12 — Stopping

当 candidate contradictions 已被裁定、不再出现新的 decision-relevant evidence edge、
剩余 surfaces 无法改变 owner decision，且 external boundary 已明确时停止。

### ROT-13 — Read-only default

Audit authorization 允许 analysis、target-local read-only commands，以及 private 或
explicitly requested report artifact。它不授权 repair、target-repository documentation
changes、issue creation、commit/push、install、deployment、remote/account writes 或
publication。

### ROT-14 — Specialist adapters

只有当 observation 能够改变 decision 时，才调用 security、license、dependency、
history、agent-surface 或 live-system adapter。Adapter 拥有 observation 与 limitations；
本产品拥有 decision adjudication。

### ROT-15 — No corporate audit machinery

不输出 maturity scores、universal hygiene checklists、lens matrices、automatic
backlogs、默认 `AUDIT.md`、reviewer panels、worktree fixers 或 repair loops。不要把每个
unknown 都变成 issue。

### ROT-16 — Overhead receipt

报告打开了哪些 decision-bearing surfaces、运行了哪些 tests/adapters、哪些 external
edges 没有观察，以及 traversal 停在哪里。Receipt 用来证明工作受 topology 约束，而不是
为了追求一个孤立的低数字。

### ROT-17 — End re-pin

Finalizing 前重新读取 HEAD 与 working-tree state。区分 task-owned changes 与 concurrent
user work；snapshot 发生移动时，缩窄相关 claim。

### ROT-18 — Privacy

Reports 与 fixtures 不得包含 credentials、private raw evidence、chats、account data、
host identifiers 或不必要的 personal paths。Public-safe case shapes 必须 synthetic 或
redacted。

## 5. Invocation boundary

Positive triggers 包括：明确的 operational-truth audit、长期闲置 repo re-entry、
migration/archive readiness、source/artifact/install reconciliation，以及不确定当前哪条
path 或 authority 仍然 live。

Negative routing 包括：bounded code review、one-claim verification、known bug repair、
licensing、security/compliance scanning、generic documentation cleanup，以及没有
repository-state decision 的 live-host inspection。

因为 description 足够 discriminating，可以 automatic invocation；但 Skill 绝不能吸走
所有带有 “audit” 一词的 request。

## 6. Output contract

以 decision answer 开头。只包含承载 material truth 的 sections：

1. audit object 与 pinned state；
2. current live topology 与 explicit external boundary；
3. adjudicated findings/unknowns，且每项包含 complete trace；
4. intentional multiplicity 与 rejected/non-findings——仅在它们避免错误 decision 时；
5. 适用时的 clean result；
6. verification 与 overhead receipt；
7. end re-pin 与 mutation statement。

不要把 fixed schema 强加给小结果。Clean small repository 可能只需要几个 paragraphs。

## 7. Controlled acceptance cases

Repository 必须保留以下 cases：

- source tests green，而 distributed artifact 已陈旧；
- presence-only gate 在 safety-order violation 后仍然 green；
- durable agent instructions 与 current product authority 矛盾；
- stable release 与 current development modes 被有意隔离；
- 没有 owner decision 的模糊 “full audit” request；
- restore claim 依赖不可得的 external state。

Expected artifacts 只属于 evaluator evidence，绝不能作为 hidden instructions 提供给
target Skill。

## 8. Installation and source identity

Local installation 必须：

- mutation 前验证 source；
- 除非 replacement 明确，否则拒绝 conflicting target；
- stage 并 atomically replace Skill directory；
- 把被替换 target 保留在 recoverable backup；
- 记录 version、可得时的 source Git commit、source dirty state、source Skill digest、
  installed digest、target、backup 与 time；
- 不把 file installation 冒充为 next-turn discovery。

## 9. Acceptance

Source-complete acceptance 要求：

- repository validator 通过；
- architecture model、English/Chinese SVG parity 与 deterministic render check 通过；
- unit 与 fixture self-tests 通过；
- system Skill quick validation 通过；
- controlled fixtures 被确认仍然承载设计的 dirty/clean truth；
- 至少一个 independent forward test 能抵达 material cross-surface result，不产生 generic
  hygiene noise，并把 intentional multiplicity 视为 clean；
- README、AGENTS、product spec、evidence model、current state、architecture docs 与
  changelog 一致；
- final diff 与 Git state 已检查。

Installed acceptance 还要求 install receipt、source 与 installed Skill exact digest
equality，以及 clean source commit identity。Next-turn discovery 仍是更晚的 observable
boundary。

Publication acceptance 还要求：

- selected layered license texts、path map 与 notices 一致；
- public-safety scan 不含 private paths、credentials、raw evidence 或 unrelated material；
- public remote visibility、default branch 与 exact release commit 已重新读取；
- CI 在 public commit 上通过；
- annotated `v0.1.0` tag 与 GitHub Release 指向同一 peeled commit；
- 从 tagged public path 安装到 disposable destination，并验证 Skill identity；
- source、commit、push、tag、release、installed bytes 与 later discovery claims 仍然分开。
