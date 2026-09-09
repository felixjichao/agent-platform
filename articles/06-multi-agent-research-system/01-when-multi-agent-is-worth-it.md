# 什么时候 Multi-Agent 值得使用

## 文章中的关键观点

Anthropic 的研究系统利用多个 Agent 并行探索不同信息空间，从而扩大搜索覆盖度和有效上下文总量。但多智能体同时带来更高 token 成本、协调成本和可靠性问题。

## 我们的架构分析

“任务复杂”不是使用 Multi-Agent 的充分条件。更合理的判断维度是：

```text
收益
≈ Parallelizability
 + Context Independence
 + Result Mergeability
 - Dependency Density
 - Coordination Cost
```

典型适合场景：

- 多个相互独立的研究方向；
- 每个子问题会产生大量局部上下文；
- 最终结果可以汇总；
- 并行能显著降低 wall-clock time。

不适合：

- 强顺序依赖；
- 子任务频繁修改同一状态；
- 需要每一步紧密共享推理上下文。

## 对 Agent Platform 的影响

Multi-Agent 应作为 Execution Strategy，而不是独立产品形态。平台需要在任务特征足够适合时才启用。

## 核心结论

> **Complexity 不等于 Multi-Agent；真正决定价值的是可并行性、上下文独立性、结果可合并性与协调成本。**