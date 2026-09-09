# Namespacing 与 Capability Discovery

## 文章中的关键观点

文章强调 Tool 命名和分组会影响模型选择。当工具集扩大时，把所有定义一次性放入 Context 会增加干扰和成本。

## 我们的架构分析

Namespacing 不只是视觉整理，它提供 Capability Space 的层级导航：

```text
Goal
 ↓
Domain
 ↓
Resource
 ↓
Operation
```

例如：

```text
github.repo.read
github.repo.create_pr
calendar.event.create
calendar.availability.query
```

随着工具数量上升，问题从：

> Tool Selection

逐渐变成：

> Capability Discovery → Tool Loading → Tool Selection

因此 Registry 和 Context 必须解耦：全量能力可以存在 Registry，但当前模型 Context 只加载相关子集。

## 对 Agent Platform 的影响

Capability Discovery 开始成为独立平台能力。Tool Definitions 应支持即时加载，而不是永久占据 Context。

## 核心结论

> **工具规模化以后，Agent 首先需要发现 Capability，再加载具体 Tool；Namespacing 是能力空间导航的一部分。**