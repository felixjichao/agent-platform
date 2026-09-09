# Multi-Agent Trust Escalation

## 文章中的关键观点

文章展望了 Multi-Agent Trust Escalation 风险：Sub-agent 可以隔离不可信内容，但如果 Parent 默认信任“内部 Agent 输出”，也可能把低可信外部信息升级成高可信指令。

## 我们的架构分析

攻击路径：

```text
Untrusted Web
    ↓
Child Agent
    ↓ transforms
Summary / Recommendation
    ↓
Parent Agent
```

如果 Parent 只看：

```text
source = internal child agent
```

就会发生 Trust Laundering。

因此 Agent-to-Agent 消息需要携带：

```text
Delegation Result
├── semantic_type
│   ├── fact
│   ├── hypothesis
│   ├── recommendation
│   └── instruction_request
├── content
├── provenance
├── evidence_refs
├── confidence
└── trust_label
```

关键原则：

- Trust 跟着数据 Provenance 走，而不是跟着 Agent 身份自动升级；
- Transformation 不意味着 Trust Elevation；
- Child recommendation 不自动扩大 Parent Capability；
- 高权限边界需要重新 Policy / Verification。

## 对 Agent Platform 的影响

Multi-Agent Protocol 应从“传文本”升级为携带语义类型、证据和信任属性的结构化 Handoff。

## 核心结论

> **Sub-agent 可以隔离 Context，但不是 Trust 洗白器；内部 Agent 输出也必须保留原始 Provenance。**