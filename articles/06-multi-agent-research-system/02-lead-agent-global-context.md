# Lead Agent 是 Orchestrator + Global Context Owner

## 文章中的关键观点

Research 系统由 Lead Agent 规划研究方向、创建并行 Sub-agent，随后综合各自返回的结果。

## 我们的架构分析

Lead Agent 不只是“高级 Agent”，它承担两个稳定职责：

1. **Orchestrator**：决定如何拆解、委托、补充搜索和停止。
2. **Global Context Owner**：维护全局问题、覆盖情况、冲突和最终综合。

Child Agent 则拥有局部上下文：

```text
Global Goal
   ↓
Lead Agent
   ├── Local Goal A → Child A
   ├── Local Goal B → Child B
   └── Local Goal C → Child C

Child → Findings / Evidence / Summary
Lead  → Global Synthesis
```

这是一种主动的上下文分区机制。

## 对 Agent Platform 的影响

Parent / Child 应有明确上下文和责任边界。Child 不需要继承 Parent 的完整 Context，只接收完成局部任务所需的最小信息。

## 核心结论

> **Lead Agent 的核心职责是全局编排和全局上下文所有权，而 Child Agent 负责受限的局部工作空间。**