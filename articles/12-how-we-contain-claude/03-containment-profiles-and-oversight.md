# Containment Profile 与用户监督能力

## 文章中的关键观点

Anthropic 在不同产品采用不同隔离方式：云端临时 Container、Claude Code 的 HITL + OS Sandbox、Cowork 的更强 VM 边界。差异与产品能力、风险和目标用户能否理解安全提示有关。

## 我们的架构分析

Containment 不是“越强越好”，需要匹配：

```text
Risk
× Agent Autonomy
× Capability Scope
× User Oversight Capability
```

例如开发者通常能够理解 Shell / Filesystem 风险，因此可以把少量越界决策交给 HITL；普通知识工作者无法判断 Bash 命令时，多弹确认框并不会真正提高安全。

更成熟的模式是：

```text
Allowed Autonomous Zone
├── bounded workspace
├── safe capabilities
├── bounded network
└── scoped credentials
        ↓ boundary
Approval / Deny / Escalation
```

Agent 在硬边界内尽量少被打断，只有真正需要人类语义判断的越界动作进入 HITL。

## 对 Agent Platform 的影响

应显式建模 Containment Profile：

```text
Containment Profile
├── isolation_mode
├── filesystem_scope
├── network_scope
├── credential_scope
├── resource_budget
├── allowed_capabilities
├── approval_boundary
└── user_oversight_level
```

## 核心结论

> **成熟的 Autonomy 是“边界内自由”，而不是“每一步审批”或“完全无边界”。**