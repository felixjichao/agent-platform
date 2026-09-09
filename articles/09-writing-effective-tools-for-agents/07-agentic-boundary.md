# Agentic Boundary：不要太原子，也不要包成 Workflow

## 我们的架构分析

Tool 粒度存在两个极端。

### 太原子：API-shaped

```text
list_ids
get_item
get_owner
update_field
```

Agent 被迫承担大量稳定、机械的 orchestration：

- 调用次数变多；
- Context 变长；
- 中间错误增加；
- 决策空间扩大。

### 太大：Workflow-shaped

```text
resolve_customer_problem_end_to_end()
```

稳定 mechanics 和真正需要 Agent 判断的决策全部被隐藏，Agent 失去必要控制权。

### 合理的 Agentic Boundary

> **Deterministic mechanics 下沉到 Capability；uncertain decisions 留给 Harness。**

Tool 可以封装稳定分页、查询、转换和事务细节，但应该保留需要语义判断、策略选择和风险权衡的边界。

## 对 Agent Platform 的影响

Capability Review 需要评估 Tool Granularity，而不是默认“一条 API 一个 Tool”或“一条业务流程一个 Tool”。

## 核心结论

> **最好的 Tool 粒度位于稳定机械执行与不确定智能决策的边界。**