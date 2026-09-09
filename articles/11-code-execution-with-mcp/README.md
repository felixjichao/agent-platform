# Code execution with MCP: Building more efficient agents

- 原文：<https://www.anthropic.com/engineering/code-execution-with-mcp>
- 研究主题：通过代码执行编排大量 Tool Call，把中间数据留在执行环境，降低 Context 成本并增强组合能力。

## 小节

1. [PTC 是 Execution Strategy，不是 Tool Type](01-ptc-as-execution-strategy.md)
2. [LLM 应是 Control Plane，而不是 Data Plane](02-control-plane-vs-data-plane.md)
3. [Result 与 Observation 再次分离](03-result-vs-observation.md)
4. [Data Flow Policy](04-data-flow-policy.md)
5. [Workspace 与生成代码生命周期](05-workspace-and-code-lifecycle.md)
6. [Programmatic Execution Runtime](06-programmatic-execution-runtime.md)
7. [Budget、Trace 与 Governance](07-budget-trace-and-governance.md)

## 对平台架构的核心影响

- PTC（Programmatic Tool Calling）属于执行策略：同一个 Tool 可以被直接调用，也可以由生成程序批量、循环、并发调用。
- 一次 Reasoning Step 不再等于一次 Tool Call，Runtime 必须能观察程序内部的多个 Action。
- 中间数据可以只存在 Execution Environment，不必全部经过 Model Context。
- Code Execution 会把 Workspace、Data Flow Policy、Capability Proxy、Secret Isolation、Budget 和 Action Trace 变成生产级执行环境的基础能力。