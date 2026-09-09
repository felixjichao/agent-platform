# Writing effective tools for agents — with agents

- 原文：<https://www.anthropic.com/engineering/writing-tools-for-agents>
- 研究主题：Tool 不只是后端 API 包装，而是面向 Agent 决策空间设计的能力接口。

## 小节

1. [Tool 的设计单位是 Agent-facing Capability](01-tool-as-agent-capability.md)
2. [Tool Space 与 Capability Taxonomy](02-tool-space-and-taxonomy.md)
3. [Tool Result 是 Context Producer](03-tool-result-as-context-producer.md)
4. [Tool Contract：Schema 之外还需要 Usage Guidance](04-tool-contract-and-guidance.md)
5. [Eval-driven Tool Engineering](05-eval-driven-tool-engineering.md)
6. [Namespacing 与 Capability Discovery](06-namespacing-and-discovery.md)
7. [Agentic Boundary：不要太原子，也不要包成 Workflow](07-agentic-boundary.md)

## 对平台架构的核心影响

- Backend API 与 Agent-facing Tool 之间需要 Capability Adapter。
- Tool Space 是 Agent 的决策空间，工具重叠和命名混乱会直接降低能力。
- Tool Result 需要经过过滤、结构化、分页、恢复提示等处理后再成为 Observation。
- Tool 的设计和版本升级应该使用真实 Agent Task 和 Eval 驱动，而不是只做接口正确性测试。