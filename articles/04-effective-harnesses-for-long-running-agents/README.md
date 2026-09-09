# Effective harnesses for long-running agents

- 原文：<https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents>
- 研究主题：让 Agent 跨多个上下文窗口持续推进，而不是把“长任务”误当成一次超长对话。

## 小节

1. [长任务的两类典型失败](01-long-running-failure-modes.md)
2. [Initializer 是 Harness 启动策略](02-initializer-as-bootstrap.md)
3. [Durable Handoff：告诉下一轮还剩什么](03-durable-handoff.md)
4. [恢复必须回到 Ground Truth](04-recovery-and-ground-truth.md)
5. [Progress / Notes 是 Handoff Projection](05-progress-as-projection.md)

## 对平台架构的核心影响

- 长任务连续性不能依赖模型保留完整上下文。
- 初始化器、进度提醒、上下文重置属于 Harness 策略，而不是 Runtime 核心原语。
- 恢复时应从持久事实和真实环境重建状态，而不是盲信上一次 Agent 的总结。
- Handoff 的核心不是保存“思考过程”，而是保存剩余工作、已完成事实和恢复入口。