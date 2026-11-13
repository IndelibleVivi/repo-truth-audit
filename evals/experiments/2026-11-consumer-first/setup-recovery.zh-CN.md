# Setup 修正与保留的首批会话

[English](setup-recovery.md)

首批使用冻结 commit `03e37060f5da720aa318d9021c03a73809fe5404`。未读取 campaign
数据的独立 review 复现三处问题：isolated Python 移除了应用自己的 import 目录，误拒
合法已打包 helper；文本换行归一化放过 owner 文件 LF→CRLF 字节变化；两份生成的 range
self-test 引用 `os.environ` 却未 import os。

十一项实验测试及 169 项仓库测试此前全通过，但没有覆盖这些保证。正常 helper import、
精确字节比较及运行所附 self-test 的反例由独立复核确认。

协调者在读取最终报告或产品结果前，因 setup 有效性停止该批。成功停止时十二槽位均已启动：
九个 host 进程 finished、一个 timed-out、两个 interrupted。这是宿主状态，不是任务成败。
[中止回执](aborted-observations.json) 保留十二项 unjudged，不计算可比成本。原 subjects、
输入、报告、日志及独立复现保存在 Git 外，未覆盖，不据此推断 Agent 成功率。

修正后的 consumer 保留 -I，仅插入 selected entry 的父目录以支持本地 imports。
Task/owner/Cedar 受保护输入改为逐字节比较，两份所附测试补齐依赖。十四项 focused tests
与独立前后复验接受合法单文件/helper bundle，拒绝 CRLF owner 修改，并成功执行两份 fresh
所附测试。

独立的[修正批预注册](recovery-preregistration.json) 使用新 seed
`consumer-first-2026-11-14-setup-repair-v2`、修正后的 fresh objects 与相同三组处理。
[修正批设置](recovery-execution-settings.json) 冻结其输入与判据。最多十二个新 Agent 会话，
每次 180 秒、三并发、不重试；两批合计最多 24 个被试会话。沿用原生 ChatGPT 登录，不启用
新付费凭据。一个 Agent 会话可以含多次模型 API 请求。

新批登记前只读过旧批 host 状态，没有读最终报告或产品判定；独立 reviewer 未接触 campaign。
这是初始对象不同的 setup 修正，两批不得混池。人工审阅仍自愿且未计时；更可靠的仪器和
绿测不能推导生产率增益。
