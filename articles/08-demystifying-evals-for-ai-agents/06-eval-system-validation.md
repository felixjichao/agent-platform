# Eval 系统本身也必须被验证和版本化

## 文章中的关键观点

文章强调在信任 Eval 结果前，要检查 grader 是否与人工判断一致、任务是否有效、reference solution 是否能通过以及评估是否存在明显偏差。

## 我们的架构分析

Eval 不是“真理机器”，它也是软件系统和测量系统。

可以区分：

```text
Trial / Outcome
→ Fact

Eval Score
→ Measurement Projection
```

Score 是对真实 Outcome 的一种测量，不等于 Outcome 本身。

因此需要：

- Grader version；
- Rubric version；
- Task version；
- Judge model version；
- Calibration dataset；
- Human Ground Truth；
- Eval Harness version。

如果 Judge Prompt 或模型版本变化，历史分数可能不再可以直接横向比较。

## 对 Agent Platform 的影响

Eval 结果必须可追溯到完整 Measurement Configuration。平台还需要支持 grader calibration 和与人工 Ground Truth 的一致性检查。

## 核心结论

> **Outcome 是事实，Score 是测量投影；Eval 系统本身同样需要版本、校准和回归测试。**