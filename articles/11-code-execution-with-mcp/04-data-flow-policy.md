# Data Flow Policy

## 我们的架构分析

当 Execution Environment 可以直接在多个系统之间搬运数据时，权限不能只回答：

> “这个 Tool 能不能调用？”

还需要回答：

> “这类数据可以从哪里流向哪里？”

例如：

```text
PII DB → approved CRM       ✓
PII DB → arbitrary LLM      ✗
PII DB → public internet    ✗
```

这是一种 Data Flow Policy：

```text
Source
+ Data Classification
+ Destination
+ Capability
+ Purpose / Work Context
      ↓
Allow / Deny / Redact
```

PTC 使这一问题变得更重要，因为中间数据不再经过每次模型决策；必须由 Runtime / Environment 做确定性 enforcement。

## 对 Agent Platform 的影响

Capability Permission 与 Data Flow Permission 是两种不同政策。拥有 `crm.write` 不自动意味着任何来源数据都允许写入 CRM。

## 核心结论

> **Programmatic Execution 需要独立 Data Flow Policy；Tool 可调用不等于任意数据可以经过它流动。**