# Agent Platform

> **Agent Platform 的核心，不是“跑一个 Agent Loop”，而是把动态组装、非确定、长期、并行、可编程的智能执行过程，约束在持久、可恢复、可验证、可观测、可治理、能够持续演进的生产系统中。**

**在线阅读：<https://felixjichao.github.io/agent-platform/>**

## 为什么需要 Agent Platform

过去我们很容易这样理解 Agent：

```text
Prompt
  ↓
LLM
  ↓
Tool Call
  ↓
Result
  ↓
LLM
  ↓
...
```

这个最小循环足够解释一个 Agent Demo，却远远不足以解释一个生产级 Agent 系统。

当 Agent 开始长时间运行、调用越来越多的工具、操作真实业务系统、处理中间文件和大量数据、跨多个 Session 延续工作、动态创建子 Agent、执行生成代码并自主规划和恢复时，真正困难的问题就不再是：

> **怎么让模型调用工具？**

而是：

> **怎么治理一个非确定的智能执行过程？**

本项目希望建立一套足够稳定的 Agent 软件架构，使对话助手、科研助手、知识库、Workflow、Coding Agent、自主智能体等不同产品形态，可以共享同一套底层执行基础设施。

---

# 核心判断

下面是当前研究形成的 12 个核心架构判断。

## 01. 应用形态不等于执行范式

对话、科研助手、知识库、Coding、行业应用，是产品形态。

Direct、Workflow、Agent Loop、程序化工具调用（PTC）、Multi-Agent，是执行范式。

```text
产品形态
Chat · Research · Knowledge Base · Coding
                 │
                 │ 不等于
                 ▼
执行范式
Direct · Workflow · Agent · PTC · Multi-Agent
```

同一个产品可以混合多种执行策略，因此不应该为每一种 Agent 产品重新实现一套 Runtime。

## 02. Workflow 与 Agent 的真正区别，是谁拥有执行控制权

Workflow 中，下一步主要由预定义代码或图决定；Agent 中，下一步主要由模型根据当前上下文动态决定。

```text
Static Workflow
      ↓
Dynamic Workflow / Plan
      ↓
Agent Loop
```

二者更像一条连续谱，而不是截然分开的两套技术。

> **Workflow Graph 是输入；Agent Graph 更接近运行时结果。**

## 03. Runtime 管事实，Harness 管策略

这是整套架构最重要的边界之一。

```text
Business
→ 要完成什么

Harness
→ 当前准备怎么完成

Runtime
→ 实际发生了什么
```

Planner、Todo、Evaluator、Context Strategy、Delegation Strategy、Completion Strategy，都可能随着模型能力提升而变化。

而 Work、Session、Run、Event、State、Action、Result、Artifact、Recovery 这些执行事实应该保持稳定。

> **Runtime 应稳定；Harness 应可替换、可简化，甚至最终消失。**

## 04. Work 承载长期连续性，而不是 Agent

一个长期任务不应该依赖“这个 Agent 永远不能忘记”。真正持久的应该是：

```text
Work
├── Goal
├── Shared Resources
├── Work Frontier
├── Artifacts
├── Workspace
├── Progress
└── Sessions
```

Agent 可以丢失 Context、结束 Session、更换模型或 Harness，甚至被新的 Agent 接管，但 Work 必须继续存在。

> **Agent 可以忘记、退出或者被替换；Work 必须记住。**

## 05. Event 是事实，State 和 Context 都是投影

统一 Runtime 的基本关系：

```text
Action / Result
      ↓
    Event
      ↓
  Event Log
      ↓
    State
```

其中：

```text
Event   → 已经发生的事实
State   → 根据事实计算出的当前视图
Context → 当前模型实际需要看到的工作集
```

因此：

> **Event 是事实，State 是投影，Context 是查询结果。**

Snapshot、Summary、Compaction 都不能反过来成为真实历史。

## 06. Context 是 Working Set，不是整个世界

生产级 Agent 不应该尝试把所有信息永久塞进 Context Window。

更合理的模型是：

```text
Session
State
Memory
Notes
Artifacts
Workspace
Skills
Capabilities
External Resources
        ↓
 Context Builder
        ↓
     Context
```

Context 应该可以丢弃、可以重建，并按照当前 Goal 动态投影、按需加载知识和能力。

> **Context contains a map, not the whole world.**

模型需要的是当前工作的地图，而不是整个世界。

## 07. LLM 应该是控制面，而不是数据面

很多 Agent 系统让模型同时承担推理、编排和数据搬运，结果大量 Token 被消耗在循环、过滤、Join、聚合和格式转换上。

更合理的是：

```text
Agent / Harness
= 执行控制面

Agent Work Environment
= 数据面 + 动作面
```

程序化工具调用（PTC）体现了这种方向：

```text
Model
 ↓ 生成程序
Program
 ├── Tool A
 ├── Tool B
 ├── Loop
 ├── Filter
 └── Aggregate
 ↓
Observation
 ↓
Model
```

> **一个模型推理步骤，可以展开成多个受治理的环境动作。**

## 08. Tool、Skill、MCP、Harness 是四种不同东西

```text
Tool
→ 能做什么动作

Skill
→ 这类任务应该怎么做

MCP
→ 如何连接外部系统

Harness
→ 当前任务现在怎么推进
```

因此：

> **MCP 是连接标准，不是能力设计标准。**

一个后端 API 或 MCP Tool，也不应该直接等于 Agent-facing Tool。

```text
Backend API / MCP
        ↓
Capability Adapter
        ↓
Semantic Capability
        ↓
Agent-facing Tool
```

真正的设计单位应该是对 Agent 有意义的工作能力，而不是后端 API Endpoint。

## 09. Agent 本身可以是动态组装出来的

随着 Skill、Tool、Knowledge、Context 都可以按需加载：

```text
Base Agent
+ Selected Skills
+ Selected Tools
+ Retrieved Knowledge
+ Task Context
        ↓
Effective Agent
```

因此不必为每一种业务场景预先创建一个固定 Agent。平台更应该建设 Capability Catalog、Capability Discovery 和 Runtime Composition，而不是不断增加静态 Agent 类型。

> **Agent 使用 Capability，但不应该拥有 Capability。**

## 10. Multi-Agent 的关键不是 Agent 数量，而是工作前沿

复杂任务并不自动意味着需要 Multi-Agent。只有当任务具备可并行、上下文相对独立、结果可合并、依赖密度较低等特征时，多智能体才真正产生价值。

真正决定并行度的是：

> **当前有多少个可以独立领取、独立推进、独立验证的工作单元。**

即工作前沿（Work Frontier）。

> **Multi-Agent 的核心是 Work Scheduler，而不是 Agent Scheduler。**

同时：

```text
Delegation
→ 传递 Goal

Authorization
→ 单独推导最小权限
```

> **Delegation 不应该默认复制 Authority。**

## 11. Eval 不是测试附件，而是 Capability Specification

对非确定 Agent，仅仅写一个 expected output 通常不够。更合理的基本单位是 Trial：

```text
Task
  ↓
Trial
├── Harness Revision
├── Environment
├── Trace
├── Outcome
└── Grader Results
```

必须区分：

```text
Trace   → Agent 是怎么做的
Outcome → 最终真实结果是什么
```

能力契约同时包含 Goal、Acceptance Criteria、Quality Criteria、Evaluation Contract 和 Evidence Requirement。

> **Harness 说明怎么实现；Eval 说明怎么证明。**

Capability Eval 用于探索能力边界，Regression Eval 用于守住已经获得的能力。

## 12. Agent Security 的本质，是控制 Agent 能触达到多大的世界

模型变得更可靠，并不意味着系统自动更安全。

```text
Deployment Risk
≈ Failure Probability × Blast Radius
```

Prompt、模型训练、Classifier、HITL 可以降低失败概率；真正限制最大后果的，是确定性边界：

```text
Filesystem
Network
Credentials
Capabilities
Data
Memory
Other Agents
External Systems
```

因此：

> **Containment 的本质是 Reachability Control。**

每个 Work、Run、Child Agent 都应该拥有尽可能小的可达世界。

最终授权也不应该只是 `github_access = true`，而应该围绕：

```text
Principal
× Delegation
× Capability
× Resource
× Scope
× Duration
× Work Context
```

构建。

> **治理决定边界画在哪里；基础设施保证 Agent 越不过这条边界。**

---

# Agent Software Stack

上述原则最终形成了当前的七层软件栈：

```text
┌───────────────────────────────────────────────┐
│ L7 业务 / 产品                                │
│ Goal · Project · Business Task                │
├───────────────────────────────────────────────┤
│ L6 能力契约                                   │
│ Acceptance · Quality · Evaluation Contract    │
├───────────────────────────────────────────────┤
│ L5 能力工程                                   │
│ Skill · Tool · Capability Discovery · MCP     │
├───────────────────────────────────────────────┤
│ L4 执行策略                                   │
│ Workflow · Agent Loop · PTC · Multi-Agent     │
├───────────────────────────────────────────────┤
│ L3 统一运行时                                 │
│ Work · Session · Run · Event · State          │
│ Action · Observation · Artifact · Recovery    │
├───────────────────────────────────────────────┤
│ L2 Agent Work Environment                     │
│ Workspace · Execution · Verification          │
│ Capability Proxy · Sandbox                    │
├───────────────────────────────────────────────┤
│ L1 基础设施 / 真实世界                        │
│ API · SaaS · DB · Browser · Files · Compute   │
└───────────────────────────────────────────────┘
```

横向贯穿整个软件栈：

```text
Context / Memory
Evaluation
Observability / Trace
Security / Governance
Registry / Versioning
Budget / Cost
```

每层只回答一个核心问题：

| 层 | 核心问题 |
|---|---|
| 业务 / 产品 | 要完成什么？ |
| 能力契约 | 什么叫真正具备这项能力？ |
| 能力工程 | Agent 可以学什么、做什么？ |
| 执行策略 | 当前任务怎么推进？ |
| 统一运行时 | 实际发生了什么？ |
| 工作环境 | Agent 能观察和作用于什么世界？ |
| 基础设施 | 真正的资源在哪里？ |

---

# 一个更完整的 Agent 心智模型

生产级 Agent 不再只是：

```text
LLM + Tools + Loop
```

而更接近：

```text
业务目标
   ↓
能力契约
   ↓
动态能力组装
   ↓
Harness / 执行策略
   ↓
统一 Runtime
   ↓
Agent Work Environment
   ↓
真实世界
```

同时，Context / Memory、Eval / Verification、Trace / Observability、Security / Governance 贯穿整个执行过程。

> **Agent Platform 本质上是一套智能执行基础设施。**

---

# 为什么做这个项目

Agent 领域正在快速出现新的概念：Agent Loop、Workflow、Harness、Context Engineering、Memory、Skill、Tool、MCP、PTC、Multi-Agent、Eval、Sandbox、Agent Identity。

单独理解每个概念并不困难。困难的是：

> **它们究竟属于哪一层？彼此是什么关系？什么应该成为稳定平台抽象，什么只是当前模型时代的临时脚手架？**

本项目通过持续阅读和分析 Agent 工程实践，逐步建立统一的平台架构。

不是简单整理文章来源，而是保留：

```text
文章来源
   ↓
逐节分析
   ↓
架构推导
   ↓
Agent Platform 演进
```

整个过程。

---

# 研究路线

目前已经系统分析：

1. [Building effective agents](articles/01-building-effective-agents/README.md)
2. [Scaling Managed Agents: Decoupling the brain from the hands](articles/02-scaling-managed-agents/README.md)
3. [Effective context engineering for AI agents](articles/03-effective-context-engineering/README.md)
4. [Effective harnesses for long-running agents](articles/04-effective-harnesses-for-long-running-agents/README.md)
5. [Harness design for long-running application development](articles/05-harness-design-for-long-running-apps/README.md)
6. [How we built our multi-agent research system](articles/06-multi-agent-research-system/README.md)
7. [Building a C compiler with a team of parallel Claudes](articles/07-building-c-compiler/README.md)
8. [Demystifying evals for AI agents](articles/08-demystifying-evals-for-ai-agents/README.md)
9. [Writing effective tools for agents — with agents](articles/09-writing-effective-tools-for-agents/README.md)
10. [Equipping agents for the real world with Agent Skills](articles/10-agent-skills/README.md)
11. [Code execution with MCP: Building more efficient agents](articles/11-code-execution-with-mcp/README.md)
12. [How we contain Claude across products](articles/12-how-we-contain-claude/README.md)

每一篇文章一个目录，每一个核心问题独立成节。

---

# 深入阅读

## 总体架构

[**智能体平台总体架构 →**](architecture/agent-platform.md)

这是当前 Agent Platform 的规范性架构文档，包含：

- 七层软件栈；
- Work / Session / Run 领域模型；
- Event / State；
- Context / Memory / Workspace；
- Skill / Tool / MCP；
- PTC；
- Multi-Agent；
- Eval / Verification；
- Security / Governance；
- Observability；
- Capability Lifecycle。

## 查看架构如何一步步形成

每完成一篇文章，都采用：

```text
文章研究提交
       ↓
架构吸收 / 修正
       ↓
架构演进提交
```

因此可以直接：

```bash
git log -- architecture/agent-platform.md
```

查看整个架构从执行控制、Managed Agents、Context Engineering、Long-running Agents、Multi-Agent、Agent Work Environment、Evaluation、Capability Engineering、PTC 到 Security / Governance 逐步形成的过程。

## 写作规范

- 正文尽可能使用中文；
- 重要英文术语首次出现时保留原词，之后优先使用中文；
- 目录名、文件名、接口、事件类型和代码标识符保持英文；
- 不把我们的架构推导伪装成文章来源；
- 一节只处理一个核心问题。

完整规范见 [docs-style-guide.md](docs-style-guide.md)。

---

# 一句话总结

> **不要把 Agent Platform 理解成一个更复杂的 Agent Loop。**
>
> **它真正要解决的是：如何把非确定的智能执行，变成可以进入生产环境的软件系统。**
