# 搜索策略与动态推理预算

## 文章中的关键观点

Research Agent 会先广泛探索，再逐步聚焦，并根据新发现调整研究计划。文章也强调让 Agent 根据任务复杂度分配更多或更少 effort。

## 我们的架构分析

### Search Broad → Narrow

研究计划不应被当成不可修改的 DAG，而更像一个当前假设：

```text
Initial Hypothesis
      ↓
Broad Search
      ↓
Evidence
      ↓
Refine Plan
      ↓
Narrow Search
```

### Dynamic Reasoning Budget

Agent 可以决定“这个问题是否值得继续深入”，但平台应限制总预算。需要持久的是：

- 决策结果；
- 预算消耗；
- 关键证据；

而不是完整 private chain-of-thought。

## 对 Agent Platform 的影响

Plan 应属于 Harness 的可变策略资源，Runtime 不把完整 reasoning 持久化为核心状态；Budget 则是平台可治理的约束。

## 核心结论

> **Plan 是可变假设，Budget 是硬约束；持久化决策和证据，不持久化完整私有推理。**