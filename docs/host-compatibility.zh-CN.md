# 宿主兼容与实际采用证据

[English](host-compatibility.md)

核对日期：2026-11-13。本页分别记录包格式可移植性、安装字节、宿主选择和任务行为。
发布状态见[当前状态](current-state.zh-CN.md)，发现问题的排查方法见
[使用指南](usage.zh-CN.md#安装与发现)。公开 `v0.3.0` 标签与未发布源码仍是独立的安装选择。

## 本轮已建立的证据

| 层次 | 本轮证据 | 范围限制 |
| --- | --- | --- |
| 标准文本包 | YAML frontmatter、`SKILL.md`、相对引用和脚本采用 [Agent Skills 格式](https://agentskills.io/specification)。 | 格式兼容本身不能证明宿主激活或执行。 |
| 精确载荷 | 源码验证、摘要、暂存和安装比对共用 [`scripts/common.py`](../scripts/common.py) 中的九文件定义。 | 目录匹配证明该目录的字节；宿主可能选中另一份目录。 |
| 本地安装器 | 新的临时安装与 candidate 九文件摘要一致，收据正确记录 dirty 源码；仓库测试另覆盖 [`scripts/install_skill.py`](../scripts/install_skill.py) 的替换与载荷身份。 | 默认目标为 `$CODEX_HOME/skills` 或 `~/.codex/skills`；`--dest` 不会向宿主注册目录。 |
| 原生研究 Agent | 本研究会话中的全新 Agent 被明确要求读取固定的 candidate 快照；无 Skill 组收到相同产品任务。 | 这验证显式加载。后端模型标识、token 计数和自动发现不可观测。 |
| 本地 Codex CLI | 环境存在 `codex-cli 0.167.0-alpha.4`。最小探针在初始化进程内 app-server client 时因 `Read-only file system (os error 30)` 失败。 | 该探针未建立目标模型执行或 Skill 选择证据；记录为环境初始化失败。 |
| 其他原生宿主 | 已核对 Claude Code、Gemini CLI 与 OpenCode 的官方发现、激活文档。 | 本轮未在这些宿主中进行原生任务实跑。 |
| 可选 Field Lab | 下文固定源码上的显式 v1→v2 迁移、v2 验证和全部六个确定性 self-test 通过；目标调用为零。 | 这验证迁移与 fixture oracle；未建立 live adapter 行为或 Skill 选择证据。 |

自然试验 candidate 的载荷摘要为
`28b73009402e0f149c7078379a15d51cf88468c66ec092f49a59a5f6926fb211`。
它标识该次被测快照。后续源码变更必须重新计算摘要；版本字符串无法独立标识未发布行为。

载荷包含 `LICENSE.txt`、`NOTICE.md`、`SKILL.md`、`agents/openai.yaml`、
`references/audit.md`、`references/intent.md`、`references/operation.md`、
`references/recovery.md` 和 `scripts/check_evidence.py`。
评价 fixture、预期答案、模型 runner 与试验比较工具均不进入载荷。
OpenAI interface 文件属于宿主元数据；实际方法位于 Markdown 包中，不依赖额外的 provider
服务或宿主专用协调器。

## 官方文档中的宿主入口

以下是按上述日期核对的本地验证起点。实际安装的宿主版本与覆盖配置仍须检查。

| 宿主 | 文档中的位置或入口 | 新任务中的验证 |
| --- | --- | --- |
| [Codex](https://learn.chatgpt.com/docs/build-skills) | 当前文档列出仓库 `.agents/skills/` 与用户 `~/.agents/skills/` 发现位置。 | 使用 `/skills` 或显式调用 `$repository-operational-truth-audit`；检查选中文件，变更未出现时重启。 |
| [Claude Code](https://code.claude.com/docs/en/skills) | 项目内 `.claude/skills/<name>/SKILL.md`，或个人目录 `~/.claude/skills/<name>/SKILL.md`。 | 调用 `/repository-operational-truth-audit`；检查实际选中的目录和引用文件读取。 |
| [Gemini CLI](https://geminicli.com/docs/cli/skills/) | 工作区 `.gemini/skills/` 或 `.agents/skills/`；也有相应的用户级位置。 | 查看 `/skills list`，必要时执行 `/skills reload`，再请求使用具名 Skill 并观察激活。 |
| [OpenCode](https://opencode.ai/docs/skills/) | 项目内 `.opencode/skills/`；文档中的兼容根目录包括 `.claude/skills/` 与 `.agents/skills/`。 | 提及 `@repository-operational-truth-audit`；检查选中的基目录。支持文件仍需单独读取。 |

当前 Codex 文档位置与本仓库安装器保留的默认目标存在差异。
针对文档中的当前宿主，可显式选择
`--dest /path/to/disposable-product/.agents/skills`，随后验证发现。
本轮未建立特定 Codex 构建是否也读取旧根目录的证据。
[旧 OpenAI catalog](https://github.com/openai/skills) 现已标记 deprecated 并指向当前指南；
其历史安装方式无法代替当前宿主观察。

同名副本可能改变最终选择。调查优先级前，先保留实际选中路径的证据；不要凭猜测删除副本。
显式调用、工具轨迹中提及路径以及实际应用方法是不同观察。按宿主实际暴露的信息记录。

## 最小可复现本地烟测

在选定的 RTA 源码 checkout 中执行包验证。以下命令只建立临时包，保留日常安装：

```bash
git rev-parse HEAD
git status --short --branch
python3 scripts/validate_repository.py
rta_preview_root=$(mktemp -d)
python3 scripts/install_skill.py --dest "$rta_preview_root"
python3 - "$rta_preview_root/repository-operational-truth-audit" <<'PY'
import sys
from pathlib import Path
sys.path.insert(0, "scripts")
from common import SKILL_DIR, SKILL_PAYLOAD_FILES, directory_digest, payload_matches
target = Path(sys.argv[1])
assert payload_matches(SKILL_DIR, target)
print("files:", len(SKILL_PAYLOAD_FILES))
print("selected payload:", directory_digest(target, SKILL_PAYLOAD_FILES))
PY
```

测试宿主时，另建一次性产品目录，只复制
`evals/cases/source-artifact-split/fixture/` 的内容。
使用 `install_skill.py --dest /path/to/disposable-product/<host-skill-root>`，
把同一份声明载荷放入该宿主文档支持的项目级 Skill 根目录。
`expected/` 留在受试目录外，并保留宿主正常的信任与执行控制。
临时副本不构成运行不可信代码的操作系统隔离。

启动新任务，使用上表的显式调用方式并提出：

> 判断这个仓库是否已适合作为打包 CLI 交给操作者。沿实际 distribution selector
> 检查现有绿测究竟证明了什么。除 `AUDIT.md` 外保持只读。说明选中了哪个 Skill 文件，
> 以及能够观察到哪些执行边界。

独立复核者随后对照 fixture 和实际选中的产物检查报告。
成功的审计应保留产品文件、到达声明的消费者，并准确界定源码绿测的证明范围。
如果没有宿主轨迹支持，Agent 声称已加载 Skill 的文字保留为自报。
只有在研究发现机制时，才单独测试隐式激活。
一次显式烟测无法建立 Audit / Plan / Operate 全覆盖、接续可靠性或生产率增益。

简短收据应保留：宿主和操作系统版本、可获得时的请求模型与实际模型标识、源码 commit
与 dirty 状态、载荷摘要、选中路径、prompt 和 subject 身份、执行结果、受保护文件变化及限制。
不可获得的计数应标为不可获得。这是有界的兼容检验，无须成为每个目标仓库的常设流程。

## 可选的 Field Lab v2 路径

本次观察使用 Skill Field Lab `0.2.1`，源码为
[`6f79c5717da8bc0639fa0d70f5d82b64c231b9c5`](https://github.com/IndelibleVivi/skill-field-lab/tree/6f79c5717da8bc0639fa0d70f5d82b64c231b9c5)。
它的正常命令接受 v2 manifest；显式离线迁移器可读取 RTA 的 legacy
[`fieldlab-pack.json`](../fieldlab-pack.json)。
[迁移指南](https://github.com/IndelibleVivi/skill-field-lab/blob/6f79c5717da8bc0639fa0d70f5d82b64c231b9c5/docs/MIGRATION_V1_TO_V2.md)
规定前置条件与收据。

从该 Field Lab 源码 checkout 执行，输出父目录应位于 RTA checkout 外，且尚不存在：

```bash
python3 -m fieldlab migrate-v1 /path/to/repo-truth-audit/fieldlab-pack.json \
  --output /path/to/new-rta-lab/fieldlab.json
python3 -m fieldlab validate /path/to/new-rta-lab/fieldlab.json
python3 -m fieldlab selftest /path/to/new-rta-lab/fieldlab.json
```

本次迁移保留一个 subject 和六个 case，未改动源 manifest，记录
`semantic_change: false`，目标 Agent 调用为零。源 manifest 的 SHA-256 为
`fd578f58abffb88a847beb7f2e1dbdf568832e14415cbf66c4a97f5c8c82b9db`。
生成的工作区快照属于带日期的实验输入；canonical Skill 后续改动不会自动进入其中。
保存迁移收据，在检验变更源码时明确创建新快照。

本轮观察覆盖迁移、`validate` 与 `selftest`。
Field Lab 的 live run 另有 plan、adapter、执行与调用上限要求，本轮未使用。
RTA 不因此增加 Field Lab 运行时依赖、第二份 canonical Skill 或隐式模型调用验证步骤。
