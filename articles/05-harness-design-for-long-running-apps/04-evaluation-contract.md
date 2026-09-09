# Evaluation Contract

## 文章中的关键观点

文章通过可重复的评估机制不断检验 Harness 产生的应用，而不是依赖自然语言中的模糊“看起来不错”。

## 我们的架构分析

可以抽象出 **Evaluation Contract（评估契约）**：

```text
Criterion
→ 要检查什么

Evidence
→ 用什么证据判断

Grader / Verifier
→ 谁或什么机制判断

Threshold
→ 什么条件算通过

Aggregation
→ 多个维度如何合成
```

它和 Plan 的边界非常清楚：

```text
Plan
→ how to do

Evaluation Contract
→ how to prove it is done
```

评估契约应该在长任务过程中保持相对稳定，而具体执行计划可以频繁改变。

## 对 Agent Platform 的影响

平台需要逐渐把“验收依据”提升为一等资源，使 Harness、Verifier、人工审批和离线 Eval 可以共享同一组标准和证据结构。

## 核心结论

> **Plan 可以变化，但“怎样证明完成”必须有稳定、可执行的契约。**