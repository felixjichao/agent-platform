# Context Ingress 与 Tool Output Trust

## 文章中的关键观点

可信 Connector / MCP / Tool 返回的数据仍然可能由不可信外部主体控制。例如可信 GitHub Connector 可以读取包含 Prompt Injection 的 README。

## 我们的架构分析

必须区分：

```text
Tool / Connector Trust
≠ Returned Content Trust
```

传统供应链审核解决：代码是否可信、版本是否安全、服务提供者是否可信。

Agent 还需要解决：

> **返回内容进入 Model Context 后，会不会改变 Agent 行为？**

因此 Result → Observation Pipeline 需要增加 Context Ingress Boundary：

```text
External Tool
     ↓
Raw Tool Result
     ↓
Content Security Gateway
├── Provenance
├── Trust Classification
├── Prompt Injection Scan
├── Data Inspection
├── Sanitization / Redaction
└── Policy Check
     ↓
Observation
     ↓
Model Context
```

事后 Audit 不能完全替代 Pre-context Inspection，因为被污染的 Agent 后续可能只调用“正常且已授权”的 API。

## 对 Agent Platform 的影响

Observation Layer 不只是 Token 优化层，还承担 Context Security：Relevance、Redaction、Provenance、Trust、Injection Detection。

## 核心结论

> **可信 Capability 不代表可信 Observation；外部内容在进入 Context 前必须经过独立的 Context Ingress Boundary。**