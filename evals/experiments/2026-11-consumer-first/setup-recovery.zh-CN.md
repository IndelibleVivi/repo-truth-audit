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

## Harness 写入范围修正

修正批 harness 把仅供 clean 任务使用的“保留全部产品字节”条件，也附在实现任务中。
两个返回报告明确引用此冲突，把实现做成了审计。这是 harness 错误，不是模型修复失败。
协调者在八次启动后停止该批，确认无原生 writer 遗留，四个槽位从未启动。所有原始状态及
输出保留。取消留下两个陈旧 running 标签，shutdown 依据为独立 process read-back。

[最后四会话预注册](final-four-preregistration.json) 只使用 24 会话总上限内的剩余四次，
明确授予 Task 所要求的实现权限。覆盖迁移的 full-RTA/短指令配对及局部修复的无 RTA/短
指令配对，仍每次 180 秒、不重试。这是缩小的 scope-corrected 工程 probe，原四任务×三组
均衡设计没有完成。披露此前 setup 知识，不作盲测或因果声称。

## 已关闭的接续

全部 24 个被试会话已使用。最后两个普通修复完成；两个 migration 产品通过 consumer
检查，却未在 deadline 前完成必需报告，因此完整 Task 结果为失败。v2 两个 clean 控制
在报告前中断，保留 unjudged。原生计量及限制见[分批结果](results.zh-CN.md)。
此带日期记录保留先前登记，不授权重启或延长调用。
