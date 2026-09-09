# Sub-agent 的核心价值是上下文隔离

## 文章中的关键观点

文章讨论了通过子智能体处理独立任务，把大量局部信息留在子智能体上下文中，只把必要结果返回给主智能体。

## 我们的架构分析

Sub-agent 的价值不能只理解成“多一个模型增加智能”。它更重要的作用是：

> **Context Isolation / Context Offloading。**

例如研究任务：

```text
Parent Context
   │ delegate
   ├── Child A：论文组 A
   ├── Child B：论文组 B
   └── Child C：论文组 C

Child 返回 findings / evidence refs
而不是全部原始历史
```

需要进一步区分两种调用：

### Agent-as-Tool

一次聚焦调用，没有独立长期目标和生命周期，可以作为 Parent Session 中的一次 Action。

### Autonomous Sub-agent

具有独立目标、多轮执行、自己的 Context、Artifact 和 Recovery，需要独立持久化时，更适合作为 Child Session。

## 对 Agent Platform 的影响

是否创建 Child Session 不应由“是不是另一个模型”决定，而由它是否需要独立、持久的执行生命周期决定。

## 核心结论

> **Sub-agent 的首要平台价值是上下文隔离；Agent-as-Tool 是 Action，真正自治的 Sub-agent 才需要 Child Session。**