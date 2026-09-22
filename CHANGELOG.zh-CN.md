# Changelog

[English](CHANGELOG.md)

## 0.3.0 — Unreleased

- 从限定范围的规格、决策和开发对话还原已接受产品意图，保留用户/任务、完整流程、约束、
  非目标、理由、替代关系与明确延期。
- 双向追踪意图到所选行为、现有责任到用途；区分缺失/局部流程、偏移、陈旧声称、无合理用途
  的堆积，以及合理演进、兼容需要和证据缺口。
- 将产品意图收敛接入 Audit / Plan / Operate 与 B/S/D/U 验收；限定对话读取范围，保留授权边界。
- 增加渐进加载的意图方法、合成场景、聚焦 evaluator 检查与同步的双语产品/使用/架构说明。
- 当前是 source candidate，稳定安装仍固定到 v0.2.1。

## 0.2.1 — 2026-09-20

- 按当前任务缺口、前置条件和完成义务判断辅助方法是否适用；尊重宿主、用户和项目的实际规则，
  不自动继承可选流程中的覆盖率、RED 或 commit 门槛。
- 区分绿色行为基线、缺陷 witness、可直接检查的退役与可执行 gate 反例。允许有依据的长期
  回归测试及过时测试退役，同时保留受支持行为的保护。
- 澄清获授权 dirty 清理可以修改、退役实现，同时保留无关工作及可恢复的 before-image。
- 在 Usefulness 中考虑保留的测试、配置与接缝成本；受到质疑时按约定阶段和真实证据复核。
  没有新增净减行配额、逐项测试审批或全局最低成本证明要求。
- 在既有 operation lab 中加入六个合成 Git 对照对象、六项夹具/反例测试和受控 forward
  评测协议。夹具及 CI 成功不证明模型行为；独立的有限
  [forward 检查](docs/forward-0.2.1-receipt.zh-CN.md) 已通过，不证明优于 0.2.0。Issue #4 提供现场
  动机，不能被当作已确认的清理失败或另一 Skill 造成问题的因果证明。
- 保持八文件安装载荷和模式路由；发布 v0.2.1 安装 pin 及双语发布文档。发布准备
  未在已验收的行为细化之外继续修改 runtime bytes。
- 包含 v0.2.0 后合入的 Windows 测试可移植性修复；不扩大原生 Windows operator 支持声明。

## 0.2.0 — 2026-09-17

- 在完整 README Mermaid topology 之前加入成对、day-first 的 English 与简体中文 SVG
  reader map，两种视图均默认可见；把 B/S/D/U 解释为四个普通 completion questions，并为新 overview artifacts
  加入 accessibility、safety、embed-order 与 locale-parity validation。
- 为 validation、hashing、staging、installed comparison 与 receipt 定义一份精确的
  eight-file Skill payload。Runtime bytecode/cache residue 不再改变或进入 install；
  undeclared source/executable file 会 fail closed，installer regression 也会对比 clean 与
  post-import payload。
- 将原始 `0.2.0` forward directory digest 对账到一个被复制的 `.pyc` residue file，保留
  历史 receipt 而不改写旧事实；随后新增 clean-payload forward evidence，覆盖一次真正
  mutation-free Plan 与一次 single-request whole-goal Operate，并独立验收 B/S/D/U。
- 将 `0.2.0` source candidate 从 read-only audit 扩展为一套 progressive
  Audit / Plan / Operate 产品：Audit 继续默认只读，Plan 不修改目标，Operate 只有在显式、
  有限的 implementation request 与匹配 effect authority 存在时才写入。
- 把 runtime 拆为精简 router 与 progressive Audit、Operation、Recovery references；加入
  verified checkpoint 与 whole-goal completion 的区分、Behavior/Structure/Delivery/
  Usefulness 验收，以及诚实的 Complete / Checkpoint / Blocked / Recovered terminal states。
- 加入可选 POSIX cited-byte continuity helper；unsupported host fail closed，并明确不声称
  semantic、Git-snapshot、atomicity 或 authorization proof。
- 加入 16 项 deterministic operation-lab tests，覆盖 two-increment synthetic refactor、
  selected delivery artifact、facade/unused/stale false completion、重复 state effect、
  drift、selective recovery、无关 owner work 保留与 formatter-only usefulness probe。
  Lab 不调用 target model，也不冒充 forward model evidence。
- 加入独立的 public-safe `0.2.0` forward receipt，记录 focused routing、fresh read-only
  Audit regression 与真实模型在同一 session 中完成的 two-increment Operate run，并在
  checkpoint 与 whole-goal B/S/D/U boundaries 由主线程独立验收。
- 加入双语 Audit / Plan / Operate mode controls 与 public contract 更新；将 source `VERSION`
  (`0.2.0`) 与 immutable public `v0.1.0` release identity 解耦。
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
- 将 renderer-neutral model 扩展为七个 region、31 个 stable nodes 与 46 条 semantic
  edges；保留原 audit topology，并加入可见 Plan exit、implementation gate、checkpoint/
  recovery loop、B/S/D/U whole-goal acceptance 与 external-proof boundary。
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
