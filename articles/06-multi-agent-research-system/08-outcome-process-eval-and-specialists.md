# Outcome Eval、Process Eval 与 Specialist Agent

## 文章中的关键观点

多智能体研究难以用固定“正确路径”评估，因为不同运行可能采用完全不同的搜索和委托过程。Anthropic 更关注最终研究质量，同时也分析过程指标和失败模式。

## 我们的架构分析

### Outcome Eval

回答：最终结果是否好？

例如：事实准确、覆盖充分、引用可靠、综合清晰。

### Process Eval

回答：执行过程是否暴露问题？

例如：重复搜索、无效委托、成本过高、局部 Agent 长时间无进展。

不应该要求所有成功 Trial 遵循同一个 Golden Agent Path。

### Specialist Agent

Citation Agent、Verifier、Research Specialist 等可以作为一种 Capability 提供给 Lead Agent，而不一定都成为永久固定团队角色。

## 对 Agent Platform 的影响

Eval 需要同时读取 Outcome 和 Trace；专门 Agent 可以通过 Agent-as-Tool 或 Child Session 暴露为可发现能力。

## 核心结论

> **开放式 Agent 不应按固定路径验收；Outcome 定义是否成功，Process Eval 用于发现效率和策略问题。**