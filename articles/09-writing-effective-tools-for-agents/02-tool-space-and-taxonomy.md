# Tool Space 与 Capability Taxonomy

## 文章中的关键观点

文章指出，工具数量增加后，名称、描述和重叠功能会显著影响 Agent 的选择准确率。

## 我们的架构分析

Tool Registry 不只是接口目录，它实际定义了 Agent 的**决策空间（Tool Space）**。

如果存在：

```text
search
find
lookup
query
fetch
```

而边界不清晰，Agent 每一步都要花额外推理判断“到底该选哪个”。

因此需要 Capability Taxonomy：

```text
Domain
  ↓
Resource
  ↓
Semantic Capability
  ↓
Concrete Tool
```

每个能力应明确：

- What：能做什么；
- When：什么时候使用；
- When NOT：什么时候不要使用；
- Neighbor：与相邻工具怎么区分。

## 对 Agent Platform 的影响

Capability Registry 不能只按 MCP Server 或服务商分组，而要提供平台层的语义分类和边界治理。

## 核心结论

> **Tool Design 是接口设计，Capability Design 是 Agent 决策空间设计。**