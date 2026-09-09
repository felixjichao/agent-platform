# Grader、Criterion 与 Evidence

## 文章中的关键观点

文章介绍了多种 Grader：确定性规则、LLM Judge 和 Human Grader。不同评估维度需要不同证据和评分方式。

## 我们的架构分析

不能把 Grader 简化成一个“给最终答案打 0-100 分”的函数。一个稳定评估项至少需要：

```text
Criterion
→ 检查哪个质量维度

Evidence Source
→ 从 Outcome / Artifact / Trace / Environment 中取什么证据

Grader
→ 用什么机制判断

Threshold / Criticality
→ 怎样算通过，是否为硬门槛
```

Grader 类型：

- **Deterministic**：测试、结构校验、数据库状态、规则匹配。
- **LLM Judge**：开放式质量、语义正确性、综合性。
- **Human**：高风险、主观质量、最终业务责任。

应优先在适合确定性判断时使用确定性 grader，而不是所有东西都交给 LLM Judge。

## 对 Agent Platform 的影响

Evaluation Contract 应显式绑定 Criterion → Evidence → Grader，而不是只配置一个 judge prompt。

## 核心结论

> **评估标准、证据来源和评分器是三个独立概念；Grader 只是测量机制，不是质量定义本身。**