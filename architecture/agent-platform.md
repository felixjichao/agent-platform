# 智能体平台总体架构

本文档记录 Agent Platform 当前已经形成的规范性架构结论，并随着研究持续演进。

> 当前版本已吸收前七篇研究。C 编译器 Agent Team 的实践进一步把长期载体从 Session 上移到 Work，并把 Execution Environment 扩展成 Agent Work Environment。

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
Agent Work Environment
    ↓
基础设施 / 真实世界
```

其中：

- 业务层决定要完成什么；
- Harness 决定当前如何执行；
- Evaluation Contract 决定如何证明完成；
- Runtime 记录真正发生的执行事实；
- Agent Work Environment 决定 Agent 能看到什么、做什么、如何获得反馈和验证。

## 2. 核心设计原则

### 2.1 应用形态与执行范式分离

对话、研究、知识库、Coding 等是应用形态；Direct、Workflow、Agent Loop、Multi-Agent 等是执行范式。

### 2.2 执行控制权决定 Workflow 与 Agent 的边界

- Workflow：下一步主要由代码或图决定。
- Agent：下一步主要由模型根据当前 Context 动态决定。

### 2.3 Runtime 稳定，Harness 可替换

Harness 是对当前模型能力缺口的适应性脚手架。Planner、Evaluator、Context Reset、Delegation Strategy 等应允许版本化、实验、替换和删除。

### 2.4 Context 是可重建投影

> **Session 追加事实，Context 选择性投影。**

Context 是当前 Working Set，不是持久事实源。

### 2.5 长期工作连续性不依赖 Agent 连续性

> **Durable work continuity should not depend on durable agent continuity.**

Agent 可以退出、忘记、被替换；Work 必须记住。

### 2.6 Execution State、Verification State 与 Acceptance State 分离

```text
Executed
≠ Verified
≠ Accepted
≠ Published / Deployed
```

系统不能把“Agent 执行完成”直接等价为“业务接受”。

### 2.7 Multi-Agent 的核心是 Work Scheduling

有效并行度由独立 Work Front 决定，而不是由可启动 Agent 数量决定。

## 3. 当前软件栈

```text
L6 业务 / 产品
   Goal · Project · Requirement

L5 能力契约
   Acceptance Criteria · Quality Criteria · Evaluation Contract

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

横切：Context / Memory · Trace · Budget · Governance
```

## 4. Work / Session / Run

### 4.1 Work

Work 是长期工作的真实载体：

```text
Work / Project
├── Goal
├── Acceptance
├── Shared Resources
├── Work Frontier
├── Artifacts
├── Environment / Workspace
├── Long-term Progress
└── Sessions
```

它可以跨 Agent、跨 Session、跨模型版本持续存在。

### 4.2 Session

Session 是一个 Agent 与某个 Work 之间相对连续的认知 / 执行关系。

同一个 Work 可以：

- 顺序经历多个 Session；
- 同时存在多个并行 Session；
- 在 Agent 更换后继续存在。

因此长期 Goal 不再天然等于一个 Session。

### 4.3 Run

Run 是：

> **Runtime 被触发后，在一个 Session 内发生的一次连续执行片段。**

典型新 Run：

- 用户新消息；
- Human Approval / Input；
- Timer / Webhook；
- Child Completion Event。

基础设施内部恢复通常仍属于同一个 Run，例如 worker restart、tool retry。

### 4.4 Parent / Child Session

自治 Sub-agent 形成独立执行生命周期时创建 Child Session：

```text
Work
├── Parent Session
│    │ Delegation
│    └──────────────┐
├── Child Session A │
├── Child Session B │
└── Child Session C │
```

Parent 拥有全局目标和综合责任，Child 拥有局部目标和局部 Context。

### 4.5 Agent-as-Tool

短生命周期、聚焦调用且不需要独立恢复的另一个 Agent，可以直接建模为 Parent Session 中的一次 Action。

## 5. Agent Work Environment

Execution Environment 被扩展成更丰富的工作环境：

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

### 5.1 Shared State + Local Isolation

Shared-world 多智能体需要：

- 共享事实世界；
- Agent 局部工作副本；
- 资源 identity / version；
- ownership / lease；
- snapshot / change；
- conflict handling。

协作不应只依赖 Agent-to-Agent 文本消息，环境状态本身就是重要协调媒介。

### 5.2 Work Frontier

Work Frontier 是当前**独立、可领取、可验证**的工作项集合：

```text
Work
├── Done
├── Claimed
├── Blocked
└── Frontier
    ├── Work Item A
    ├── Work Item B
    └── Work Item C
```

> **Effective Parallelism ≈ Independent Work Fronts。**

真正的平台问题是 Work Scheduler，而不只是 Agent Scheduler。

### 5.3 Environment Engineering

原始环境结果需要转换为 Agent 可消费的高信号 Observation：

```text
Raw Environment Result
      ↓
Parse / Filter / Diagnose
      ↓
Agent-facing Observation
```

环境质量直接影响 Agent 能否正确理解当前世界并高效继续。

## 6. Multi-Agent 执行模型

### 6.1 适用条件

```text
Multi-Agent Value
≈ 可并行性
 + 上下文独立性
 + 结果可合并性
 - 依赖密度
 - 协调成本
```

任务复杂本身不是使用 Multi-Agent 的理由。

### 6.2 Lead Agent

> **Lead Agent = Orchestrator + Global Context Owner。**

它负责全局目标、工作拆解、委托、覆盖度、冲突协调和最终综合。

### 6.3 Dynamic Team Formation

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

Agent Team 可以是运行时结果。

### 6.4 Local Recovery + Global Reconciliation

Child 局部失败优先局部恢复；恢复结果再回到 Parent 进行全局重新协调。

### 6.5 两层并发

- Delegation Concurrency：多个 Agent 同时工作。
- Action Concurrency：单个 Agent 内多个 Tool / Action 同时执行。

### 6.6 Async Delegation

Delegation 应允许成为持久、事件驱动关系，而不是要求 Parent 同步阻塞等待 Child。

## 7. Verification 与 Acceptance

### 7.1 Evaluation Contract

```text
Plan                → How to do
Evaluation Contract → How to prove it is done
```

Evaluation Contract 包含 Criterion、Evidence、Grader / Verifier、Threshold 和 Aggregation。

### 7.2 Acceptance 与 Quality

- Acceptance Criteria：决定能否结束。
- Quality Criteria：描述完成得有多好。

### 7.3 Verification Ladder

```text
Local Checks
   ↓
Regression
   ↓
Representative Workloads
   ↓
Integration
   ↓
Production-like Verification
```

先使用便宜、高频的局部反馈，再逐步升级到昂贵但更接近真实目标的验证。

### 7.4 Differential Oracle

Verifier 不应只返回 pass / fail，还应尽量返回高信号差异和诊断，帮助 Agent 决定下一步。

### 7.5 Steward / Guardian

除了 Work Item 局部验证，还需要维护跨任务长期质量：回归、架构约束、技术债和共享资源健康度。

### 7.6 Cost per Successful Outcome

成本最终应衡量：

> **完成一个成功 Outcome 需要多少总资源。**

单次请求或 token 便宜，不代表整体执行策略更经济。

## 8. Recovery 与 Escalation

### 8.1 Recovery

解决当前能力范围内的可恢复故障，如 worker restart、临时 Tool failure、Harness crash。

### 8.2 Escalation

解决当前能力边界无法跨越的问题，例如：

- 需要更强模型；
- 需要专家 Capability；
- 需要人工决策；
- 缺少 Tool；
- 需要缩小 Scope。

> **Recovery 解决暂时失败，Escalation 解决能力边界。**

## 9. Context、Memory 与持久资源

### 9.1 Context Builder

```text
Session / State / Memory / Notes / Artifacts / Workspace
                         ↓
                   Context Builder
                         ↓
                      Context
```

Context Builder 属于 Harness / Context Strategy。

### 9.2 Compaction

Compaction 改变模型看到什么，不改变真实历史；摘要是派生资源。

### 9.3 Notes、Memory、Workspace、Artifact

- Notes / Todo：当前主观工作认知。
- Memory：跨时间保留并可召回的信息。
- Workspace：Work 的外部持久工作状态。
- Artifact：正式结果或交付物。

Workspace 现在更明确属于 Work，而不是某个 Session 的临时附件。

## 10. Effort 与预算

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

Plan 是可变假设；Budget 是硬约束。

## 11. Harness 工程

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

Harness Revision 与 Session 生命周期分离。

## 12. Human Governance

随着 Agent 自主性增强，人类逐渐从 Execution Path 移向 Governance Plane：

```text
Human / Governance
├── Goal
├── Acceptance
├── Risk Boundary
├── Escalation
└── Publish / Deploy Decision
```

必须区分：

```text
VerificationPassed
≠ AcceptedForProduction
≠ Published / Deployed
```

## 13. 当前架构不变量

1. **应用形态不等于执行范式。**
2. **Workflow 与 Agent 的核心区别是执行控制权归属。**
3. **Runtime 承载持久执行事实，不固化控制策略。**
4. **Runtime 稳定，Harness 可替换、可简化甚至消失。**
5. **Context 是可重建投影和当前 Working Set。**
6. **长期工作连续性不依赖 Agent 或 Session 永久存在；Work 才是长期载体。**
7. **Work、Session、Run 分别承载长期工作、Agent 连续关系和一次触发后的连续执行片段。**
8. **Progress / Notes 是 Projection，不是 Source of Truth。**
9. **Recovery 必须重新校验 Ground Truth。**
10. **Plan 负责怎么做，Evaluation Contract 负责如何证明已经做成。**
11. **Execution State、Verification State 与 Acceptance State 必须分离。**
12. **Multi-Agent 的关键不是 Agent 数量，而是 Work Frontier。**
13. **Agent Work Environment 既要支持行动，也要支持工作发现、Ownership、Observation 和 Verification。**
14. **Lead Agent 负责全局编排和全局 Context；Child Agent 负责局部工作。**
15. **Agent Team 可以由 Harness 根据 Goal 和约束动态形成。**
16. **Multi-Agent 需要 Local Recovery + Global Reconciliation。**
17. **Delegation Concurrency 与 Action Concurrency 是两种不同并发。**
18. **Recovery 与 Escalation 分别解决暂时失败和能力边界。**
19. **Verification 应形成阶梯，并提供可行动的 Differential Oracle。**
20. **Human 应逐渐从 Execution Path 移向 Governance Plane。**
