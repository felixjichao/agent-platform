# Effort Scaling：不是所有任务都给同样预算

## 文章中的关键观点

Anthropic 发现多智能体研究的质量与 token 使用、搜索次数和并行 Agent 数量高度相关，因此需要根据任务复杂度调整 effort。

## 我们的架构分析

Effort 不应该只等价于“模型 thinking level”。更完整的预算包括：

```text
Effort Budget
├── Reasoning Budget
├── Delegation Budget
├── Action / Tool Budget
├── Search Budget
├── Evaluation Budget
└── Cost / Time Budget
```

任务复杂度越高，可以允许更深搜索、更多并行 Agent 和更严格验证；简单任务则应尽快收敛。

## 对 Agent Platform 的影响

Budget 应成为 Harness 可读取的运行约束，而不是散落在 Prompt 中。它既影响性能，也影响成本、延迟和风险。

## 核心结论

> **Effort Scaling 是资源治理问题：推理、委托、动作和评估都应该有可调预算。**