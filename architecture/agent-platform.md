# 智能体平台总体架构

本文档记录 Agent Platform 当前已经形成的规范性架构结论，并随着研究持续演进。

> 当前版本已吸收前十一篇研究。PTC（Programmatic Tool Calling）进一步把 Execution Strategy 与 Execution Environment 分开，并明确 LLM 应主要处于 Control Plane，而数据与动作尽可能留在执行平面。

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
- Harness / 执行策略决定 **当前怎么执行和编排**；
- Runtime 记录 **真实发生了什么**；
- Work Environment 提供 **受治理的数据与动作平面**；
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
   Direct · Workflow · Agent Loop · PTC · Multi-Agent
   Planning · Delegation · Context Strategy · Evaluator

L3 统一运行时
   Work · Session · Run · State · Action · Result · Observation
   Resource · Delegation · Recovery

L2 Agent Work Environment
   Workspace · Programmatic Execution · Shared Resources
   Work Discovery · Ownership · Observation Projection
   Verification · Sandbox · Capability Proxy

L1 基础设施 / 真实世界
   API · MCP · DB · Browser · Files · Compute · SaaS · Devices

横切：
Context / Memory · Trace · Eval · Budget · Data Flow · Governance
```

## 3. 核心设计原则

### 3.1 应用形态与执行范式分离

对话、研究、知识库、Coding 等是应用形态；Direct、Workflow、Agent Loop、PTC、Multi-Agent 等是执行范式。

### 3.2 执行控制权决定 Workflow 与 Agent 的边界

- Workflow：下一步主要由代码或图决定。
- Agent：下一步主要由模型根据当前 Context 动态决定。

### 3.3 Runtime 稳定，Harness 可替换

Harness 是当前模型能力缺口的适应性脚手架，其复杂度必须通过 Eval 证明。

### 3.4 LLM 是 Control Plane，不是 Data Plane

模型负责高价值决策和策略调整；批量数据搬运、循环、过滤、join 和 aggregation 尽量留在 Execution Environment。

```text
Agent / Harness
= Execution Control Plane

Agent Work Environment
= Data + Action Plane
```

### 3.5 One Reasoning Step != One Action

一个模型决策可能直接产生一个 Tool Call，也可能产生一个 Program，而 Program 再展开大量 Actions。因此 Runtime 不绑定 `1 model step = 1 tool call`。

### 3.6 Agent 可以动态组装

```text
Base Agent
+ Selected Skills
+ Selected Tools
+ Retrieved Knowledge
+ Task Context
        ↓
Effective Agent
```

### 3.7 Context 是可重建投影

Context 是当前 Working Set，不是持久事实源。

### 3.8 长期工作连续性不依赖 Agent 连续性

Agent 可以退出、忘记、被替换；Work 必须记住。

## 4. Execution Strategy

### 4.1 执行连续谱

```text
Direct
  ↓
Static Workflow
  ↓
Dynamic Workflow / Plan
  ↓
Agent Loop
  ↓
PTC / Programmatic Orchestration
  ↓
Dynamic Multi-Agent
```

这些不是互斥层级。一个 Multi-Agent Child 内部也可以使用 PTC，一个 Workflow 节点也可以启动 Agent Loop。

### 4.2 Workflow Control Primitives

基础控制原语：Sequence、Branch、Fork / Join、Loop、Dynamic Expansion。

Workflow Graph 是输入表达；Agent Graph 更接近运行时结果。

### 4.3 PTC

PTC 是 Tool Orchestration Mode，而不是 Tool Type。

```text
Direct
Model → Tool → Model → Tool → Model

PTC
Model → Program → many Tools / loops / filters → Observation → Model
```

同一个 Tool 可以同时支持 Direct 和 PTC。

### 4.4 Multi-Agent

使用 Multi-Agent 取决于可并行性、上下文独立性、结果可合并性、依赖密度和协调成本。

Lead Agent = Orchestrator + Global Context Owner。

Agent Team 可以根据 Goal、Capabilities、Knowledge、Permissions、Budget 和 Risk 动态形成。

## 5. Capability Engineering

### 5.1 Capability 分类

```text
Capability
├── Procedural Capability
│   └── Skill
└── Action Capability
    └── Tool
```

### 5.2 Skill、Tool、Harness、MCP

```text
Skill   → 这类任务应该怎么做
Tool    → 能执行什么动作
MCP     → 如何连接外部系统
Harness → 当前任务怎么推进
```

MCP 是连接标准，不是 Capability Design Standard。

### 5.3 Capability Adapter

```text
Backend API / Service
        ↓
Capability Adapter
        ↓
Agent-facing Tool
```

稳定 mechanics 下沉到 Capability，需要智能判断的决策留给 Harness。

### 5.4 Capability Discovery

```text
Capability Catalog
      ↓ discovery
Metadata
      ↓ select
Skill / Tool Loading
      ↓
Execution
```

Discovery 与 Loading 分离。

### 5.5 Skill Progressive Disclosure

Metadata → `SKILL.md` → references / scripts / resources。

Skill-local Script 不自动成为平台 Tool。

### 5.6 Tool Contract

Tool Contract 包括 Identity、Applicability、Semantics、Schema、Usage Guidance、Side Effects 和 Permission / Risk。

### 5.7 Tool Result 与 Observation

Tool 既是 Action Capability，也是 Context Producer。

Result 是真实执行事实；Observation 是面向模型的信息投影。

### 5.8 Eval-driven Capability Engineering

Tool 与 Skill 都必须通过真实 Task、Trial、Trace 和 Regression Eval 迭代。

## 6. Programmatic Execution Runtime

PTC 不应该被实现成一个无限权限 `python` Tool，而需要受治理的 Programmatic Execution Runtime：

```text
Programmatic Execution Runtime
├── Sandbox / Isolation
├── Workspace
├── Capability Proxy
├── Permission Policy
├── Data Flow Policy
├── Resource Budget
├── Secrets Isolation
├── Action Trace
├── Kill / Timeout
└── Recovery
```

### 6.1 Code Permission != Business Capability Permission

允许执行代码，不代表代码自动拥有 GitHub、数据库、Slack 等业务权限。

程序内部仍通过 Capability Proxy 调用受治理 Capability。

```text
Effective Permission
≈ Sandbox Boundary
  ∩ Capability Grant
  ∩ User Permission
  ∩ Task Policy
```

### 6.2 程序内部 Action 必须可观测

Trace 不能只有：

```text
CodeExecutionStarted
CodeExecutionSucceeded
```

而应保留：

```text
Program
├── Action A
├── Action B
├── Action C
├── Policy Decision
├── Retry
└── Result
```

模型步骤、程序和具体 Action 形成层级 Trace。

### 6.3 Program Budget

至少治理：

- max_tool_calls；
- max_runtime；
- max_cost；
- max_parallelism；
- CPU / memory；
- data read / write limits。

Harness 可以生成复杂程序，但 Environment 必须限制其资源上界。

## 7. Data Plane 与 Observation

### 7.1 三类数据

```text
Model-visible Data
→ 可进入 Context

Execution-only Data
→ 程序可处理，但模型不可见

Persistent Resource
→ 写入 Workspace / Resource Store，通过 Ref 使用
```

> **可以允许 Agent 系统处理数据，而不允许模型直接看到这些数据。**

### 7.2 Result → Observation Pipeline

```text
Action
  ↓
Raw Result
  ↓
Transform
├── Filter
├── Join
├── Aggregate
├── Redact
├── Persist
└── Summarize
  ↓
Observation
  ↓
Context
```

Observation Projection 是 Agent Work Environment 与 Context Engineering 的连接点。

### 7.3 Data Flow Policy

Capability Permission 只回答“能不能调用某个动作”，还需要 Data Flow Policy 回答“某类数据能从哪里流向哪里”。

```text
Source
+ Data Classification
+ Destination
+ Capability
+ Purpose / Work Context
      ↓
Allow / Deny / Redact
```

例如：

```text
PII DB → approved CRM       ✓
PII DB → arbitrary LLM      ✗
PII DB → public internet    ✗
```

PTC 尤其依赖确定性的 Data Flow Enforcement，因为中间数据可能完全不经过模型。

## 8. Workspace 与代码生命周期

Workspace 是 Work 的持久工作世界：

```text
Workspace
├── Intermediate Files
├── Generated Programs
├── Checkpoints
├── Data Artifacts
└── Progress
```

生成代码分三层生命周期：

```text
Ephemeral Code
→ 当前 Run

Workspace Code
→ 当前 Work

Promoted Capability
→ 跨 Work 平台资产
```

晋升流程：

```text
Ephemeral
   ↓ useful
Workspace
   ↓ reusable
Capability Candidate
   ↓ Eval / Security / Review
Promoted Capability
```

Agent 可以提出 Candidate，但不能在生产 Session 内直接自发布为全局可信 Capability。

## 9. Work / Session / Run

### 9.1 Work

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

### 9.2 Session

Session 是一个 Agent 与 Work 的相对连续认知 / 执行关系。

### 9.3 Run

Run 是 Runtime 被触发后，在一个 Session 内发生的一次连续执行片段。

### 9.4 Parent / Child Session

自治 Sub-agent 需要独立目标、多轮 Context、Artifact 和 Recovery 时使用 Child Session；Agent-as-Tool 是 Parent 中一次 Action。

## 10. Agent Work Environment

```text
Agent Work Environment
├── Shared Resources
├── Local Workspace
├── Programmatic Execution
├── Work Discovery
├── Ownership / Lease
├── Observation Projection
├── Verification
├── Feedback / Oracle
├── Capability Proxy
└── Sandbox / Isolation
```

### 10.1 Work Frontier

当前独立、可领取、可验证的 Work Item 集合决定有效并行度。

> **Multi-Agent 的关键是 Work Scheduler，不是 Agent Scheduler。**

### 10.2 Environment Engineering

环境负责把原始结果转化为高信号 Observation，并提供可行动反馈。

## 11. Context、Memory 与持久资源

### 11.1 Context Builder

```text
Session / State / Memory / Notes / Artifacts / Workspace / Capabilities
                              ↓
                        Context Builder
                              ↓
                           Context
```

### 11.2 Context 是 Working Set

稳定 Policy / Agent Definition / Capability Metadata 前置，完整 Tool / Skill、外部知识和数据按需加载。

### 11.3 Compaction

Compaction 改变模型看到什么，不改变真实历史。

### 11.4 资源语义

Notes / Todo 是主观工作认知；Memory 是跨时间信息；Workspace 是持久工作状态；Artifact 是正式结果。

## 12. Eval Architecture

Trial 是 Agent Eval 的基本单位：

```text
Task
  ↓
Trial
├── Harness Revision
├── Capability Revisions
├── Environment Revision
├── Trace
├── Outcome
└── Grader Results
```

Evaluation Contract 由 Criterion、Evidence Source、Grader、Threshold / Criticality、Aggregation 组成。

- pass@k：能力 / 搜索潜力；
- pass^k：可靠性；
- Capability Eval：探索能力边界；
- Regression Eval：守住能力。

Outcome 是事实，Score 是 Measurement Projection。

Eval Infrastructure 属于平台能力；Eval Content 属于 Capability Asset。

## 13. Verification 与 Acceptance

Execution State、Verification State、Acceptance State、Publish / Deploy State 分离。

Verification Ladder：Local Checks → Regression → Representative Workloads → Integration → Production-like Verification。

## 14. Recovery 与 Escalation

Recovery 解决暂时、可恢复故障；Escalation 解决当前能力边界。

## 15. Effort 与预算

Reasoning、Delegation、Action、Search、Evaluation、Time、Cost 以及 Program Resource 都是可治理预算。

Plan 是可变假设；Budget 是硬约束。

## 16. Harness 工程

Harness Revision → Trial → Trace + Outcome → Eval → Failure Analysis → Harness Revision。

Harness 版本与 Session 生命周期分离。

## 17. Governance

Human 逐渐从 Execution Path 移向 Governance Plane，负责 Goal、Acceptance、Risk Boundary、Escalation 和最终 Publish / Deploy Decision。

Capability Candidate 晋升、Data Flow Policy、Program Permission 也属于 Governance 的治理范围。

## 18. 当前架构不变量

1. **应用形态不等于执行范式。**
2. **Workflow 与 Agent 的核心区别是执行控制权归属。**
3. **Runtime 承载持久执行事实，不固化控制策略。**
4. **Runtime 稳定，Harness 可替换、可简化甚至消失。**
5. **PTC 是 Execution Strategy / Tool Orchestration Mode，不是 Tool Type。**
6. **LLM 应作为 Execution Control Plane，而不是承担大规模 Data Transportation。**
7. **One Reasoning Step 可以展开 many Environment Actions。**
8. **Code Permission 不等于 Business Capability Permission。**
9. **程序内部 Action 仍必须经过授权、Budget、Trace 和 Audit。**
10. **Result 是执行事实，Observation 是面向模型的信息投影。**
11. **Execution-only Data 可以被程序处理，而不进入 Model Context。**
12. **Capability Policy 与 Data Flow Policy 是两个不同治理维度。**
13. **生成代码按 Run → Work → Platform 分层生命周期管理。**
14. **从 Workspace Code 晋升为共享 Capability 必须经过 Eval、安全和评审。**
15. **Tool 是行动能力，Skill 是程序性知识，MCP 是连接标准，Harness 是当前执行策略。**
16. **Agent 可以由 Base Agent + Skills + Tools + Knowledge + Task Context 动态组装。**
17. **Context 是可重建投影和当前 Working Set。**
18. **Work 是长期连续性的载体。**
19. **Multi-Agent 的关键调度对象是 Work Frontier。**
20. **Eval 是可执行 Capability Specification。**
