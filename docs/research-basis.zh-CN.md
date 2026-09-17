# Research basis 与 provenance

[English](research-basis.md)

状态：2026-08-30 pre-spec research 与 2026-09-17 Audit / Plan / Operate expansion
research 的 public-safe synthesis。完整 raw research packets 与 private repository
evidence 保留在本 repo 之外。

## Product-form decision

Research 接受了 `DISTINCT_SKILL_HYPOTHESIS_SUPPORTED`：一种反复出现的
topology-first behavior 能够在结构不同的 repositories 中产生与决策实质相关的 findings
或 unknowns，同时保留短小的 clean control，并与 bounded code review 与 one-claim
verification 形成稳定边界。

Evidence classes 包括：

- private infrastructure re-entry 与 presence-only safety gate；
- source/generated/installed Skill identity 与 provenance；
- durable agent instructions 偏离当前 product authority 的 local-first product；
- 有意分开的 stable-release/current-development clean control；
- controlled source-green/distribution-stale package fixture。

本 repo 不携带 private raw evidence、account data、host addresses 或 local user paths。

## External behavioral sources

### Conor Bronsdon / `repo-audit`

- Ref：`ec1b73485c442299f3c189afd4d4dd80b9a413e5`
- 观察到的 license：Apache-2.0；repository 包含 `NOTICE`。
- 概念上保留：source-before-claims、enforcement classification、concept search、
  artifact tracing、coverage-bounded clean results。
- 拒绝：以 public launch 为中心、universal community/license hygiene、fixed launch
  templates 与 generic small-repository recommendations。
- 本项目没有复制其 text、template 或 code。

### The Interdependency / `repo-audit-repair`

- Ref：`7a10c6af08bdc23cb745a7f2384ac641d68db30c`
- 观察到的 license：MPL-2.0。
- 概念上保留：exact repository identity、false-green discipline、ownership，以及
  defect/environment/external/policy/unknown 的分离。
- 拒绝：把 read-only audit 与 repair、merge、release、deployment 捆绑。
- 没有复用 file-level material；未来若发生复用，必须单独完成 MPL-2.0 compliance 与
  attribution review。

## 2026-09-17 核对的 structural-operation sources

所有者扩展 product boundary 后，这些 sources 只影响了单项机制。它们不授予修改 target
repository 的权限，也没有任何内容被复制进本 Skill。

### Cloudflare / `security-audit-skill`

- Source：<https://github.com/cloudflare/security-audit-skill>；观察时 `main` commit 为
  `c1c8a8c1471069fb0e188eeaff69b8e8db6564a8`。
- 概念上保留：consequential claim 应由 fresh challenge 尝试推翻；confirmed、unresolved
  与 rejected outcomes 必须分开；target-controlled execution 需要真实 host sandbox，
  不能靠 prompt language 冒充。
- 拒绝：security-specialist scope、默认 multi-agent panels、permanent ledgers，以及把其
  report schemas 变成本产品 requirement。
- 没有复制 Skill text、validator、schema、prompt 或 source code。

### Martin Fowler / Branch by Abstraction

- Source：<https://martinfowler.com/bliki/BranchByAbstraction.html>。
- 概念上保留：temporary coexistence 可以是 migration state；必须切换 actual caller；
  superseded supplier 与 temporary abstraction 在不再需要时应被删除。
- 拒绝：强制 facade、feature flag，或在 direct bounded cut 更安全简单时仍强制 gradual
  replacement。

### Git worktree documentation

- Source：<https://git-scm.com/docs/git-worktree>（观察于 2026-09-17）。
- 概念上保留：linked worktree 可以隔离 editable checkout，但仍链接同一个 repository，
  并共享 common Git state；因此把它当成 execution-security sandbox 是无依据推断。

### Alibaba / `open-code-review`

- Source：<https://github.com/alibaba/open-code-review>；观察时 `main` commit 为
  `f6f0f792eade540d0ae0145bc187e59201e43dfa`。
- 概念上比较：deterministic scope selection 与 explicit accounting 可以支持 bounded
  reviewer。
- 拒绝：code-review CLI dependency、automatic review/fix machinery，或在本
  repository-level product 内再造一套 orchestration engine。
- 没有复制 code、rules、templates 或 Skill text。

## Negative controls

产品拒绝 lens explosion、multi-agent audit panels、automatic worktree fixers、maturity
scoring、永久 target-repository audit backlogs，以及与当前 owner decision 无关的 broad
specialist scans。

## Independence boundary

Softpowers 提供了 review 与 verification 的 comparison baseline，但不拥有本产品。
Skill Field Lab 可以运行 controlled subject cases，但它只是 optional evaluation
infrastructure，不是 runtime dependency。
