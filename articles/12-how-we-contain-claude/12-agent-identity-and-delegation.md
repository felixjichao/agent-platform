# Agent Identity 与 Delegation

## 文章中的关键观点

文章提出未来 Agent Identity 的关键问题：Agent 应作为用户身份的延伸，还是拥有自己的 Principal？实践更可能走向混合模式。

## 我们的架构分析

如果 Agent 完全复制用户长期身份：

```text
User Permissions
      ↓ inherit
Agent
```

Blast Radius 很容易远超当前 Task Need。

更合理的 Identity Chain：

```text
Human Principal
      │ delegates
      ▼
Agent Principal
      │ assumes / narrows
      ▼
Execution Principal
      │ uses
      ▼
Scoped Credential
```

建议区分：

### Human Identity

谁拥有、发起和最终负责 Work。

### Agent Identity

哪个自治执行主体代表谁、正在处理哪个 Work。

### Execution Identity

当前 Session / Run 实际使用的最短生命周期权限主体。

同时分离：

```text
Identity
→ 我是谁

Delegation
→ 我代表谁

Authority
→ 我被允许做什么

Credential
→ 我如何证明这些权限
```

Multi-Agent delegation 应创建新的受限 Principal，而不是复制 Parent Credential。

Audit 需要保留完整链路：Human → Parent Agent → Child Agent → Execution Credential → Action。

## 对 Agent Platform 的影响

Authorization 决策逐渐完整为：

```text
Principal
× Delegation Chain
× Capability
× Resource
× Scope
× Duration
× Context
```

## 核心结论

> **Agent 需要成为可独立授权、审计、限制和撤销的 Principal，但不能切断与 Human Principal 的责任链。**