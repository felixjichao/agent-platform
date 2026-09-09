# How we built our multi-agent research system

- 原文：<https://www.anthropic.com/engineering/multi-agent-research-system>
- 研究主题：什么时候值得使用多智能体，以及如何治理并行、委托、上下文、恢复与评估。

## 小节

1. [什么时候 Multi-Agent 值得使用](01-when-multi-agent-is-worth-it.md)
2. [Lead Agent 是 Orchestrator + Global Context Owner](02-lead-agent-global-context.md)
3. [Effort Scaling：不是所有任务都给同样预算](03-effort-scaling.md)
4. [Agent-as-Tool 与 Child Session](04-child-session-and-agent-as-tool.md)
5. [Goal-driven Dynamic Team Formation](05-dynamic-team-formation.md)
6. [恢复、并发与异步委托](06-recovery-concurrency-and-async.md)
7. [搜索策略与动态推理预算](07-search-and-reasoning-budget.md)
8. [Outcome Eval、Process Eval 与 Specialist Agent](08-outcome-process-eval-and-specialists.md)

## 对平台架构的核心影响

- 多智能体不是复杂任务的默认答案，只有在可并行、上下文可隔离、依赖密度低且结果易合并时才值得。
- Lead Agent 负责全局目标和整合，Child Agent 负责局部探索。
- Agent Team 可以是运行时根据 Goal、Capability、Budget 等动态形成的结果，而不是用户预先画好的固定拓扑。
- 多智能体需要两层并发、异步委托、局部恢复和全局协调。