# Agent Work Environment

## 文章中的关键观点

编译器实验依赖的不只是模型和 Harness，还包括 Git、工作副本、测试、编译器反馈、任务发现和共享代码状态。环境质量直接决定 Agent 能否高效工作。

## 我们的架构分析

此前的 Execution Environment 主要回答“Agent 能在哪里行动”。现在需要升级为更丰富的 **Agent Work Environment**：

```text
Agent Work Environment
├── Shared Resources
├── Local Workspace
├── Work Discovery
├── Ownership / Lease
├── Observation
├── Verification
├── Feedback / Oracle
└── Artifacts / Progress
```

它不仅执行动作，还要把复杂的原始世界转换成高信号 Observation。

例如编译失败不是简单返回 20MB 日志，而应该尽量提供：

- 哪个目标失败；
- 错误位置；
- 最小诊断上下文；
- 可继续验证的入口。

这属于 Environment Engineering。

## 对 Agent Platform 的影响

L2 不再只是 Sandbox / Tool 容器，而应承载长期 Work 的可操作世界。Workspace 也从 Session 附属文件夹提升为 Work 的持久状态载体。

## 核心结论

> **生产级 Agent 需要 Work Environment，而不仅是 Execution Sandbox；环境必须同时支持工作发现、行动、观测和验证。**