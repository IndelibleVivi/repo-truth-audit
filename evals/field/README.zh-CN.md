# 真实消费者探针

[English](README.md)

这些可选探针在一次性副本中执行固定版本的公共项目，不调用目标模型，也不进入普通仓库 CI。
输入须显式准备；探针不会克隆、联系上游维护者或修改被观察仓库和全局环境。
sampleproject probe 只在一次性 virtual environment 内，用显式准备的离线输入构建和安装。
它们属于评价材料，必须留在目标 Agent 的工作区之外。
输出回执须位于被观察 source/package 目录外；probe 会拒绝覆盖输入的目标。
Python helper 使用仓库要求的 Python 3.10+ 语法；原始一轮实际执行于 3.12.14。
后续带日期的观察分别记录自己的 interpreter 版本。

## Python：真实子进程继承的配置

使用已有且提供 Click 的 Python 环境。记录中的观察环境为 Python 3.12.14、Click 8.4.2。
源码 checkout 必须包含下述两个固定 commit；只修改临时 archive。

```sh
git clone https://github.com/theskumar/python-dotenv.git /path/to/python-dotenv
python3 evals/field/probe_dotenv.py --repo /path/to/python-dotenv --output /path/to/dotenv.json
```

历史任务来自 [issue #697](https://github.com/theskumar/python-dotenv/issues/697)
和[修复 #698](https://github.com/theskumar/python-dotenv/pull/698)。
`a00cb2eed0704cd6d2071b2004c37e95ccc86ee5` 是修复前状态，
`e0310e5bb3f2b701b11bbc007ca0c82c1bd56f38` 是上游修复。
执行入口为 `python -m dotenv`，由真实子进程报告最终环境。
探针覆盖保留已有值、保留空值和有效 override 模式，并加入改错层次、过宽改动、
传播不完整与误导 README 的控制；已存在的 API 是正例。
19 个进程可以全部正常退出，同时产生不同的语义结果。
这建立源码入口证据；wheel 和用户安装的 console script 尚未在此检验。

## TypeScript：发布声明与实际运行时

```sh
git clone https://github.com/developit/mitt.git /path/to/mitt
git -C /path/to/mitt checkout 6b41670516ed8e8b738612f60491995470aa63b3
npm install --ignore-scripts --no-audit --no-fund --prefix /path/to/mitt-consumer mitt@3.0.1 typescript@4.9.5
python3 evals/field/probe_mitt.py --source /path/to/mitt --consumer-seed /path/to/mitt-consumer --output /path/to/mitt.json
```

任务是移除通配订阅者，同时保留具名订阅者。
真实包的声明阻挡了运行时支持的单参数操作。
控制案例会拒绝仅修改源码的修复、过宽类型合同，以及同时删除具名订阅者的运行时改动。
源码检查与消费者检查有意选择不同入口。
维护者对语义的说明见 [issue #150](https://github.com/developit/mitt/issues/150#issuecomment-1024417195)
与 [issue #70](https://github.com/developit/mitt/issues/70#issuecomment-361379190)。

source-only 变体从固定 git show 字节读取，避免工作树改动被错误归因于 commit。
记录实际 package 版本、声明 hash 与编译器观察。

## Go：所选环境变量到结构体路径

准备符合固定 module Go 1.23 要求的真实编译器。依赖准备是明确的独立操作；Python probe
会禁止 Go proxy 查找和自动 toolchain 下载。使用已有 module cache，或在离线观察前通过正常
Go 工具准备：

```sh
git clone https://github.com/spf13/viper.git /path/to/viper
git -C /path/to/viper checkout 528f7416c4b56a4948673984b190bf8713f0c3c4
/path/to/go/bin/go version
/path/to/go/bin/go -C /path/to/viper mod download
python3 evals/field/probe_viper.py --repo /path/to/viper --go /path/to/go/bin/go \
  --output /path/to/viper-observation.json
```

module-cache 可指定另备的模块缓存；build-cache 可指定仓库外的编译缓存，默认编译缓存为
一次性目录。viper_consumer.go 与 wrapper 放在一起。本轮使用 Linux Go 1.27.4，实际编译
消费者并核对 module replacement 选择固定源码，未独立检验某个已安装发布包。

七个变体/十二次读取比较默认 AutomaticEnv、key binding、登记 default key、显式实验 struct
模式、陈旧快照假修复及两种合法空值策略。API 成功还须核对实际解码值。本例在候选 Skill 冻结后
选择，没有因此新增运行规则。见 [issue #761](https://github.com/spf13/viper/issues/761)
和 [v1.18.2 兼容说明](https://github.com/spf13/viper/releases)。

wrapper 分开记录编译与运行：observed 退出0，expectation-mismatch 退出1，setup-blocked
退出2。缺少缓存依赖不构成 Viper 缺陷。Go 模块环境选项不提供 OS 网络隔离。

## Node/ACP：最终结果之前的进展

CWR 使用所有者公开仓库、真实固定 acpx@0.15.1 runtime 与合成 ACP server。当前测试在
final 暂不返回时，由第二个 CLI 读取持久活动：

```sh
git clone https://github.com/IndelibleVivi/codex-worker-routing.git /path/to/cwr
git -C /path/to/cwr checkout 18774c0628789b554db10e01189a367a21aad7fb
cd /path/to/cwr/integrations/acpx
npm ci --ignore-scripts --no-audit --no-fund
node --test --test-name-pattern='REAL activity:' test/real-acpx.integration.mjs
node --test --test-name-pattern='prompt with no events|live status requires|live phase distinguishes|ended observation stream' test/cli.test.mjs
```

旧源码对照在独立临时 checkout 提取 efc9613769960577f148c8e457a41f8c9e4ca234，
从当前 integrations/acpx 树复制 test/real-acpx.integration.mjs、test/helpers.mjs、
test/fixture-acp-agent.mjs，使用同一依赖树，执行相同 held-final 命令。旧源码失败，当前通过。
这里有意把当前测试复制到旧源码，不声称旧树当年已经包含该回归。

已观察 Linux 生产方→持久活动→status CLI，Windows/OpenCode 显示属于另一个未观察消费者
边界。旧序列为零、旧日志不存在，不能否定新状态路径。见[完整机制说明](../../docs/user-outcomes-study.zh-CN.md)。

这些机制经过有意挑选。上游修复和构造变体属于评价证据，不能用来估计自然模型输出或普遍失败频率。
临时目录为已检查的代码模拟交付边界，并不提供对抗恶意代码的隔离。

## Python：实际选中的安装包（预先声明的构造实验）

执行之前选定公共 `pypa/sampleproject` 的
`621e4974ca25ce531773def586ba3ed8e736b3fc`。已检查 backend 为
`setuptools.build_meta`，build requirement 为 setuptools。这是构造的交付实验，
不是上游 bug 报告，也不是 Skill 收益的盲测。具体消费者从所选 venv 导入
`sample.simple.add_one(10)`。预期读取：初始 wheel 11；有意只改 source 为 +2 后，
source 为 12、wheel 消费者仍为 11；重建并重装后 wheel 为 12；原生 pip editable
安装为 12；之后 owner 将 source 改为 +3，editable 为 13，regular wheel 合法保留
12，直到显式重建交付 13。不得仅凭 source 变化将冻结 wheel 判为缺陷。
实际 module origin 与 PEP 610 direct_url metadata 必须建立选择关系；PYTHONPATH
checkout shim 不能充当 editable 安装证据。

wrapper 只在一次性副本使用精确 Git pin 字节，显式联网准备 seed 后才执行离线
wheel/editable 操作，记录实际 Python/build-tool 版本。在写入前拒绝 output/source/seed
重叠（含 symlink）。setup failure 与语义不匹配分开。此可选外部执行不进入普通 CI，
不调用模型，不预设 canonical Skill 需要改变。

通过显式准备的开发 seed 复现（只有以下准备命令联网；使用被观察 checkout 外的一次性路径）：

```sh
git clone https://github.com/pypa/sampleproject.git /path/to/sampleproject
git -C /path/to/sampleproject checkout 621e4974ca25ce531773def586ba3ed8e736b3fc
uv venv --python python3 /path/to/seed
uv pip install --python /path/to/seed/bin/python pip==26.3 setuptools==84.2.1 wheel==0.48.0 packaging==26.3 peppercorn==0.6
/path/to/seed/bin/python -m pip download --dest /path/to/seed/wheelhouse pip==26.3 setuptools==84.2.1 wheel==0.48.0 packaging==26.3 peppercorn==0.6
python3 evals/field/probe_sampleproject.py --source /path/to/sampleproject \
  --seed /path/to/seed --output /path/to/observation.json
python3 -m unittest discover -s tests -p test_sampleproject_probe.py
```

probe 创建不带 pip 的 stdlib venv，通过 seed 的原生 pip --python 安装缓存的 build tools
和真实 runtime dependency peppercorn。使用已检查的 backend 构建真实 wheel，并执行
原生 pip editable 安装。project 的安装/构建命令禁用依赖获取与 build isolation；target
venv 的依赖准备只从 seed 本地 wheelhouse 选取。移除 PYTHONPATH。source-only control
显式插入一次性源码路径；editable readings 使用 isolated Python，没有此插入。
这些 pip 限制不提供 OS 网络隔离，已检查的 backend 仍执行受信任公共代码。
成功回执替换临时路径；失败诊断可能含本机路径，因此 raw receipt 保持私有。
source/seed snapshot 比较文件名、大小、mtime 与 symlink target，属于写入检测证据，
不声称建立 cryptographic identity。

2026-11-14 实测 Python 3.13.5、pip 26.3、setuptools 84.2.1、wheel 0.48.0、
packaging 26.3、peppercorn 0.6：八次读取全部符合预声明序列
**11 / 12 / 11 / 12 / 12 / 13 / 12 / 13**，22 个 subprocess 全部成功，source/seed 文件名、大小、mtime 与 link target 均未改变。两种安装模式通过 module origin 与 direct_url metadata
建立选择证据。九个离线测试覆盖值/origin/metadata 拒绝、合法冻结 wheel 邻例、
symlink/重叠保护、输入写入检测，以及已就绪 consumer 非零退出/非法 JSON 判为 mismatch、保留 portable setup-command 证据与不同失败状态（observed 0、expectation-mismatch 1、
setup-blocked 2）。仅检验所选函数和交付序列；console script、其他 Python/tool 版本、
自然发生的 agent 错误及 Skill 收益仍未测量。没有修改上游或 canonical Skill。
