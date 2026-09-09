# Tool Contract：Schema 之外还需要 Usage Guidance

## 文章中的关键观点

文章通过实际工具优化发现，仅有 JSON Schema 不足以让 Agent 正确使用 Tool。清晰名称、描述、参数解释和使用示例都会显著影响效果。

## 我们的架构分析

Tool Contract 可以分成：

```text
Identity
→ 这个能力叫什么

Applicability
→ 何时用 / 何时不用

Semantics
→ 调用意味着什么

Input / Output Schema
→ 数据结构

Usage Guidance
→ 怎样使用最有效

Side Effects
→ 会改变什么

Permission / Risk
→ 需要哪些授权
```

Schema 解决：

> 机器允许什么？

Guidance 解决：

> Agent 怎样才能用对？

Tool Description 因而是一种 **Capability-level Prompt Engineering**，应该版本化和 Eval。

## 对 Agent Platform 的影响

Tool Registry 需要保存完整 Capability Contract，而不只是函数名 + JSON Schema。

## 核心结论

> **Tool Contract 同时包含机器可验证 Schema 和面向 Agent 的语义使用指导。**