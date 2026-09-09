# 生成与评估必须分离

## 文章中的关键观点

文章通过更明确的 evaluator 机制来检查应用是否真正满足要求，而不是只依赖执行 Agent 自己判断“我完成了”。

## 我们的架构分析

Agent 同时承担：

```text
生成方案
实现方案
判断自己的方案是否正确
```

会产生明显的自证偏差。更合理的是逻辑分离：

```text
Generator
→ 产生候选结果

Evaluator / Verifier
→ 根据独立标准验证结果
```

这里“分离”不一定意味着必须使用两个物理模型实例。核心是：

- 评估标准独立；
- 评估证据独立；
- 不能因为生成器认为完成就直接接受。

## 对 Agent Platform 的影响

Evaluator 属于 Harness / Evaluation Strategy，但验证结果和证据应能够进入运行时和 Artifact 状态，供后续 Recovery、Audit 和最终 Acceptance 使用。

## 核心结论

> **Execution State 与 Acceptance State 必须分开；生成完成不等于验收通过。**