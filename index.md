---
layout: home

hero:
  name: Agent Platform
  text: 智能体平台架构研究
  tagline: 从 Agent Loop 到平台化 Agent Harness，通过一手工程文章持续推导统一执行、上下文、工具、评估与安全治理架构。
  actions:
    - theme: brand
      text: 阅读当前架构
      link: /architecture/agent-platform
    - theme: alt
      text: 从第一篇开始
      link: /articles/01-building-effective-agents/

features:
  - title: 当前架构
    details: 以 architecture/agent-platform.md 作为当前稳定架构的事实入口。
  - title: 研究过程
    details: 每篇工程文章按小节保存原文观点、架构分析与平台影响。
  - title: 持续演进
    details: 每完成一篇研究，再把稳定结论吸收到总体架构，保留完整演进历史。
---

## Agent Platform 总体架构 · Archify MVP

这一版改用 Archify：`Typed JSON IR` 是可编辑、可 Diff 的图源，交互 HTML 由 Archify 校验后确定性生成。

<iframe src="./diagrams/core/agent-platform-overview.architecture.html" title="Agent Platform 总体架构图" style="width:100%;height:760px;border:1px solid var(--vp-c-divider);border-radius:12px;background:var(--vp-c-bg);" loading="lazy"></iframe>

[打开独立交互图](/diagrams/core/agent-platform-overview.architecture.html) · [查看 Archify 图源](https://github.com/felixjichao/agent-platform/blob/feat/visual-architecture-mvp/diagrams/core/agent-platform-overview.architecture.json)

## Agent Software Stack

七层软件栈提供整个项目的统一坐标系：越往上越接近业务语义，越往下越接近稳定执行事实和真实资源。

![Agent Software Stack 七层软件栈](/diagrams/core/agent-software-stack.svg)

## 一个关键边界：Runtime vs Harness

Harness 负责“当前准备怎么完成”，Runtime 负责“实际上发生了什么”。前者应该可替换、可演进，后者承担稳定、持久、可恢复的执行事实。

![Runtime vs Harness](/diagrams/core/runtime-vs-harness.svg)

## 研究路线

当前研究从执行控制出发，逐步扩展到长任务、多智能体、评估、能力工程、代码执行与安全治理：

1. [Building effective agents](/articles/01-building-effective-agents/)：工作流与智能体、执行控制与统一执行内核。
2. [Scaling Managed Agents](/articles/02-scaling-managed-agents/)：大脑与手的解耦、会话 Harness 与持久状态。
3. [Effective context engineering](/articles/03-effective-context-engineering/)：上下文工作集、投影、压缩与隔离。
4. [Effective harnesses for long-running agents](/articles/04-effective-harnesses-for-long-running-agents/)：长任务恢复、交接与事实来源。
5. [Harness design for long-running apps](/articles/05-harness-design-for-long-running-apps/)：执行一致性、生成与评估分离。
6. [Multi-agent research system](/articles/06-multi-agent-research-system/)：多智能体编排与研究任务分解。
7. [Building a C compiler with parallel Claudes](/articles/07-building-c-compiler/)：并行智能体协作与工程约束。
8. [Demystifying evals for AI agents](/articles/08-demystifying-evals-for-ai-agents/)：智能体评估体系。
9. [Writing effective tools for agents](/articles/09-writing-effective-tools-for-agents/)：工具设计与能力工程。
10. [Agent Skills](/articles/10-agent-skills/)：可组合、可发现的能力封装。
11. [Code execution with MCP](/articles/11-code-execution-with-mcp/)：程序化工具调用与代码执行。
12. [How we contain Claude](/articles/12-how-we-contain-claude/)：执行隔离、权限边界与安全治理。

## 阅读方式

如果希望直接了解当前结论，从[智能体平台总体架构](/architecture/agent-platform)开始；如果希望理解架构为什么演进成现在的样子，从第一篇研究文章顺序阅读。
