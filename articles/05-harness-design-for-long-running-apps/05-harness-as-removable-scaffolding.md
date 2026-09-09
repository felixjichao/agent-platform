# Harness 是可移除的脚手架

## 文章中的关键观点

文章在迭代 Harness 时发现，复杂 Harness 中的每个组件都编码了一个“模型自己做不到”的假设。随着模型升级，这些假设可能迅速过时。

## 我们的架构分析

因此 Harness Engineering 的目标不应该是让 Harness 越来越复杂，而应该不断问：

```text
这个组件还必要吗？
如果删除，Eval 是否下降？
模型升级后是否可以下掉？
```

这形成一个原则：

> **Harness complexity must earn its keep.**

Planner、progress reminder、forced evaluator、context reset 等都应该被当成实验变量，而不是永久架构。

## 对 Agent Platform 的影响

Runtime 只保留跨模型版本仍然稳定的执行事实、状态、资源和边界。Harness 组件通过版本管理和 Eval 发布，不下沉成不可移除的 Runtime primitive。

## 核心结论

> **Harness 是对模型能力缺口的可实验脚手架，任何组件都应该允许被 Eval 证明“已经不需要”。**