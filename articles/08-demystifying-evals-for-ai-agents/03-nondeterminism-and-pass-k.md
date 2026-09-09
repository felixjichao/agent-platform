# 非确定性：pass@k 与 pass^k

## 文章中的关键观点

Agent 具有明显非确定性。同一个 Task 多次执行可能出现不同策略和结果，因此单次 Trial 不能代表能力或可靠性。

## 我们的架构分析

需要根据问题选择统计指标。

### pass@k

k 次尝试中至少一次成功。

它更接近：

> **Capability / Search Potential：系统有没有能力找到成功路径？**

### pass^k

k 次尝试全部成功。

它更接近：

> **Reliability：系统能不能稳定重复成功？**

例如一个 Coding Agent：

```text
10 次里成功 9 次
```

对“能力是否存在”可能已经很好，但对于自动 Production Deployment，1/10 的失败率仍然不可接受。

## 对 Agent Platform 的影响

Eval Runner 需要原生支持同 Task 多 Trial、随机种子 / 环境隔离、统计聚合和置信区间，而不是把一次执行结果写成 Capability Score。

## 核心结论

> **非确定性 Agent 必须通过多 Trial 测量；pass@k 看能力上限，pass^k 更接近稳定可靠性。**