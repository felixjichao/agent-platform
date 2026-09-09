# Scaling Managed Agents: Decoupling the brain from the hands

- 原文：<https://www.anthropic.com/engineering/managed-agents>
- 研究主题：把会话、执行框架和执行环境解耦，寻找比具体 Harness 更稳定的平台接口。

## 为什么研究这篇文章

如果 Agent Platform 直接围绕某个当前版本的 Harness 构建，模型能力一升级，平台结构就可能被迫重写。Managed Agents 给出了一个更稳定的方向：把“如何思考和推进”与“如何持久化、如何执行动作”分开。

## 小节

1. [Session、Harness 与 Execution Environment](01-session-harness-environment.md)
2. [把脑和手解耦](02-decouple-brain-and-hands.md)
3. [持久状态不能依赖 Harness 进程](03-durable-state-outside-harness.md)
4. [Harness 应该可以替换甚至消失](04-harness-replaceable.md)
5. [从 Sandbox 泛化到 Execution Environment](05-execution-environment-generalization.md)

## 对平台架构的核心影响

- Session 负责持久事实，Harness 负责当前执行策略，Execution Environment 负责真实动作。
- Harness 可以无状态、可替换，平台稳定性不能依赖某个 Harness 进程长期存活。
- “Sandbox”不足以覆盖所有 Agent 场景，更稳定的抽象是执行环境。