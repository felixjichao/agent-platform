# 智能体平台总体架构

本文档记录 Agent Platform 当前已经形成的规范性架构结论，并随着研究持续演进。

> 当前版本已吸收前十篇研究。Capability Engineering 进一步拆分出程序性能力（Skill）与行动能力（Tool），并形成运行时动态组装 Agent 的模型。

## 1. 架构主张

Agent Platform 不按产品形态分别建设执行内核，而是围绕七层稳定边界组织：

```text
L7 业务 / 产品
L6 能力契约
L5 能力工程
L4 执行策略
L3 统一运行时
L2 Agent Work Environment
L1 基础设施 / 真实世界
```

关键职责：

- 业务 / 产品决定 **要完成什么**；
- 能力契约定义 **能力是什么、怎样证明**；
- 能力工程提供 **Agent 能发现、学习和调用什么能力**；
- Harness / 执行策略决定 **当前怎么执行**；
- Runtime 记录 **真实发生了什么**；
- Work Environment 决定 **Agent 如何观察、行动和验证**；
- Eval / Trace 反馈 **做得怎样以及为什么**。

## 2. 七层软件栈

```text
L7 业务 / 产品
   Goal · Project · Requirement · Application

L6 能力契约
   Capability Definition
   Acceptance Criteria · Quality Criteria · Evaluation Contract

L5 能力工程
   Capability Catalog · Taxonomy · Discovery
   Skill · Tool · Capability Adapter · MCP Binding

L4 执行策略 / Harness
   Direct · Workflow · Agent Loop · Multi-Agent
   Planning · Delegation · Context Strategy · Evaluator

L3 统一运行时
   Work · Session · Run · State · Action · Result
   Resource · Delegation · Recovery

L2 Agent Work Environment
   Workspace · Shared Resources · Work Discovery
   Ownership · Observation · Verification · Sandbox

L1 基础设施 / 真实世界
   API · MCP · DB · Browser · Files · Compute · SaaS · Devices

横切：
Context / Memory · Trace · Eval · Budget · Governance
```

## 3. 核心设计原则

### 3.1 应用形态与执行范式分离

对话、研究、知识库、Coding 等是应用形态；Direct、Workflow、Agent Loop、Multi-Agent 等是执行范式。

### 3.2 执行控制权决定 Workflow 与 Agent 的边界

- Workflow：下一步主要由代码或图决定。
- Agent：下一步主要由模型根据当前 Context 动态决定。

### 3.3 Runtime 稳定，Harness 可替换

Harness 是当前模型能力缺口的适应性脚手架，其复杂度必须通过 Eval 证明。

### 3.4 Agent 可以动态组装

Agent 不需要永久拥有一套静态 Tool / Skill 全集。有效 Agent 可以在运行时被组装：

```text
Base Agent
+ Selected Skills
+ Selected Tools
+ Retrieved Knowledge
+ Task Context
        ↓
Effective Agent
```

### 3.5 Context 是可重建投影

Context 是当前 Working Set，不是持久事实源。

### 3.6 长期工作连续性不依赖 Agent 连续性

Agent 可以退出、忘记、被替换；Work 必须记住。

### 3.7 Outcome 是事实，Eval Score 是测量投影

评分必须可追溯到 Task、Evidence、Grader 和版本化 Measurement Configuration。

## 4. Capability Engineering

### 4.1 Capability 分类

当前至少区分：

```text
Capability
├── Procedural Capability
│   └── Skill
│
└── Action Capability
    └── Tool
```

未来还可以增加 Knowledge Capability、Agent Capability 等类型，但核心是保持**语义能力**与具体实现解耦。

### 4.2 Skill、Tool、Harness

```text
Tool
→ Agent 能做什么动作？

Skill
→ 这类任务通常应该怎么做？

Harness
→ 当前任务此刻怎么推进？
```

> **Tool 是行动能力，Skill 是程序性知识，Harness 是当前执行策略。**

### 4.3 Capability Adapter

```text
Backend API / Service
        ↓
Capability Adapter
        ↓
Agent-facing Tool
```

后端接口粒度不等于 Agent Capability 粒度。Adapter 负责把稳定 mechanics 下沉，给 Agent 暴露有业务语义的行动边界。

### 4.4 Capability Taxonomy

```text
Domain
  ↓
Resource
  ↓
Semantic Capability
  ↓
Concrete Tool / Skill
```

每个 Capability 应明确 What、When、When NOT、Neighbor / Boundary。

### 4.5 Capability Discovery

随着能力数量扩大，平台不再把全量定义注入 Context：

```text
Capability Discovery
      ↓
Metadata Selection
      ↓
Skill / Tool Loading
      ↓
Execution
```

> **Discovery != Loading。**

Capability Catalog 是全量资产目录，Context 只承载当前需要的子集。

### 4.6 Progressive Disclosure for Skill

```text
Level 1
Skill Metadata
name + description
      ↓
Level 2
SKILL.md
      ↓
Level 3
references / scripts / resources
```

Metadata 是 Knowledge Routing Prompt。它既要帮助正确激活，也要支持“不该激活时不激活”。

### 4.7 Skill Anatomy

```text
Skill
├── Instructions
├── Scripts
├── References
└── Resources
```

Skill-local Script 用于封装某个 Skill 内稳定、局部的 deterministic mechanics；它不自动成为平台全局 Tool。

### 4.8 Skill Information Architecture

`SKILL.md` 不应长成巨型手册。它应主要包含：

- 核心原则；
- 决策路径；
- Knowledge Map；
- Resource Entry Points。

深入内容拆到 references。拆分依据优先是 Context Co-occurrence，而不是传统文档目录。

### 4.9 Tool Contract

```text
Tool Contract
├── Identity
├── Applicability
├── Semantics
├── Input / Output Schema
├── Usage Guidance
├── Side Effects
└── Permission / Risk
```

Schema 说明机器允许什么；Guidance 说明 Agent 怎样才能用对。

### 4.10 Result 与 Observation

```text
Action
  ↓
Raw Result
  ↓
Transform / Filter / Summarize / Reference
  ↓
Observation
  ↓
Context
```

Result 是执行事实；Observation 是面向模型的信息投影。Tool 同时是 Action Capability 和 Context Producer。

### 4.11 Agentic Boundary

> **Deterministic mechanics 下沉到 Capability；uncertain decisions 留给 Harness。**

Tool 太原子会把机械 orchestration 推给 Agent；太巨大则会把真正需要智能判断的决策藏进黑盒 Workflow。

### 4.12 Skill 与 MCP

```text
MCP
→ 怎么连接外部系统？

Tool
→ 可以执行什么动作？

Skill
→ 应该怎样完成一类任务？
```

MCP 是连接标准，不是 Capability Design Standard。

推荐绑定关系：

```text
Skill
  ↓ requires
Semantic Capability
  ↓ binds
Tool
  ↓ implemented via
MCP / API / Local Script
```

Skill 应尽量依赖语义能力，而不是硬编码某个具体 MCP Server。

### 4.13 Skill / Tool Registry

> **Agent uses capability; Agent does not own capability.**

Skill / Tool 都应具备：

- independent；
- portable；
- versioned；
- discoverable；
- composable；
- governed。

Agent Definition 逐渐从“静态能力全集”转向“基础身份 + 动态能力发现”。

### 4.14 Eval-driven Capability Engineering

Tool：

```text
Real Tasks
→ Agent Trials
→ Trace Mining
→ Tool-use Smells
→ Tool Revision
→ Regression Eval
```

Skill：

```text
Capability Gap
→ Skill Candidate
→ Activation / Restraint / Outcome Eval
→ Publish / Revise
```

常见 Skill Failure：Discovery、False Activation、Navigation、Instruction、Over-contexting、Procedure Failure。

## 5. Capability Supply Chain 与权限边界

Skill 可以包含 Instructions、Scripts 和 Dependencies，因此是可执行供应链资产。

必须区分：

```text
Install
≠ Activate
≠ Execute Script
≠ Grant Capability
```

Skill 可以声明 Requirement，但不能自行扩大权限：

```text
Effective Permission
≈ Skill Requirement
  ∩ Agent Policy
  ∩ User Permission
  ∩ Task Need
```

Skill Revision 和 Tool Revision 都需要固定版本，使 Recovery、Audit 和 Eval 可以重现当时真正使用的能力。

## 6. Work / Session / Run

### 6.1 Work

```text
Work / Project
├── Goal
├── Capability / Acceptance Contract
├── Shared Resources
├── Work Frontier
├── Artifacts
├── Environment / Workspace
├── Long-term Progress
└── Sessions
```

Work 是长期目标与共享世界的载体。

### 6.2 Session

Session 是一个 Agent 与 Work 的相对连续认知 / 执行关系。

### 6.3 Run

Run 是 Runtime 被触发后，在一个 Session 内发生的一次连续执行片段。

### 6.4 Parent / Child Session

需要独立目标、多轮 Context、Artifact 和 Recovery 的自治 Sub-agent 使用 Child Session；短生命周期 Agent-as-Tool 是 Parent 中的一次 Action。

## 7. Agent Work Environment

```text
Agent Work Environment
├── Shared Resources
├── Local Workspace
├── Work Discovery
├── Ownership / Lease
├── Observation
├── Verification
├── Feedback / Oracle
└── Artifacts / Progress
```

### 7.1 Work Frontier

Work Frontier 是当前独立、可领取、可验证的 Work Item 集合。

> **Effective Parallelism ≈ Independent Work Fronts。**

### 7.2 Environment Engineering

环境负责把原始结果转化为高信号 Observation，并提供可行动反馈。

## 8. Execution Strategy

### 8.1 连续谱

```text
Direct
  ↓
Static Workflow
  ↓
Dynamic Workflow / Plan
  ↓
Agent Loop
  ↓
Dynamic Multi-Agent
```

### 8.2 Workflow Control Primitives

Sequence、Branch、Fork / Join、Loop、Dynamic Expansion。

Workflow Graph 是输入表达；Agent Graph 更接近运行时结果。

### 8.3 Multi-Agent

使用 Multi-Agent 取决于可并行性、上下文独立性、结果可合并性、依赖密度和协调成本。

Lead Agent = Orchestrator + Global Context Owner。

Agent Team 可以根据 Goal、Capabilities、Knowledge、Permissions、Budget 和 Risk 动态形成。

## 9. Context、Memory 与持久资源

### 9.1 Context Builder

```text
Session / State / Memory / Notes / Artifacts / Workspace / Capabilities
                              ↓
                        Context Builder
                              ↓
                           Context
```

### 9.2 Context 是 Working Set

稳定 System / Policy / Capability Metadata 适合前置，稀疏知识、完整 Tool / Skill 内容和外部数据适合 JIT 加载。

### 9.3 Compaction

Compaction 改变模型看到什么，不改变真实历史。摘要是派生资源。

### 9.4 资源语义

- Notes / Todo：当前主观工作认知；
- Memory：跨时间保留并召回的信息；
- Workspace：Work 的持久工作状态；
- Artifact：正式结果或交付物。

## 10. Eval Architecture

Trial 是 Agent Eval 的基本单位。

```text
Eval Suite
   └── Task
        └── Trial
             ├── Harness Revision
             ├── Capability Revisions
             ├── Environment Revision
             ├── Trace
             ├── Outcome
             └── Grader Results
```

Evaluation Contract 由 Criterion、Evidence Source、Grader、Threshold / Criticality 和 Aggregation 组成。

- pass@k 更接近能力 / 搜索潜力；
- pass^k 更接近可靠性；
- Capability Eval 探索能力边界；
- Regression Eval 守住已获得能力。

Eval Infrastructure 属于平台能力，Eval Content 属于 Capability Asset。

> **Harness → How to implement；Eval → How to prove。**

## 11. Verification 与 Acceptance

Execution State、Verification State、Acceptance State、Publish / Deploy State 分离。

Verification Ladder：Local Checks → Regression → Representative Workloads → Integration → Production-like Verification。

## 12. Recovery 与 Escalation

Recovery 解决暂时、可恢复故障；Escalation 解决当前能力边界。

## 13. Effort 与预算

Reasoning、Delegation、Action、Search、Evaluation、Time 和 Cost 都是可治理预算。Plan 是可变假设，Budget 是硬约束。

## 14. Harness 工程

Harness Revision → Trial → Trace + Outcome → Eval → Failure Analysis → Harness Revision。

Harness 版本与 Session 生命周期分离。

## 15. Governance

Human 逐渐从 Execution Path 移向 Governance Plane，负责 Goal、Acceptance、Risk Boundary、Escalation 和最终 Publish / Deploy Decision。

## 16. 当前架构不变量

1. **应用形态不等于执行范式。**
2. **Workflow 与 Agent 的核心区别是执行控制权归属。**
3. **Runtime 承载持久执行事实，不固化控制策略。**
4. **Runtime 稳定，Harness 可替换、可简化甚至消失。**
5. **Agent 可以由 Base Agent + Skills + Tools + Knowledge + Task Context 动态组装。**
6. **Tool 是行动能力，Skill 是程序性知识，Harness 是当前执行策略。**
7. **MCP 是连接标准，不是 Capability Design Standard。**
8. **API 不等于 Agent Capability；Capability Adapter 负责建立 Agent-facing Tool。**
9. **Capability Discovery 与 Loading 分离，避免全量 Tool / Skill 永久进入 Context。**
10. **Skill 是可执行供应链资产；Install、Activate、Execute、Grant 是不同阶段。**
11. **Deterministic mechanics 下沉到 Capability，uncertain decisions 留给 Harness。**
12. **Skill / Tool Engineering 必须由真实 Task、Trace 和 Eval 驱动。**
13. **Context 是可重建投影和当前 Working Set。**
14. **Work 是长期连续性的载体。**
15. **Work、Session、Run 分别承载长期工作、Agent 连续关系和一次连续执行。**
16. **Multi-Agent 的关键调度对象是 Work Frontier。**
17. **Agent Work Environment 同时支持工作发现、行动、观测和验证。**
18. **Trial 是 Agent Eval 的基本单位。**
19. **Outcome 是事实，Eval Score 是 Measurement Projection。**
20. **Eval 是可执行 Capability Specification。**
