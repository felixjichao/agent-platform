# How we contain Claude across products

- 原文：<https://www.anthropic.com/engineering/how-we-contain-claude>
- 研究主题：随着 Agent 自主性和可达世界扩大，如何通过模型层、内容层和执行环境层的纵深防御控制 Blast Radius。

## 小节

1. [Risk = Failure Probability × Blast Radius](01-risk-probability-times-blast-radius.md)
2. [三类风险来源与纵深防御](02-three-risk-sources-defense-in-depth.md)
3. [Containment Profile 与用户监督能力](03-containment-profiles-and-oversight.md)
4. [Network Allowlist 本质是 Capability Grant](04-network-allowlist-as-capability-grant.md)
5. [Trust before privileged interpretation](05-trust-before-interpretation.md)
6. [用户也可能成为 Prompt Injection 通道](06-user-as-injection-channel.md)
7. [Context Ingress 与 Tool Output Trust](07-context-ingress-and-tool-output.md)
8. [Multi-Agent Trust Escalation](08-multi-agent-trust-escalation.md)
9. [Persistent Memory Poisoning](09-persistent-memory-poisoning.md)
10. [Containment 与 Observability 的张力](10-containment-observability-tradeoff.md)
11. [Just-in-Time Capability Boundary](11-just-in-time-capability-boundary.md)
12. [Agent Identity 与 Delegation](12-agent-identity-and-delegation.md)
13. [优先使用 Battle-tested Security Primitives](13-prefer-battle-tested-primitives.md)

## 对平台架构的核心影响

- 安全目标从“让 Agent 不犯错”升级为“即使犯错也把最大后果限制在可接受范围内”。
- Agent Security 需要同时治理 Context Ingress、Trust Propagation、Execution Boundary、Egress、Identity 和 Memory。
- Capability Grant 的核心授权单元逐渐收敛为 `Principal × Capability × Resource × Scope × Duration`。
- Containment 的本质是控制 Agent Reachability，而不只是 `sandbox=true`。
- Agent-specific 创新主要发生在 Governance / Policy；底层 Isolation / Enforcement 应尽量复用成熟安全原语。