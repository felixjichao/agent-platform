# Context 是持久事实的投影

## 文章中的关键观点

Agent 在多轮执行中不断产生新的消息、工具结果和外部数据，需要持续维护当前上下文，而不是仅依赖一次性 Prompt。

## 我们的架构分析

这进一步要求区分：

```text
Session
→ 持久历史 / 事实来源

State
→ 当前执行状态的视图

Context
→ 给当前模型调用的工作集投影
```

所以：

> **Session != Chat History != Context Window。**

Context 可以被重建：

```text
Session / State / Memory / Notes / Workspace / Artifacts
                     ↓
               Context Builder
                     ↓
                  Context
```

如果 Context 丢失，应该能够从持久来源重新生成，而不是把“当前 prompt 字符串”当成系统唯一事实。

## 对 Agent Platform 的影响

需要显式引入 Context Builder 或等价策略接口。它负责从多个来源选择、排序、压缩和加载信息。

Context Builder 属于 Harness / Context Strategy，而不是 Session 本身。

## 核心结论

> **Context 是持久状态的一次查询与投影；它应该可重建，而不是成为 Source of Truth。**