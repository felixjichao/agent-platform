# 智能体平台总体架构

本文档记录 Agent Platform 当前已经形成的规范性架构结论，并随着研究持续演进。

> 当前版本已吸收前九篇研究。Tool Engineering 使 Capability Engineering 成为独立架构层，平台开始从“Tool Registry”升级为“能力空间设计与发现”。

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
- 能力工程提供 **Agent 可以发现和使用什么能力**；
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
   Capability Taxonomy · Discovery · Tool · Capability Adapter

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

### 3.4 Capability 与 Backend API 分离

> **API atomicity != Agent capability granularity。**

后端接口通过 Capability Adapter 转化成 Agent-facing Tool。平台不把外部 API 目录直接暴露成 Agent 决策空间。

### 3.5 Context 是可重建投影

Context 是当前 Working Set，不是持久事实源。

### 3.6 长期工作连续性不依赖 Agent 连续性

Agent 可以退出、忘记、被替换；Work 必须记住。

### 3.7 Outcome 是事实，Eval Score 是测量投影

所有评分必须可追溯到 Task、Evidence、Grader 和版本化的 Measurement Configuration。

## 4. Capability Engineering

### 4.1 Capability Adapter

```text
Backend API / Service
        ↓
Capability Adapter
        ↓
Agent-facing Tool
```

Adapter 可以负责：

- 合并低层 API 调用；
- 稳定默认值；
- 分页；
- 参数收敛；
- 结果转换；
- 错误恢复提示。

目标是建立 Agent 可理解、可选择、可组合的语义能力。

### 4.2 Capability Taxonomy

Tool Registry 本质上定义 Agent 的决策空间。能力应按语义组织：

```text
Domain
  ↓
Resource
  ↓
Capability
  ↓
Concrete Tool
```

每个 Capability 应明确：

- What；
- When；
- When NOT；
- Neighbor / Boundary。

> **Tool Design 是接口设计；Capability Design 是决策空间设计。**

### 4.3 Tool Contract

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

### 4.4 Tool Result 与 Observation

必须区分：

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

- **Result**：真实执行事实；
- **Observation**：模型可消费的信息投影。

Tool 因而同时是 Action Capability 和 Context Producer。

### 4.5 Output Policy

Agent-facing Observation 应考虑：

- relevance；
- volume；
- pagination；
- truncation；
- Resource Ref；
- navigation；
- actionable error guidance。

### 4.6 Namespacing 与 Capability Discovery

Namespacing 提供能力空间导航：

```text
Goal
 ↓
Domain
 ↓
Resource
 ↓
Operation
```

工具规模扩大以后，流程从：

```text
Tool Selection
```

升级为：

```text
Capability Discovery
      ↓
Tool Definition Loading
      ↓
Tool Selection
```

全量 Registry 与当前 Context 必须解耦，Tool Definition 支持即时加载。

### 4.7 Agentic Boundary

两个极端都应避免：

- 太原子：把稳定机械 orchestration 留给 Agent；
- 太巨大：把需要 Agent 判断的业务决策封装进黑盒 Workflow Tool。

正确边界：

> **Deterministic mechanics 下沉到 Capability；uncertain decisions 留给 Harness。**

### 4.8 Eval-driven Tool Engineering

```text
Real Tasks
   ↓
Agent Trials
   ↓
Trace Mining
   ↓
Tool-use Smells
   ↓
Tool Revision
   ↓
Held-out / Regression Eval
```

Tool Correctness 不等于 Tool Effectiveness。工具是否真正有效，要看 Agent 能否在真实 Task 中发现、选择、调用和理解，并最终改善 Outcome。

## 5. Work / Session / Run

### 5.1 Work

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

### 5.2 Session

Session 是一个 Agent 与 Work 的相对连续认知 / 执行关系。同一 Work 可以包含多个顺序或并行 Session。

### 5.3 Run

Run 是 Runtime 被触发后，在一个 Session 内发生的一次连续执行片段。

### 5.4 Parent / Child Session

需要独立目标、多轮 Context、Artifact 和 Recovery 的自治 Sub-agent 使用 Child Session；短生命周期 Agent-as-Tool 是 Parent 中的一次 Action。

## 6. Agent Work Environment

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

### 6.1 Work Frontier

Work Frontier 是当前独立、可领取、可验证的 Work Item 集合。

> **Effective Parallelism ≈ Independent Work Fronts。**

### 6.2 Environment Engineering

环境负责把原始结果转化为高信号 Observation，并提供可行动的反馈。

## 7. Execution Strategy

### 7.1 连续谱

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

### 7.2 Workflow Control Primitives

基础控制原语包括 Sequence、Branch、Fork / Join、Loop、Dynamic Expansion。

Workflow Graph 是输入表达；Agent Graph 更接近运行时结果。

### 7.3 Multi-Agent

是否使用 Multi-Agent 取决于可并行性、上下文独立性、结果可合并性、依赖密度和协调成本。

Lead Agent = Orchestrator + Global Context Owner。

Agent Team 可以根据 Goal、Capabilities、Knowledge、Permissions、Budget 和 Risk 动态形成。

需要 Local Recovery + Global Reconciliation，并区分 Delegation Concurrency 与 Action Concurrency。

## 8. Context、Memory 与持久资源

### 8.1 Context Builder

```text
Session / State / Memory / Notes / Artifacts / Workspace / Capabilities
                              ↓
                        Context Builder
                              ↓
                           Context
```

### 8.2 Context 是 Working Set

稳定 System / Policy / Capability Metadata 适合前置，稀疏知识、完整 Tool Definitions 和外部数据适合 JIT 加载。

### 8.3 Compaction

Compaction 改变模型看到什么，不改变真实历史。摘要是派生资源。

### 8.4 资源语义

- Notes / Todo：当前主观工作认知；
- Memory：跨时间保留并召回的信息；
- Workspace：Work 的持久工作状态；
- Artifact：正式结果或交付物。

## 9. Eval Architecture

### 9.1 基本关系

```text
Eval Suite
   └── Task
        └── Trial
             ├── Harness Revision
             ├── Environment Revision
             ├── Trace
             ├── Outcome
             └── Grader Results
```

Trial 是 Agent Eval 的基本单位。

### 9.2 Evaluation Contract

Criterion、Evidence Source、Grader、Threshold / Criticality 和 Aggregation 分开建模。

### 9.3 多 Trial

- pass@k：能力 / 搜索潜力；
- pass^k：可靠性。

### 9.4 Capability Eval 与 Regression Eval

Capability Eval 探索新的能力边界；Regression Eval 守住已经证明的能力。

### 9.5 Eval Infrastructure vs Content

平台提供 Runner、Environment、Trace、Grader SDK、Statistics、Versioning；Domain Owner 维护 Tasks、Criteria、Rubrics、Reference Solutions、Failure Cases 和 Domain Graders。

### 9.6 Eval 是 Capability Specification

```text
Harness → How to implement
Eval    → How to prove
```

## 10. Verification 与 Acceptance

Execution State、Verification State、Acceptance State、Publish / Deploy State 分离。

Verification Ladder：Local Checks → Regression → Representative Workloads → Integration → Production-like Verification。

Verifier 应提供 Differential Oracle，而不只是 pass / fail。

## 11. Recovery 与 Escalation

Recovery 解决暂时、可恢复故障；Escalation 解决当前能力边界。

## 12. Effort 与预算

Reasoning、Delegation、Action、Search、Evaluation、Time 和 Cost 都是可治理预算。Plan 是可变假设，Budget 是硬约束。

## 13. Harness 工程

Harness Revision → Trial → Trace + Outcome → Eval → Failure Analysis → Harness Revision。

Harness 版本与 Session 生命周期分离。

## 14. Governance

Human 逐渐从 Execution Path 移向 Governance Plane，负责 Goal、Acceptance、Risk Boundary、Escalation 和最终 Publish / Deploy Decision。

## 15. 当前架构不变量

1. **应用形态不等于执行范式。**
2. **Workflow 与 Agent 的核心区别是执行控制权归属。**
3. **Runtime 承载持久执行事实，不固化控制策略。**
4. **Runtime 稳定，Harness 可替换、可简化甚至消失。**
5. **API 不等于 Agent Capability；Capability Adapter 负责建立 Agent-facing Tool。**
6. **Tool Space 是 Agent 决策空间，Capability Taxonomy 与 Boundary 会直接影响 Agent 能力。**
7. **Tool Result 是执行事实，Observation 是面向模型的投影。**
8. **Deterministic mechanics 下沉到 Capability，uncertain decisions 留给 Harness。**
9. **Capability Discovery 与 Tool Loading 分离，避免全量 Tool Definition 永久进入 Context。**
10. **Tool Engineering 必须由真实 Task、Trace 和 Eval 驱动。**
11. **Context 是可重建投影和当前 Working Set。**
12. **Work 是长期连续性的载体。**
13. **Work、Session、Run 分别承载长期工作、Agent 连续关系和一次连续执行。**
14. **Multi-Agent 的关键调度对象是 Work Frontier。**
15. **Agent Work Environment 同时支持工作发现、行动、观测和验证。**
16. **Plan 负责怎么做，Evaluation Contract 负责如何证明已经做成。**
17. **Trial 是 Agent Eval 的基本单位。**
18. **Outcome 是事实，Eval Score 是 Measurement Projection。**
19. **Eval 是可执行 Capability Specification。**
20. **Execution、Verification、Acceptance 和 Publish 状态不能混为一体。**
