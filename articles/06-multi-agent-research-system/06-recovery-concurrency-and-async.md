# 恢复、并发与异步委托

## 文章中的关键观点

Multi-Agent 系统中 Sub-agent 可能失败，Lead Agent 需要处理超时、错误和部分结果，同时多个 Sub-agent 和 Tool Call 会并行运行。

## 我们的架构分析

### Local Recovery + Global Reconciliation

Child 失败时优先局部重试或恢复；Parent 不必立刻重跑所有任务。但 Child 状态变化后，Lead 必须重新评估全局计划。

```text
Child Failure
   ↓
Local Recovery
   ↓
Result / Failure State
   ↓
Global Reconciliation
```

### 两层并发

```text
Delegation Concurrency
→ 多个 Agent 同时工作

Action Concurrency
→ 单个 Agent 内多个 Tool / Action 并发
```

两层预算和背压策略不能混成一个 `max_concurrency`。

### Async Delegation

长任务中的委托应被建模为持久关系，而不是必须阻塞 Parent 线程等待 Child 返回。

## 对 Agent Platform 的影响

需要持久 Delegation 状态、事件驱动回传、局部 Recovery、Parent Reconciliation，以及分层并发预算。

## 核心结论

> **Multi-Agent 的可靠性来自局部恢复 + 全局协调；并发也必须区分 Agent 层和 Action 层。**