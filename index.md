---
layout: home

hero:
  name: Agent Platform
  text: 智能体执行基础设施
  tagline: 把动态组装、非确定、长期、并行、可编程的智能执行过程，约束在持久、可恢复、可验证、可观测、可治理、能够持续演进的生产系统中。
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
  - title: 运行时管事实
    details: 工作、会话、运行、事件、状态、动作、结果与恢复构成稳定的执行事实。
  - title: 执行框架管策略
    details: 工作流、智能体循环、PTC、多智能体等执行策略可以持续替换和演进。
  - title: 平台管边界
    details: 上下文、评估、追踪、安全与治理共同把非确定执行约束成生产系统。
---

<!-- README-SYNC: README.md 的核心定位或架构判断变化时必须同步更新本页，CI 会检查。 -->

## Agent Platform 总体架构

从业务目标一直到真实世界，平台把能力契约、能力工程、执行策略、稳定运行时与智能体工作环境分层，并由上下文、评估、可观测性与安全治理横向贯穿。

<iframe class="architecture-frame architecture-frame--overview" src="./diagrams/core/agent-platform-overview.architecture.html?embed=1" title="Agent Platform 总体架构图" loading="lazy"></iframe>

<div class="architecture-links">
  <a href="./architecture/">浏览完整架构图谱 →</a>
  <a href="./diagrams/core/agent-platform-overview.architecture.html">打开独立交互图 ↗</a>
</div>

## 核心判断

当前研究形成了 12 个核心架构判断：

1. **应用形态不等于执行范式**：对话、科研、知识库、Coding 是产品形态；直接执行、工作流、智能体循环、PTC、多智能体是执行范式。
2. **工作流与智能体的真正区别是执行控制权**：二者是从静态控制到动态控制的一条连续谱。
3. **运行时管事实，执行框架管策略**：稳定执行事实与可演进执行策略必须解耦。
4. **工作承载长期连续性，而不是智能体**：智能体可以退出、遗忘或替换，但工作必须持续存在。
5. **事件是事实，状态和上下文都是投影**：真实历史不能被快照、摘要或上下文压缩取代。
6. **上下文是工作集，不是整个世界**：上下文应按当前目标动态投影、按需加载，并可以重建。
7. **LLM 应该是控制面，而不是数据面**：循环、过滤、聚合等数据操作应尽量下沉到执行环境。
8. **工具、技能、MCP、执行框架是不同层次的抽象**：连接协议不等于面向智能体的能力设计。
9. **智能体可以动态组装**：技能、工具、知识和上下文应按任务形成实际工作的智能体。
10. **多智能体的关键是工作前沿**：平台真正需要调度的是可独立推进的工作单元，而不是智能体数量。
11. **评估是能力规格**：执行框架说明怎么实现，评估说明怎么证明具备能力。
12. **智能体安全的本质是可达范围控制**：通过确定性边界限制每个工作、运行、子智能体可触达的世界。

## 三个关键执行层

Agent Platform 最关键的工程边界集中在 L4～L2：谁决定下一步、谁记录事实，以及智能体真正在哪里执行动作。

<div class="diagram-grid">
  <a class="diagram-card" href="./architecture/l4-strategy-harness">
    <span class="diagram-card__eyebrow">L4 · 执行控制</span>
    <strong>执行策略 / 执行框架</strong>
    <p>直接执行、工作流、智能体循环、PTC、多智能体如何动态选择；执行框架负责策略。</p>
  </a>
  <a class="diagram-card" href="./architecture/l3-runtime">
    <span class="diagram-card__eyebrow">L3 · 执行事实</span>
    <strong>统一运行时</strong>
    <p>工作、会话、运行、事件、状态如何组成持久、可恢复的执行事实。</p>
  </a>
  <a class="diagram-card" href="./architecture/l2-work-environment">
    <span class="diagram-card__eyebrow">L2 · 数据面 + 动作面</span>
    <strong>智能体工作环境</strong>
    <p>工作空间、执行、验证、能力代理和隔离如何组成智能体可以作用的真实工作环境。</p>
  </a>
</div>

## 研究路线

1. [Building effective agents](/articles/01-building-effective-agents/)：工作流与智能体、执行控制与统一执行内核。
2. [Scaling Managed Agents](/articles/02-scaling-managed-agents/)：大脑与手的解耦、会话执行框架与持久状态。
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

希望快速建立整体认知，从[架构图谱](/architecture/)开始；希望直接了解完整结论，从[智能体平台总体架构](/architecture/agent-platform)开始；希望理解这些判断如何逐步形成，从第一篇研究文章顺序阅读。
