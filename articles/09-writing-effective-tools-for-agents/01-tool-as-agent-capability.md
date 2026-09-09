# Tool 的设计单位是 Agent-facing Capability

## 文章中的关键观点

文章强调，给 Agent 暴露的 Tool 应围绕 Agent 能理解、能正确选择、能组合完成真实任务来设计，而不是机械复制后端 API。

## 我们的架构分析

后端接口的原子性来自服务设计，而 Agent Tool 的粒度来自**决策语义**。

因此更合理的链路是：

```text
Backend API
    ↓
Capability Adapter
    ↓
Agent-facing Tool
```

Capability Adapter 可以：

- 合并低层 API 调用；
- 收敛参数；
- 注入稳定默认值；
- 处理分页；
- 转换结果；
- 提供 Agent 能理解的语义。

Tool 设计的目标不是让 Agent“拥有所有 API”，而是让它在合理的决策粒度上拥有行动能力。

## 对 Agent Platform 的影响

Capability Engineering 层开始独立出现。外部世界的原始 API 不应直接等价为 Tool Registry。

## 核心结论

> **Tool 的设计单位是有业务语义的 Agent Capability，而不是后端 API endpoint。**