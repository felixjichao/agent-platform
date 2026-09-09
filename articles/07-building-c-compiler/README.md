# Building a C compiler with a team of parallel Claudes

- 原文：<https://www.anthropic.com/engineering/building-c-compiler>
- 研究主题：多个 Agent 在同一真实工程世界中长期并行协作时，如何组织共享状态、工作发现、验证和治理。

## 小节

1. [从 Isolated World 到 Shared-State Collaboration](01-shared-state-collaboration.md)
2. [Work Frontier：Multi-Agent 的真正调度对象](02-work-frontier.md)
3. [Agent Work Environment](03-agent-work-environment.md)
4. [Steward、Verifier 与长期质量](04-steward-and-verifier.md)
5. [Recovery 与 Escalation 必须分开](05-recovery-vs-escalation.md)
6. [Work / Session / Run 层级修正](06-work-session-run-hierarchy.md)
7. [Verification Ladder 与 Cost per Successful Outcome](07-verification-ladder-and-cost.md)
8. [Human 从 Execution Path 移向 Governance Plane](08-governance-plane.md)

## 对平台架构的核心影响

- 多智能体共享同一个 Work，但不共享同一个 Context。
- 真正决定并行度的是当前有多少独立、可领取、可验证的工作前沿，而不是“最多启动多少 Agent”。
- 执行环境升级为 Agent Work Environment：不仅提供 Sandbox，还提供共享资源、工作发现、Ownership、Observation、Verification 和反馈。
- Work、Session、Run 三层关系被重新定义：长期目标属于 Work；Session 是某个 Agent 与 Work 的连续执行关系；Run 是一次被触发后的连续执行片段。