# Tool Result 是 Context Producer

## 文章中的关键观点

文章强调 Tool 返回结果的结构、字段名称、分页方式和信息密度会显著影响 Agent 的后续推理。

## 我们的架构分析

因此：

> **Tool 不只是 Action Executor，也是 Context Producer。**

需要区分：

```text
Raw API Response
      ↓
Tool Result Transformation
      ↓
Agent-facing Observation
      ↓
Context
```

Transformation 可以包括：

- 删除无关字段；
- 摘要；
- 结构化元数据；
- 大对象使用 Resource Ref；
- 分页 / truncation；
- 下一步导航提示；
- Error Recovery Guidance。

错误结果同样是 Observation。好的错误不是只返回 `500`，而是告诉 Agent：发生了什么、是否可重试、应该修改什么参数。

## 对 Agent Platform 的影响

Action Result 与 Model Observation 应分离。运行时可以保存真实 Result，Context Builder 使用经过处理的 Observation。

## 核心结论

> **Result 是执行事实，Observation 是面向 Agent 的信息投影；Tool 输出设计本质上属于 Context Engineering。**