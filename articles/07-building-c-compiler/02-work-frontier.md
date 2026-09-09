# Work Frontier：Multi-Agent 的真正调度对象

## 文章中的关键观点

编译器团队中的 Agent 会不断发现新的失败、缺失功能和可并行工作，并自主领取任务。有效并行度取决于当前是否存在足够多可独立推进的工作项。

## 我们的架构分析

可以把当前所有**独立、可领取、可验证**的工作项称为 Work Frontier：

```text
Work
├── 已完成
├── 被占用
├── 被阻塞
└── Frontier
    ├── Work Item A
    ├── Work Item B
    └── Work Item C
```

于是：

> **Effective Parallelism ≈ Independent Work Fronts。**

如果只有一个关键阻塞点，即使允许启动 100 个 Agent，也没有 100 倍并行度。

这修正了“Agent Scheduler”的思路：

```text
错误重点：现在还能启动几个 Agent？
正确重点：现在有哪些值得独立领取的 Work Item？
```

## 对 Agent Platform 的影响

Multi-Agent orchestration 需要 Work Discovery、Ownership / Lease、Dependency、Status 和 Verification。Agent 数量只是调度结果。

## 核心结论

> **Multi-Agent 的关键不是 Agent Scheduler，而是 Work Scheduler；真正可扩展的是 Work Frontier。**