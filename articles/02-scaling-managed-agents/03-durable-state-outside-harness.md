# 持久状态不能依赖 Harness 进程

## 文章中的关键观点

Managed Agents 需要跨时间运行，Harness 可能因为升级、重启或上下文变化而重新创建，因此长期状态不能只存在 Harness 内存中。

## 我们的架构分析

如果事实状态依赖 Harness 进程：

```text
Harness crash
→ state lost
→ 无法恢复
```

那么平台就无法真正支持长任务。

更合理的是：

```text
Harness
  ↓ append / read
Durable Session State
  ↓ recover
New Harness
```

Harness 可以持有临时推理状态，但真正影响恢复、审计和后续执行的事实必须落到运行时管理的持久层。

## 对 Agent Platform 的影响

Session 开始成为运行时的一等实体。Harness 的生命周期可以短于 Session，甚至每次触发都重新实例化。

这也为后续 Event Log、State Projection 和 Recovery 奠定了基础。

## 核心结论

> **Durable state 必须独立于 Harness 生命周期；Harness 可以被重启，执行历史不能因此消失。**