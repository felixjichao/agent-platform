# Result 与 Observation 再次分离

## 文章中的关键观点

代码执行可以在 Tool Result 返回模型之前先做过滤和聚合，只向模型提供真正需要的信息。

## 我们的架构分析

这进一步强化：

```text
Action
  ↓
Raw Result
  ↓
Transform
├── Filter
├── Join
├── Aggregate
├── Redact
├── Persist
└── Summarize
  ↓
Observation
  ↓
Model Context
```

Result 可能很大，甚至不适合让模型直接读取；Observation 则是为了下一次决策构建的有限工作集。

因此可以出现三类数据：

```text
Model-visible Data
→ 允许进入 Context

Execution-only Data
→ 允许程序处理，但模型不可见

Persistent Resource
→ 保存到 Workspace / Resource Store，按 Ref 访问
```

## 对 Agent Platform 的影响

Observation Projection 应成为 Work Environment 的明确职责，并允许与 Context Policy、Security Policy 一起决定什么真正进入模型。

## 核心结论

> **Agent 可以被允许“处理”某些数据，而不代表模型必须被允许“看到”这些数据。**