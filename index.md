---
layout: home

hero:
  name: Agent Platform
  text: 智能体平台架构研究
  tagline: 从 Agent Loop 到平台化 Agent Harness，通过一手工程文章持续推导统一执行、上下文、工具、评估与安全治理架构。
  actions:
    - theme: brand
      text: 浏览架构图谱
      link: /architecture/
    - theme: alt
      text: 阅读当前架构
      link: /architecture/agent-platform
    - theme: alt
      text: 从第一篇开始
      link: /articles/01-building-effective-agents/

features:
  - title: 当前架构
    details: architecture/agent-platform.md 是规范性架构文档，Archify 图谱提供可交互的视觉表达。
  - title: 研究过程
    details: 每篇工程文章按小节保存原文观点、架构分析与平台影响。
  - title: 持续演进
    details: 每完成一篇研究，再把稳定结论吸收到总体架构和图谱，保留完整演进历史。
---

## Agent Platform 总体架构

从业务目标一直到真实世界，平台把动态能力组装、执行策略、稳定运行时与工作环境分层，并由上下文、评估、可观测与安全治理横向贯穿。

<iframe class="architecture-frame architecture-frame--overview" src="./diagrams/core/agent-platform-overview.architecture.html?embed=1" title="Agent Platform 总体架构图" loading="lazy"></iframe>

<div class="architecture-links">
  <a href="./architecture/">浏览完整架构图谱 →</a>
  <a href="./diagrams/core/agent-platform-overview.architecture.html">打开独立交互图 ↗</a>
</div>

## 三个关键执行层

Agent Platform 最关键的工程边界集中在 L4～L2：谁决定下一步、谁记录事实，以及 Agent 真正在哪里执行动作。

<div class="diagram-grid">
  <a class="diagram-card" href="./architecture/l4-strategy-harness">
    <span class="diagram-card__eyebrow">L4 · Execution Control</span>
    <strong>执行策略 / Harness</strong>
    <p>Direct、Workflow、Agent Loop、PTC、Multi-Agent 如何动态选择；Harness 管策略。</p>
  </a>
  <a class="diagram-card" href="./architecture/l3-runtime">
    <span class="diagram-card__eyebrow">L3 · Execution Facts</span>
    <strong>统一 Runtime</strong>
    <p>Work、Session、Run、Event、State 如何组成持久、可恢复的执行事实。</p>
  </a>
  <a class="diagram-card" href="./architecture/l2-work-environment">
    <span class="diagram-card__eyebrow">L2 · Data + Action Plane</span>
    <strong>Agent Work Environment</strong>
    <p>Workspace、执行、验证、能力代理和隔离如何组成 Agent 可作用的真实工作环境。</p>
  </a>
</div>

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

希望快速建立整体认知，从[架构图谱](/architecture/)开始；希望直接了解完整结论，从[智能体平台总体架构](/architecture/agent-platform)开始；希望理解架构为什么演进成现在的样子，从第一篇研究文章顺序阅读。
