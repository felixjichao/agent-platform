# Equipping agents for the real world with Agent Skills

- 原文：<https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills>
- 研究主题：把可复用程序性知识从 Agent 定义中拆出来，形成可发现、可组合、可版本化的 Skill。

## 小节

1. [Skill、Tool 与 Harness 的边界](01-skill-vs-tool-vs-harness.md)
2. [Progressive Disclosure：发现与加载分离](02-progressive-disclosure.md)
3. [Skill Anatomy 与 Skill-local Script](03-skill-anatomy-and-scripts.md)
4. [Eval-driven Skill Engineering](04-eval-driven-skills.md)
5. [Skill 是可执行供应链资产](05-security-and-supply-chain.md)
6. [Skill Information Architecture](06-information-architecture.md)
7. [Skill Registry 与动态组合](07-skill-registry-and-composition.md)
8. [Skill 与 MCP 的关系](08-skill-and-mcp.md)

## 对平台架构的核心影响

- Tool 解决“能做什么动作”，Skill 解决“这类任务应该怎么做”，Harness 解决“当前任务现在怎么推进”。
- Skill 不属于某个 Agent 私有定义，而应成为独立、可发现、可版本化、可治理的能力资产。
- Skill 的 Progressive Disclosure 与 Tool Discovery 使用相同的 Context Engineering 原理。
- Skill 中的脚本与平台 Tool 需要区分：前者是 Skill-local deterministic implementation，后者是平台可治理的外部行动能力。