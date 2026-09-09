# 智能体平台总体架构

本文档记录 Agent Platform 当前已经形成的规范性架构结论，并随着研究持续演进。

> 当前版本已吸收前六篇研究，新增了多智能体适用条件、Parent / Child Session、动态团队形成、分层并发与委托恢复等结论。

## 1. 架构主张

Agent Platform 不按“对话 Agent、科研 Agent、知识库 Agent、工作流 Agent”等产品形态分别建设执行内核，而是围绕稳定的平台边界组织：

```text
业务 / 产品
    ↓
能力目标 / 验收要求
    ↓
执行策略 / Harness
    ↓
统一运行时
    ↓
Execution Environment
    ↓
真实世界
```

其中：

- 业务 / 产品决定要完成什么；
- Harness 决定当前怎么完成；
- Evaluation Contract 决定怎样证明完成；
- Runtime 保存真实执行事实并支持恢复；
- Execution Environment 负责真正观察和作用于外部世界。

Multi-Agent 是执行策略之一，不是独立的平台内核。

## 2. 核心设计原则

### 2.1 应用形态与执行范式分离

对话、研究、知识库、Coding 等是应用形态；Direct、Workflow、Agent Loop、Multi-Agent 等是执行范式。

### 2.2 执行控制权决定 Workflow 与 Agent 的边界

- Workflow：下一步主要由代码或图决定。
- Agent：下一步主要由模型基于当前 Context 动态决定。

### 2.3 执行方式是一条连续谱

```text
Direct
  ↓
静态 Workflow
  ↓
动态 Workflow / Plan
  ↓
Agent Loop
  ↓
Dynamic Multi-Agent Topology
```

最后一层不是“必然更高级”，而是在任务可并行且值得承担协调成本时才使用。

### 2.4 Runtime 稳定，Harness 可替换

Harness 是对当前模型能力缺口的适应性脚手架，Planner、Evaluator、Context Reset、Delegation Strategy 等都应允许版本化、实验、替换和删除。

### 2.5 Context 是可重建投影

> **Session 追加事实，Context 选择性投影。**

Context 是当前 Working Set，不是持久事实源。

### 2.6 长任务依靠恢复而不是无限 Context

持续工作依赖 Durable State、Handoff、Workspace 和 Recovery。

### 2.7 Execution State 与 Acceptance State 分离

生成结束不等于验收通过。Execution、Verification 和 Acceptance 必须有独立语义。

### 2.8 Delegation 先传递目标，不等于复制整个执行主体

Child Agent 应拿到完成局部目标所需的最小 Context、Budget 和能力，而不是无条件复制 Parent 的全部上下文和状态。

## 3. 当前软件栈

```text
L6 业务 / 产品
   Goal · Requirement · Application

L5 能力契约
   Acceptance Criteria · Quality Criteria · Evaluation Contract

L4 执行策略 / Harness
   Direct · Workflow · Agent Loop · Multi-Agent
   Planning · Delegation · Context Strategy · Bootstrap · Evaluator

L3 统一运行时
   Session · State · Action · Result · Resource · Recovery · Delegation

L2 执行环境
   Workspace · Sandbox · API · MCP · DB · Browser · Filesystem

L1 基础设施 / 真实世界
   Compute · SaaS · Data · Devices

横切：Context / Memory · Trace · Budget
```

## 4. 核心领域边界

### 4.1 Session

Session 是一个 Agent 持续执行关系中的持久历史容器，回答“发生过什么”。它不等于聊天记录或 Context Window。

### 4.2 Parent / Child Session

只有形成独立执行生命周期的 Sub-agent 才需要 Child Session：

```text
Parent Session
   │
   │ Delegation
   ▼
Child Session
   ├── Local Goal
   ├── Local Context
   ├── Local Actions
   ├── Local Artifacts
   └── Result / Failure
```

Parent 保留全局目标和综合责任，Child 只处理局部工作。

### 4.3 Agent-as-Tool

如果只是短生命周期、聚焦调用且不需要独立恢复，则作为 Parent Session 中的一次 Action，而不是创建 Child Session。

### 4.4 State

State 是根据持久事实形成的当前执行视图，用于快速回答“现在是什么状态”。

### 4.5 Context

Context 由多个来源动态投影：

```text
Session / State / Memory / Notes / Artifacts / Workspace
                         ↓
                   Context Builder
                         ↓
                      Context
```

### 4.6 Harness

Harness 负责当前任务如何推进，可以包含：

- Planner；
- Delegator / Orchestrator；
- Evaluator；
- Context Strategy；
- Bootstrap；
- Handoff；
- Completion / Escalation Strategy。

### 4.7 Execution Environment

执行环境描述 Agent 实际可以观察和操作的世界。Sandbox 是其中一种实现。

### 4.8 Recovery

Recovery 负责恢复执行环境、加载持久资源、重建状态并重新校验 Ground Truth。

## 5. Multi-Agent 执行模型

### 5.1 适用条件

是否使用 Multi-Agent 应根据：

```text
Multi-Agent Value
≈ 可并行性
 + 上下文独立性
 + 结果可合并性
 - 依赖密度
 - 协调成本
```

任务复杂本身不是理由。

### 5.2 Lead Agent

Lead Agent 承担：

- 全局目标所有权；
- 全局 Context 管理；
- 工作拆解和委托；
- 覆盖度判断；
- Child 结果协调；
- 最终综合。

因此可以概括为：

> **Lead Agent = Orchestrator + Global Context Owner。**

### 5.3 Dynamic Team Formation

默认不要求用户手工建立固定 Team Graph。Harness 可以根据：

```text
Goal
+ Capabilities
+ Knowledge
+ Permissions
+ Budget
+ Risk
      ↓
Execution Strategy
      ↓
Single / Workflow / Multi-Agent / Hybrid
```

如果选择 Multi-Agent，再动态决定角色、数量、子目标和并行度。

> **Agent Team itself can be runtime output.**

### 5.4 Local Recovery + Global Reconciliation

```text
Child Failure
   ↓
Local Recovery / Retry
   ↓
Result or Failure State
   ↓
Parent Reconciliation
   ↓
Global Plan Update
```

Child 局部失败不应强迫整个 Work 重跑，但任何局部状态变化都可能要求 Parent 重新协调全局计划。

### 5.5 两层并发

必须区分：

- **Delegation Concurrency**：多少 Agent 同时工作；
- **Action Concurrency**：单个 Agent 内多少 Tool / Action 同时执行。

二者拥有不同的预算、背压和失败语义。

### 5.6 Async Delegation

长任务中的 Parent 不应该必须阻塞等待 Child 返回。Delegation 更适合成为持久、事件驱动关系：

```text
Parent delegates
    ↓
Child running
    ↓
Parent may continue / pause
    ↓
Child emits completion event
    ↓
Parent reconcile
```

## 6. Effort 与预算

Effort 不只是模型 reasoning level，而是一组资源预算：

```text
Effort Budget
├── Reasoning Budget
├── Delegation Budget
├── Action / Tool Budget
├── Search Budget
├── Evaluation Budget
├── Time Budget
└── Cost Budget
```

Harness 可以根据任务动态分配 effort，但不能越过平台给定的总预算。

Plan 是可变假设；Budget 是硬约束。系统持久化关键决策、资源使用和证据，不持久化完整 private reasoning。

## 7. 能力契约与验收

### 7.1 Plan 与 Evaluation Contract

```text
Plan              → How to do
Evaluation Contract → How to prove it is done
```

### 7.2 Acceptance Criteria 与 Quality Criteria

- Acceptance Criteria：最低什么条件满足才允许结束。
- Quality Criteria：结果完成得有多好。

### 7.3 Evaluation Contract

```text
Evaluation Contract
├── Criterion
├── Evidence
├── Grader / Verifier
├── Threshold
└── Aggregation
```

### 7.4 Outcome Eval 与 Process Eval

- Outcome Eval：最终结果是否成功。
- Process Eval：执行过程暴露了哪些策略、效率或成本问题。

开放式 Agent 不应该被要求遵循唯一 Golden Agent Path。

### 7.5 Specialist Agent as Capability

Research Specialist、Citation Agent、Verifier 等可以作为一种可发现能力，通过 Agent-as-Tool 或 Child Session 使用，而不必永远成为固定团队成员。

## 8. 长任务连续性

### 8.1 Durable Handoff

Handoff 至少回答剩余工作、已发生事实和恢复入口。

### 8.2 Progress / Notes 是投影

当 Progress 与 Git、Test、Artifact、Runtime Event 等 Ground Truth 冲突时，应重新校验。

### 8.3 Bootstrap 属于 Harness

Initializer、Planner、Reviewer 等具体角色不进入 Runtime Core。

## 9. 上下文与持久资源

### 9.1 Context Builder

负责选择历史、加载 Memory、读取 Notes / Artifacts / Workspace、即时加载能力和知识，并做摘要和压缩。

### 9.2 Compaction

Compaction 改变模型看到什么，不改变真实历史。

### 9.3 Notes、Memory、Workspace、Artifact

- Notes / Todo：当前主观工作认知。
- Memory：跨时间保留并可召回的信息。
- Workspace：文件、代码、中间结果和 Checkpoint。
- Artifact：正式结果或交付物。

## 10. Harness 工程

```text
Harness Revision
      ↓
     Trial
      ↓
Trace + Outcome
      ↓
     Eval
      ↓
Failure Analysis
      ↓
Harness Revision
```

Harness Revision 与 Session 生命周期分离；发布新 Harness 不意味着隐式迁移正在执行的 Session。

## 11. 当前架构不变量

1. **应用形态不等于执行范式。**
2. **Workflow 与 Agent 的核心区别是执行控制权归属。**
3. **Runtime 承载持久执行事实，不固化控制策略。**
4. **静态 Workflow、动态 Plan、Agent Loop 和动态 Multi-Agent 是逐渐增加动态性的执行方式。**
5. **Workflow Graph 是输入表达；Agent Graph 更接近运行时结果。**
6. **Session、Harness、Execution Environment 分别回答“发生了什么、怎么推进、在哪里行动”。**
7. **Runtime 稳定，Harness 可替换、可简化甚至消失。**
8. **Context 是可重建投影和当前 Working Set。**
9. **Compaction 改变模型看到什么，不改变真实历史。**
10. **长任务连续性来自 Durable State + Handoff + Recovery。**
11. **Progress / Notes 是 Handoff Projection，不是 Source of Truth。**
12. **Recovery 必须重新校验 Ground Truth。**
13. **Plan 负责怎么做，Evaluation Contract 负责如何证明已经做成。**
14. **Execution State 与 Acceptance State 必须分离。**
15. **Multi-Agent 不是复杂任务默认答案，其价值取决于可并行性、上下文独立性和可合并性。**
16. **Lead Agent 负责全局编排与全局上下文；Child Agent 负责局部工作。**
17. **Agent-as-Tool 是 Action；真正自治且需要持久生命周期的 Sub-agent 是 Child Session。**
18. **Agent Team 可以由 Harness 根据 Goal 和约束动态形成。**
19. **Multi-Agent 需要局部恢复 + 全局协调，并区分 Delegation Concurrency 与 Action Concurrency。**
20. **Plan 是可变假设，Budget 是硬约束。**
