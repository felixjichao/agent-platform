# 智能体平台总体架构

本文档记录 Agent Platform 当前已经形成的规范性架构结论，并随着研究持续演进。

> 当前版本已吸收前八篇研究。Eval 被进一步提升为 Capability Contract 的可执行组成部分，并与 Trial、Trace、Outcome、Grader 和 Environment 建立完整关系。

## 1. 架构主张

Agent Platform 不按产品形态分别建设执行内核，而是围绕稳定的平台边界组织：

```text
业务 / 产品
    ↓
能力契约
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

- 业务 / 产品决定要完成什么；
- Capability Contract 定义“能力是什么、怎样证明”；
- Harness 决定当前如何实现；
- Runtime 记录真正发生的执行事实；
- Agent Work Environment 决定 Agent 能看到什么、做什么、如何获得反馈和验证；
- Eval 测量 Trial 是否满足 Capability Contract，并为 Harness 演进提供反馈。

## 2. 核心设计原则

### 2.1 应用形态与执行范式分离

对话、研究、知识库、Coding 等是应用形态；Direct、Workflow、Agent Loop、Multi-Agent 等是执行范式。

### 2.2 执行控制权决定 Workflow 与 Agent 的边界

- Workflow：下一步主要由代码或图决定。
- Agent：下一步主要由模型根据当前 Context 动态决定。

### 2.3 Runtime 稳定，Harness 可替换

Harness 是对当前模型能力缺口的适应性脚手架，其复杂度必须通过 Eval 证明。

### 2.4 Context 是可重建投影

> **Session 追加事实，Context 选择性投影。**

Context 是当前 Working Set，不是持久事实源。

### 2.5 长期工作连续性不依赖 Agent 连续性

Agent 可以退出、忘记、被替换；Work 必须记住。

### 2.6 Trial 是 Agent Eval 的基本测量单位

Agent 的能力不能由单次 response 代表。Eval 需要观察完整 Trial，包括 Environment、Trace 和 Outcome。

### 2.7 Outcome 是事实，Score 是测量投影

Eval Score 不是 Source of Truth，必须可追溯到 Task、Evidence、Grader 和 Measurement Configuration。

## 3. 当前软件栈

```text
L6 业务 / 产品
   Goal · Project · Requirement

L5 能力契约
   Capability Definition
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

横切：
Context / Memory · Trace · Eval · Budget · Governance
```

## 4. Work / Session / Run

### 4.1 Work

Work 是长期工作的真实载体：

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

### 4.2 Session

Session 是一个 Agent 与某个 Work 之间相对连续的认知 / 执行关系。同一 Work 可以跨多个 Session、多个 Agent 和多个模型版本持续存在。

### 4.3 Run

Run 是 Runtime 被触发后，在一个 Session 内发生的一次连续执行片段。

典型新 Run：用户新输入、Human Approval、Timer / Webhook、Child Completion Event。

### 4.4 Parent / Child Session

自治 Sub-agent 形成独立执行生命周期时创建 Child Session；短生命周期 Agent-as-Tool 仍可作为 Parent 中的一次 Action。

## 5. Agent Work Environment

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

### 5.1 Work Frontier

Work Frontier 是当前独立、可领取、可验证的 Work Item 集合。

> **Effective Parallelism ≈ Independent Work Fronts。**

Multi-Agent 的关键调度对象是 Work，而不是 Agent 数量。

### 5.2 Environment Engineering

原始环境结果需要经过 Parse / Filter / Diagnose，转化成高信号 Agent-facing Observation。

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

### 6.2 Lead Agent

> **Lead Agent = Orchestrator + Global Context Owner。**

### 6.3 Dynamic Team Formation

Harness 可以根据 Goal、Capabilities、Knowledge、Permissions、Budget 和 Risk 动态选择 Single、Workflow、Multi-Agent 或 Hybrid，并形成具体 Agent Team。

### 6.4 Recovery 与并发

- Local Recovery + Global Reconciliation；
- Delegation Concurrency 与 Action Concurrency 分离；
- Delegation 可以是持久、异步、事件驱动关系。

## 7. Eval Architecture

### 7.1 基本对象

```text
Eval Suite
   └── Task
        └── Trial
             ├── Agent / Harness Revision
             ├── Environment Revision
             ├── Transcript / Trace
             ├── Outcome
             └── Grader Results
```

#### Task

定义要测量的能力和初始条件。

#### Trial

一次完整 Agent 执行，是 Agent Eval 的基本单位。

#### Transcript / Trace

描述执行过程：模型步骤、Action、Delegation、Retry、Tool Result、Budget 等。

#### Outcome

描述 Trial 结束后真实世界的状态和交付结果。

#### Grader

根据 Criterion 和 Evidence 对 Outcome 或 Process 做测量。

### 7.2 Evaluation Contract

```text
Evaluation Contract
├── Criterion
├── Evidence Source
├── Grader
├── Threshold / Criticality
└── Aggregation
```

Criterion 定义“什么叫好”，Evidence 定义“看什么证明”，Grader 定义“怎么测”。三者不能混为一个 Judge Prompt。

### 7.3 Grader 类型

- Deterministic：测试、结构校验、环境状态、规则。
- LLM Judge：开放式语义、综合性和主观质量。
- Human：高风险、最终业务责任和难以自动化的判断。

适合确定性检查时优先使用确定性 Grader。

### 7.4 非确定性与多 Trial

Agent 具有非确定性，同一个 Task 需要多次 Trial。

- **pass@k**：k 次至少一次成功，更接近 Capability / Search Potential。
- **pass^k**：k 次全部成功，更接近 Reliability。

能力存在与生产可靠性不能用同一个单次通过率代表。

### 7.5 Capability Eval 与 Regression Eval

```text
Capability Eval
→ 探索新的能力边界
      ↓ graduation
Regression Eval
→ 守住已经证明的能力
```

Task 应有生命周期：新能力被证明后，将代表性案例晋升到长期 Regression Suite。

### 7.6 Task Spec

一个稳定 Task 至少描述：

```text
Task Spec
├── Initial State
├── Goal
├── Constraints
├── Available Capabilities
├── Acceptable Outcomes
├── Evaluation Criteria
└── Environment Requirements
```

Reference Solution 用于证明 Task 可解并验证 Grader，不要求 Agent 遵循相同执行路径。

### 7.7 Eval Environment

Eval Environment 必须：

- 与 Production 行为足够接近；
- Trial 间隔离；
- 可重置；
- 可观测；
- 固定关键依赖版本。

Eval Harness 应调用真实 Runtime，而不是重新实现一套假的 Agent。

### 7.8 Eval Score 是 Measurement Projection

```text
Trial / Outcome
    ↓
Measurement Configuration
(Task + Rubric + Grader + Judge Model + Threshold)
    ↓
Eval Score
```

Task、Rubric、Grader、Judge Model、Eval Harness 都需要版本化。Judge 还应通过 Human Ground Truth 校准。

### 7.9 Quality / Reliability / Efficiency

不建议用单一总分掩盖不同维度：

- **Quality**：结果好不好；
- **Reliability**：能否稳定重复成功；
- **Efficiency**：达到成功 Outcome 需要多少时间、token、tool call 和成本。

### 7.10 Research Eval

Research Agent 应共享 Evidence Chain：

```text
Claim
  ↓ supported by
Evidence Ref
  ↓ points to
Source Ref
```

关键维度：Groundedness、Coverage、Source Quality、Factual Accuracy、Synthesis。

Judge Strategy 可使用多个独立 Judge，但是否值得应由与 Human Ground Truth 的校准结果决定。

### 7.11 Eval Infrastructure vs Eval Content

平台负责 Eval Infrastructure：

- Runner；
- Environment；
- Trace；
- Grader SDK；
- Statistics；
- Versioning。

Capability / Domain Owner 负责 Eval Content：

- Tasks；
- Criteria；
- Rubrics；
- Reference Solutions；
- Failure Cases；
- Domain-specific Graders。

> **Eval Infrastructure 是平台能力；Eval Content 是 Capability Asset。**

### 7.12 Eval 是 Capability Specification

```text
Requirement
   ↓
Capability Eval
   ↓
Harness Development
   ↓
Trial
   ↓
Gap Analysis
   ↓
Iteration
```

因此 Capability Contract 有两个互补面：

```text
Harness
→ How to implement

Eval
→ How to prove
```

## 8. Verification 与 Acceptance

### 8.1 状态分离

```text
Execution State
≠ Verification State
≠ Acceptance State
≠ Publish / Deploy State
```

### 8.2 Verification Ladder

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

### 8.3 Differential Oracle

Verifier 应尽量提供高信号诊断，而不只是 pass / fail。

### 8.4 Acceptance 与 Quality

- Acceptance Criteria：决定能否结束。
- Quality Criteria：描述完成得有多好。

## 9. 整体质量系统

离线 Eval 不是完整质量系统。Production 还需要：

```text
Offline Eval
Production Monitoring
A/B Experiment
User Feedback
Transcript Review
Human Evaluation
Failure / Incident Mining
```

Production failure 应能够沉淀为新的 Capability Eval 或 Regression Task，形成数据闭环。

## 10. Recovery 与 Escalation

Recovery 解决暂时、可恢复的故障；Escalation 解决当前能力边界无法跨越的问题。

## 11. Context、Memory 与持久资源

Context Builder 从 Session、State、Memory、Notes、Artifacts、Workspace 等来源动态投影当前 Working Set。

Compaction 改变模型看到什么，不改变真实历史。

Workspace 属于 Work 的长期工作状态；Artifact 是正式结果；Notes 是主观工作认知；Memory 是跨时间召回信息。

## 12. Effort 与预算

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

## 13. Harness 工程

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

## 14. Human Governance

人类逐渐从 Execution Path 移向 Governance Plane，负责 Goal、Acceptance、Risk Boundary、Escalation 和最终 Publish / Deploy Decision。

## 15. 当前架构不变量

1. **应用形态不等于执行范式。**
2. **Workflow 与 Agent 的核心区别是执行控制权归属。**
3. **Runtime 承载持久执行事实，不固化控制策略。**
4. **Runtime 稳定，Harness 可替换、可简化甚至消失。**
5. **Context 是可重建投影和当前 Working Set。**
6. **Work 是长期连续性的载体；Agent 和 Session 都可以被替换。**
7. **Work、Session、Run 分别承载长期工作、Agent 连续关系和一次触发后的连续执行。**
8. **Multi-Agent 的关键调度对象是 Work Frontier。**
9. **Agent Work Environment 同时支持工作发现、行动、观测和验证。**
10. **Plan 负责怎么做，Evaluation Contract 负责如何证明已经做成。**
11. **Trial 是 Agent Eval 的基本单位，而不是单次 response。**
12. **Transcript / Trace 与 Outcome 必须分离。**
13. **Outcome 是事实，Eval Score 是 Measurement Projection。**
14. **Capability Eval 探索能力边界，Regression Eval 守住已获得能力。**
15. **非确定性 Agent 必须多 Trial 测量；pass@k 和 pass^k 分别反映不同问题。**
16. **Eval Infrastructure 属于平台能力，Eval Content 属于 Capability Asset。**
17. **Eval 是可执行 Capability Specification：Harness 说明怎么实现，Eval 说明怎么证明。**
18. **Execution、Verification、Acceptance 和 Publish 状态不能混为一体。**
19. **开放式 Agent 不需要遵循 Golden Agent Path，Outcome 与 Process 应分别评估。**
20. **Human 最终位于 Goal、Risk、Acceptance 和 Publish 所在的 Governance Plane。**
