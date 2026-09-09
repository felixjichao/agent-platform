# Agent-as-Tool 与 Child Session

## 文章中的关键观点

Research 系统会创建多个 Sub-agent，每个 Sub-agent 有独立上下文并完成一段自主研究，再把结果返回 Lead Agent。

## 我们的架构分析

需要区分两种语义：

### Agent-as-Tool

- 聚焦调用；
- 生命周期短；
- 不需要独立恢复；
- 返回后即结束。

它可以建模为 Parent Session 中的一次 Action。

### Autonomous Child Agent

- 独立目标；
- 多轮自主执行；
- 独立 Context；
- 可能产生 Artifact；
- 可能失败、暂停或恢复。

它更适合拥有 Child Session。

因此判断标准不是“是否调用了另一个 LLM”，而是是否形成独立执行生命周期。

## 对 Agent Platform 的影响

Parent Session 与 Child Session 需要建立 Delegation Link，保留目标、预算、结果、状态和因果关系。

## 核心结论

> **Agent-as-Tool 属于 Action；具有独立生命周期的自治 Sub-agent 属于 Child Session。**