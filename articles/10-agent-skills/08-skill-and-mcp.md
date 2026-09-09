# Skill 与 MCP 的关系

## 我们的架构分析

Skill、Tool、MCP 经常被混用，但它们解决的是不同层次问题：

```text
MCP
→ 怎么连接外部系统？

Tool
→ Agent 可以执行什么动作？

Skill
→ Agent 应该怎样完成一类任务？
```

因此：

> **Tool solves action; MCP solves connectivity; Skill solves method.**

MCP Server 暴露的原始工具集不应天然直接进入 Agent Capability Space。平台仍然需要 Capability Adapter、Taxonomy、Naming、Output Policy 和 Permission。

Skill 最好面向语义 Capability 编写，而不是强绑定某个具体 MCP Server 名称。不同环境可以把同一个语义 Capability 绑定到不同实现。

## 对 Agent Platform 的影响

Capability Catalog 在逻辑上高于 MCP Registry：

```text
Skill
  ↓ requires
Semantic Capability
  ↓ binds
Tool
  ↓ implemented via
MCP / API / Local Script
```

## 核心结论

> **MCP 是连接标准，不是 Capability Design Standard；Skill 应尽可能依赖语义能力，而不是具体连接实现。**