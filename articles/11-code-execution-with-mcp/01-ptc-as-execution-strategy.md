# PTC 是 Execution Strategy，不是 Tool Type

## 文章中的关键观点

文章展示了让模型生成代码，由代码批量调用 MCP Tool，并在程序内部做循环、过滤、聚合，从而避免每次 Tool Call 都重新经过模型上下文。

## 我们的架构分析

这类模式当前可以统一称为 PTC（Programmatic Tool Calling）。核心是调用路径变化：

### Direct Tool Calling

```text
Model
  ↓
Tool A
  ↓ result
Model
  ↓
Tool B
  ↓
Model
```

### PTC

```text
Model
  ↓ generates program
Program
  ├── Tool A
  ├── Tool B
  ├── Tool C
  ├── loop
  ├── filter
  └── aggregate
       ↓
Condensed Observation
       ↓
Model
```

同一个 Tool 并没有改变类型，变化的是 Tool Orchestration Mode。

## 对 Agent Platform 的影响

PTC 应进入 L4 Execution Strategy，与 Direct、Workflow、Agent Loop、Multi-Agent 并列或组合，而不是在 Capability Catalog 里创建一种“PTC Tool”。

## 核心结论

> **PTC 是执行策略 / Tool Orchestration Mode，不是新的 Tool 类型。**