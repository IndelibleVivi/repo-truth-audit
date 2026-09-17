# v0.2.0 发布记录与流程

[English](release-preparation.md) · [发布说明](releases/v0.2.0.zh-CN.md)

状态：**COMPLETED — v0.2.0 PUBLISHED**

这是已经用于正式 [v0.2.0 Release](https://github.com/IndelibleVivi/repo-truth-audit/releases/tag/v0.2.0)
的维护者流程记录；它不授予安装或发布权限，也不会自动执行发布。未来 release 必须重新确认自身授权
和版本事实，并遵循 [AGENTS.md](../AGENTS.md)。

## 1. 固定并验证候选

使用真正的候选工作区，保留并发工作，记录 HEAD、分支、暂存区与工作区状态、声明载荷摘要。
不要通过重置把任意脏工作区伪装成干净候选。

```bash
pwd -P
git rev-parse --show-toplevel
git rev-parse HEAD
git status --short --branch
python3 scripts/validate_repository.py
python3 scripts/validate_architecture.py
python3 -m unittest discover -s tests -p 'test_*.py'
python3 scripts/selftest.py
python3 evals/operation-lab/run_operation_lab.py
git diff --check
```

宿主有系统 Skill 验证器时，先解析其真实路径再运行。工具缺失要记录为未观察边界，不能虚构 PASS。
回读候选提交的 CI，旧 CI 不能替新字节作证。原始本机路径和私有日志不进入公开文档。

身份与复制统一使用 `SKILL_PAYLOAD_FILES`。正常导入不能改变声明摘要，字节码不能进入安装暂存。
[forward 回执](forward-0.2.0-receipt.zh-CN.md) 记录了候选八文件摘要；运行时有变更，就先对齐身份，
再判断旧模型观察是否仍适用，不得改写历史摘要。仅修改载荷外文档时，验证文档即可，不声称新增模型实测。

## 2. 检查安装，再检查真实宿主使用

在已验证工作区中，先把真实安装器指向一次性 Skill 根目录。禁用 Python bytecode 写入，确保该命令只写
选中的临时安装目标：

```bash
preview_root=$(mktemp -d)
PYTHONDONTWRITEBYTECODE=1 python3 scripts/install_skill.py --dest "$preview_root"
```

核对实际文件集合、源码与安装摘要、安装回执。替换流程也先在一次性空间验证：旧副本保留为备份，
目标目录中的无关内容不受影响。临时目录不构成执行沙箱，也未必会被宿主发现。

所有者明确授权修改日常安装后，再使用真实宿主 Skill 根目录；已有副本通过
`scripts/install_skill.py --replace` 升级，检查备份与回执，不手工合并目录。
按宿主要求重启或重新加载，在一次性合成目标中开新任务：

- **Audit：**检查真正选中的产物，除明确要求的报告外不改目标。
- **Plan：**真正生成结构方案，对比起止目标字节和原有工作；仅回答请求分类不够。
- **Operate：**一次给出完整有限目标，检查实际调用者、状态效果、声明产物和必要退役。
  不逐步提示下一步，也不凭模型的完成宣称验收。

同时确认加载路径、身份与行为。评测答案不进入目标上下文。观察限制与所有者验收分别记录，
不要拿生产数据迁移当作安装冒烟测试。

## 3. 准备发布提交，避免提前宣称发布

上述步骤通过、所有者决定发布后，用经过审阅的提交准备版本元数据，不从脏工作区直接发版。

安装引用和 `PUBLIC_RELEASE_VERSION` 一起更新，同时协调确实受影响的双语 README、产品与版本状态、
current-state、changelog 和发布说明。现有仓库测试写死了旧稳定引用：需有意迁移到新发布契约，
保留引用不一致时失败的检查，不能删断言换绿色。历史 v0.1.0 文件和 tag 保留，不全仓替换旧版本字符串。

在 pre-publication 阶段，把新引用写作 **release target（发布目标）**，说明安装命令仅在发布后
可用，并与当时的已发布事实区分。本次 release 在 `PUBLIC_RELEASE_VERSION` 改为 `0.2.0` 后，
仍保留 `DRAFT — NOT PUBLISHED` 标记及其无条件 repository assertion；只有后续 public read-back
gate 通过后才迁移状态。Package `VERSION` 本身不能证明公开版本存在。

一并检查 GitHub About。建议描述：

> Evidence-led repository diagnosis and verified structural change for Codex.

仓库元数据修改属于需授权的外部写入，不是编辑本指南的附带动作。调用 slug 与许可保持不变。
重新验证并取得确切发布候选的 CI。

## 4. 得到真实授权后发布

遵循所有者认可的 Git／发布流程，将选定提交发布到远端、创建新的 annotated v0.2.0 tag，并创建对应
GitHub Release。tag 应解析到该提交，Release 应引用该 tag。不移动 v0.1.0；已经公开的 tag 出问题时，
不能悄悄重定向来“修复”。

本页没有创建 tag、改变远端引用或发布 Release 的命令。阅读本页不会授予执行权限。

发布后，回读公开仓库与默认分支、tag 指向、Release 状态和 CI，再从公开 tag 安装到一次性目录，
核对声明载荷与测试候选一致，确认 README、许可和 Skill 路径公开可读。仅有 API 成功响应不够。

只有完成上述发布与回读 gate 后，status-only commit 才可把 release-note draft marker 改为已观察到的
published 状态，并迁移对应 repository assertion；该 test change 不得提前进入 pre-publication candidate。

状态文档只填写实际观察到的事实。后续状态提交可以推进 main，无需移动已经发布的 tag。
待完成或失败的步骤继续如实保留。公开安装成功不等于宿主已激活，合成测试也不能泛化为生产能力。

## 完成记录

- Release／tag commit：`5d25c581a7d331329d39be9f6bace11371dd4437`。
- Annotated tag object：`8c739ea505066662c60e7afa994ee2948b2fea64`。
- Release-commit CI：[run `35240303414`](https://github.com/IndelibleVivi/repo-truth-audit/actions/runs/35240303414)，四项 jobs 全部通过。
- 正式 Release：[v0.2.0](https://github.com/IndelibleVivi/repo-truth-audit/releases/tag/v0.2.0)，回读为 latest、non-draft、non-prerelease。
- Declared／public-tag install digest：`80863c9796a2364d99f43cd81d6f53c8d6059f0c303061d18362ba683411a29f`，恰好八个文件且无 undeclared entry。
- Host gate：日常副本 transactional upgrade 并保留 backup；随后在 synthetic target 上新开
  Audit、Plan 与 one-request Operate task。这不证明其他用户今后的 discovery，也不证明通用生产重构。
