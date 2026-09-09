# Goal-driven Dynamic Team Formation

## 文章中的关键观点

Research 系统不是让用户先手工定义固定 Agent Team，而是由 Lead Agent 根据研究问题动态创建适合的 Sub-agent。

## 我们的架构分析

这可以进一步抽象成：

```text
Goal
+ Available Capabilities
+ Knowledge
+ Permissions
+ Budget
+ Risk
        ↓
Harness / Orchestrator
        ↓
Execution Strategy
        ↓
Single Agent / Workflow / Multi-Agent / Hybrid
```

如果选择 Multi-Agent，再动态形成：

- Agent 数量；
- 角色；
- 子目标；
- 并行度；
- 汇总方式。

因此：

> **Agent Team 本身可以是 Runtime Output。**

固定 Team Builder 更适合显式业务流程，不应该成为平台唯一模式。

## 对 Agent Platform 的影响

平台需要 Capability Discovery、Budget、Policy 和 Delegation 等基础能力，Harness 才能在运行时形成团队。

## 核心结论

> **默认应从 Goal 出发动态形成执行结构，而不是要求用户预先设计 Agent 拓扑。**