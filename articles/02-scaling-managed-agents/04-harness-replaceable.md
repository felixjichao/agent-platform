# Harness 应该可以替换甚至消失

## 文章中的关键观点

文章强调 Harness 会编码“模型当前做不到什么”的假设。这些假设会随着模型升级迅速过时，因此不应把 Harness 的当前结构当成长期稳定平台接口。

## 我们的架构分析

Harness 更适合作为一种**适应性脚手架（Adaptive Scaffolding）**：模型弱时增加计划、提醒、上下文重置、评估等结构；模型变强后，一部分结构可能简化或消失。

因此平台设计必须满足：

```text
Runtime stable
Harness replaceable
```

更强一点：

> **Harness 应该允许被删除，而平台仍然成立。**

如果删掉 Harness 后 Session、动作执行、持久状态和审计都无法工作，说明平台边界画错了。

## 对 Agent Platform 的影响

Plan、Todo、Planner、Evaluator 等当前常见机制不应过早成为 Runtime Core。它们更适合属于 Harness 策略层。

## 核心结论

> **Runtime 应稳定，Harness 应可替换、可简化，甚至随着模型进步逐渐消失。**