# 智能体平台总体架构

本文档是 Agent Platform 当前的规范性架构文档（Canonical Architecture Document）。文章目录保存研究过程和依据；本文件只保留已经形成的稳定架构结论，并通过 Git 历史记录这些结论如何逐步演进。

## 1. 总体架构主张

Agent Platform 的目标，不是为每一种 Agent 产品形态实现一套独立框架，而是为**动态组装、非确定、长期运行、可并行、可编程的智能执行过程**提供一套稳定的生产系统边界。

平台最终需要把这样的执行过程约束在：

> **持久、可恢复、可验证、可观测、可治理、可持续演进的系统中。**

统一心智模型：

```text
业务目标
   ↓
能力契约
   ↓
动态组装能力
   ↓
选择执行策略 / Harness
   ↓
统一 Runtime 记录真实执行
   ↓
Agent Work Environment 执行动作、处理数据、提供反馈
   ↓
真实世界
```

同时，Context / Memory、Eval / Trace、安全与治理贯穿整个软件栈。

## 2. Agent Software Stack

```text
L7 业务 / 产品
   Goal · Project · Business Task · Requirement

L6 能力契约
   Capability Definition
   Acceptance Criteria · Quality Criteria · Evaluation Contract

L5 能力工程
   Capability Catalog · Taxonomy · Discovery
   Skill · Tool · Capability Adapter · MCP Binding

L4 执行策略
   Direct · Workflow · Agent Loop · PTC · Multi-Agent
   Harness · Planning · Delegation · Context Strategy · Evaluator

L3 统一运行时
   Work · Session · Run · Event · State
   Action · Result · Observation · Artifact
   Delegation · Recovery

L2 Agent Work Environment
   Workspace · Shared Resources · Programmatic Execution
   Work Discovery · Ownership / Lease
   Observation Projection · Verification / Oracle
   Capability Proxy · Sandbox / Isolation

L1 基础设施 / 真实世界
   API · MCP Server · SaaS · DB · Browser
   Files · Compute · Network · Devices
```

横切系统：

```text
Context / Memory
Observability / Trace
Evaluation
Security / Governance
Registry / Versioning
Budget / Cost
```

## 3. 每一层回答什么问题

### L7 业务 / 产品：要完成什么？

负责：

- Goal；
- Project；
- Business Task；
- 用户价值；
- 业务约束和责任。

对话、科研助手、知识库、Coding、Workflow 产品等都属于应用形态，不等于执行范式。

### L6 能力契约：什么叫“具备这项能力”？

负责定义：

```text
Capability
├── Goal / Requirement
├── Acceptance Criteria
├── Quality Criteria
├── Evaluation Contract
└── Evidence Requirement
```

Harness 描述“怎么实现”，Eval 描述“怎么证明”。

### L5 能力工程：Agent 能学什么、能做什么？

负责组织：

- Skill：程序性知识；
- Tool：行动能力；
- MCP / API Binding：连接实现；
- Capability Discovery；
- Capability Adapter；
- Capability Revision / Eval。

### L4 执行策略：当前任务怎么推进？

负责：

- Direct；
- Workflow；
- Agent Loop；
- PTC；
- Multi-Agent；
- Planning；
- Delegation；
- Context Strategy；
- Evaluation Strategy；
- Completion / Escalation Strategy。

这些策略主要由 Harness 承载。

### L3 统一运行时：实际上发生了什么？

负责记录和管理执行事实、状态、生命周期、恢复和因果关系，不负责把某一种 Harness 策略固化为系统唯一执行方式。

### L2 Agent Work Environment：Agent 能观察和作用于什么世界？

负责：

- Workspace；
- 数据与动作执行；
- Work Discovery；
- Shared State；
- Ownership；
- Observation；
- Verification；
- Sandbox / Isolation；
- Capability Proxy；
- Programmatic Execution。

### L1 基础设施 / 真实世界：真正的资源在哪里？

包括 API、SaaS、数据库、浏览器、文件、计算资源、网络、设备等。

## 4. 核心设计原则

### 4.1 应用形态不等于执行范式

```text
Application Forms
Chat · Research · Knowledge Base · Coding · Industry Apps

Execution Paradigms
Direct · Workflow · Agent · PTC · Multi-Agent
```

同一种产品可以使用不同执行策略，同一种执行策略也可以服务多个产品。

### 4.2 Workflow 与 Agent 的真正区别是执行控制权

```text
Workflow
→ 下一步主要由预定义代码 / 图决定

Agent
→ 下一步主要由模型基于 Context 动态决定
```

因此：

> **Static Workflow → Dynamic Workflow / Plan → Agent Loop 是连续谱。**

Workflow Graph 是输入表达；Agent Graph 更接近运行时结果。

### 4.3 Runtime 稳定，Harness 可替换

Harness 编码了“当前模型还做不到什么”的假设。

这些假设会随着模型升级而过时，所以：

> **Runtime should be stable; Harness should be replaceable and removable.**

Planner、Evaluator、Initializer、Context Reset、Todo、Completion Strategy 等默认属于 Harness，而不是 Runtime Core。

### 4.4 长期工作连续性不依赖 Agent 连续性

> **Agent 可以忘记、退出或被替换；Work 必须记住。**

长任务依赖 Durable Work State、Workspace、Event、Artifact、Handoff 和 Recovery，而不是一个 Session 永久不结束。

### 4.5 LLM 应是 Control Plane，而不是 Data Plane

模型适合做高价值、不确定决策；数据搬运、循环、join、过滤、聚合和稳定 mechanics 尽量进入执行环境。

```text
Agent / Harness
= Execution Control Plane

Agent Work Environment
= Data + Action Plane
```

### 4.6 Execution、Verification、Acceptance、Publish 分离

```text
Executed
≠ Verified
≠ Accepted
≠ Published / Deployed
```

Agent 认为完成，不代表系统验证通过；验证通过，也不自动等于业务接受或允许生产发布。

## 5. 核心领域模型

### 5.1 Work

Work 是长期目标和共享工作世界的载体：

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

多个 Agent、多个 Session、多个 Harness Revision 可以围绕同一个 Work 工作。

### 5.2 Session

Session 表示：

> **一个 Agent 与一个 Work 之间相对连续的认知 / 执行关系。**

Session 不是 Chat History，也不是 Context Window。

同一个 Work 可以：

- 顺序经历多个 Session；
- 并行存在多个 Session；
- Agent 更换后继续存在。

### 5.3 Run

Run 表示：

> **Runtime 被触发后，在一个 Session 内发生的一次连续执行片段。**

常见新 Run 触发：

- User Message；
- Human Approval / Input；
- Timer / Webhook；
- External Event；
- Child Session Completion。

基础设施内部恢复通常仍属于同一个 Run，例如 worker restart、tool retry。

### 5.4 Event

Event 是已经发生的事实，是持久执行历史的重要基础。

典型类别：

```text
Trigger
├── UserMessageReceived
├── ExternalEventReceived
└── TimerTriggered

Run
├── RunStarted
├── RunPaused
├── RunCompleted
└── RunFailed

Action
├── ActionRequested
├── ActionStarted
├── ActionSucceeded
└── ActionFailed

Human
├── ApprovalRequested
├── ApprovalGranted
├── ApprovalRejected
└── HumanInputReceived

Artifact
├── ArtifactCreated
└── ArtifactUpdated

Recovery
├── RecoveryStarted
└── RecoveryCompleted
```

Planning Event 默认不是 Runtime Core，因为 Plan 属于 Harness Strategy。

推荐 Event Envelope：

```text
event_id
event_type
schema_version
work_id
session_id
run_id
sequence
timestamp
actor
causation_id
correlation_id
payload
```

### 5.5 Command / Event / State

```text
Command
→ 希望发生什么

Event
→ 实际发生了什么

State
→ 根据事实得到的当前视图
```

推荐：

```text
Action / Result
      ↓
     Event
      ↓ append
 Event Log
      ↓ project
    State
```

State 可以被重建；Event Log 承担持久事实来源。Snapshot 是恢复优化，不是真理来源。

### 5.6 Action

Action 是 Runtime 向 Execution Environment 发出的受治理执行请求。

来源可能是 Workflow、Harness、Program、Human 或系统自动机制。

### 5.7 Result

Result 是 Action 的真实执行结果，属于执行事实。

### 5.8 Observation

Observation 是从 Result、Resource 或 Environment 中构建出的 Agent-facing Projection：

```text
Action
  ↓
Raw Result
  ↓
Filter / Transform / Aggregate / Redact / Persist
  ↓
Observation
  ↓
Context
```

> **Result = execution fact；Observation = model-facing projection。**

### 5.9 Artifact

Artifact 是正式结果 / 交付物，具有版本、评审、发布或引用语义。

它与 Note 的区别：Note 是 Agent 当前主观认知；Artifact 是正式工作产物。

## 6. Context、Memory、Workspace

### 6.1 Session != State != Context

```text
Session
→ 持久执行历史

State
→ 当前运行视图

Context
→ 当前模型 Working Set
```

Context 是投影，可以丢弃和重建。

### 6.2 Context Builder

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

Context Builder 属于 Harness / Context Strategy。

### 6.3 Context 是 Working Set

> **Context contains a map, not the whole world.**

稳定内容适合前置：

- System / Policy；
- Agent Definition；
- Capability Metadata。

阶段性稳定：

- Goal；
- Checkpoint；
- Summary；
- 当前 Plan。

动态内容：

- recent history；
- Observation；
- JIT Knowledge；
- Tool / Skill detail。

### 6.4 Compaction

```text
Session append facts
        ↓
Context Strategy
        ↓
select / summarize / compact
        ↓
Context
```

Compaction 改变模型看到什么，不改变真实发生过什么。

### 6.5 Notes / Todo

Agent 当前主观工作认知，包括计划、待办、假设和临时结论。

它可以被修改，也可能是错的，因此不是 Source of Truth。

### 6.6 Memory

可以区分：

- Working Memory → Notes / Todo；
- Episodic Memory → 过去任务 / Session 经验；
- Semantic Memory → 稳定知识、规则、偏好。

长期 Memory 推荐 Promotion Pipeline：

```text
Session / Observation
      ↓
Candidate Memory
      ↓
Validation / Provenance / Trust
      ↓
Long-term Memory
```

原则：

> **Write freely, promote carefully.**

Recall 不能只用 Vector Top-K，还应考虑 Goal、State、Scope、Recency、Importance、Confidence、Trust / Provenance。

### 6.7 Workspace

Workspace 是 Work 的外部持久工作状态：

- files；
- code；
- intermediate data；
- checkpoints；
- generated programs；
- progress。

Workspace 不等于 Memory，也不属于单个 Context。

## 7. Capability Engineering

### 7.1 Capability 分类

```text
Capability
├── Procedural Capability
│   └── Skill
│
└── Action Capability
    └── Tool
```

### 7.2 Tool、Skill、MCP、Harness

```text
Tool
→ 能做什么动作

Skill
→ 这类任务通常应该怎么做

MCP
→ 如何连接外部系统

Harness
→ 当前任务现在怎么推进
```

### 7.3 Capability Adapter

```text
Backend API / MCP Tool
        ↓
Capability Adapter
        ↓
Agent-facing Tool
```

API atomicity 不等于 Agent Capability Granularity。

### 7.4 Agentic Boundary

> **Deterministic mechanics 下沉到 Capability；uncertain decisions 留给 Harness。**

Tool 太原子会产生大量无意义编排；Tool 太大则会把真正需要 Agent 判断的策略藏进黑盒 Workflow。

### 7.5 Capability Catalog / Taxonomy

```text
Domain
  ↓
Resource
  ↓
Semantic Capability
  ↓
Concrete Skill / Tool
```

每个能力要明确 What、When、When NOT、Boundary / Neighbor。

### 7.6 Discovery != Loading

能力规模化后：

```text
Capability Discovery
      ↓
Metadata
      ↓
Select
      ↓
Skill / Tool Detail Loading
```

不要永久把全量 Tool / Skill 定义放入 Context。

### 7.7 Skill Progressive Disclosure

```text
Skill Metadata
      ↓
SKILL.md
      ↓
References / Scripts / Resources
```

Skill 是可发现、可导航、按需加载的程序性知识。

### 7.8 Skill Script 与 Tool

Skill-local Script 服务于某个 Skill 的稳定局部实现；Tool 是平台级、可治理、可复用的行动能力。

不是每个 Script 都需要注册成全局 Tool。

### 7.9 MCP 的位置

> **MCP 是 Connectivity Standard，不是 Capability Design Standard。**

推荐：

```text
Skill
  ↓ requires
Semantic Capability
  ↓ binds
Tool
  ↓ implemented via
MCP / API / Local Script
```

### 7.10 Tool Contract

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

Schema 描述机器允许什么；Guidance 帮助 Agent 正确选择和使用。

### 7.11 动态组装 Agent

```text
Base Agent
+ Selected Skills
+ Selected Tools
+ Retrieved Knowledge
+ Task Context
        ↓
Effective Agent
```

> **Agent uses capabilities; Agent does not own capabilities.**

能力资产应独立、可版本化、可发现、可组合、可治理。

### 7.12 Eval-driven Capability Engineering

Tool 和 Skill 都从真实 Capability Gap 出发，通过 Trial / Trace / Eval 迭代。

Tool-use Smells：wrong-tool switching、重复 retry、oversized result、invalid params 等。

Skill Failure：Discovery、False Activation、Navigation、Instruction、Over-contexting、Procedure Failure。

## 8. Execution Strategy

### 8.1 Direct

模型直接做一次决策或直接调用少量 Tool。

### 8.2 Workflow

代码拥有主要执行控制权。

基础控制原语：

- Sequence；
- Branch；
- Fork / Join；
- Loop；
- Dynamic Expansion。

### 8.3 Agent Loop

模型持续根据 Context 和 Observation 决定下一 Action。

### 8.4 PTC

PTC（Programmatic Tool Calling）是 Tool Orchestration Mode，不是 Tool Type。

```text
Model
  ↓ generate program
Program
  ├── Tool A
  ├── Tool B
  ├── loop
  ├── filter
  └── aggregate
       ↓
Observation
       ↓
Model
```

一个 Reasoning Step 可以对应许多 Environment Actions。

### 8.5 Multi-Agent

使用 Multi-Agent 取决于：

```text
Value
≈ Parallelizability
 + Context Independence
 + Result Mergeability
 - Dependency Density
 - Coordination Cost
```

复杂任务本身不是理由。

## 9. Multi-Agent Architecture

### 9.1 Lead Agent

> **Lead Agent = Orchestrator + Global Context Owner。**

负责全局目标、工作拆解、委托、覆盖度、冲突和最终综合。

### 9.2 Agent-as-Tool vs Child Session

Agent-as-Tool：聚焦短调用，是 Parent Session 中一次 Action。

Autonomous Child Agent：独立目标、多轮 Context、Artifact、Recovery，需要 Child Session。

### 9.3 Dynamic Team Formation

```text
Goal
+ Capabilities
+ Knowledge
+ Permissions
+ Budget
+ Risk
      ↓
Harness
      ↓
Single / Workflow / Multi-Agent / Hybrid
```

Agent Team 本身可以是运行时结果。

### 9.4 Work Frontier

Work Frontier 是当前独立、可领取、可验证的 Work Item 集合。

> **Effective Parallelism ≈ Independent Work Fronts。**

Multi-Agent 的关键是 Work Scheduler，而不是 Agent Scheduler。

### 9.5 Shared State + Local Isolation

Shared-world 协作需要：

- Shared Resource；
- Local Workspace；
- resource identity / version；
- ownership / lease；
- snapshot / change；
- conflict handling。

协作可以通过环境状态发生，不必全部依赖 Agent-to-Agent message。

### 9.6 Local Recovery + Global Reconciliation

Child 局部失败优先局部恢复；结果回到 Parent 重新协调全局计划。

### 9.7 两层并发

- Delegation Concurrency；
- Action / Tool Concurrency。

两层拥有独立预算和背压策略。

### 9.8 Trust-aware Agent Handoff

Agent-to-Agent Result 不应该只是一段文本：

```text
Agent Message / Delegation Result
├── semantic_type
├── content
├── provenance
├── evidence_refs
├── confidence
└── trust_label
```

Transformation 不自动提升 Trust。

## 10. Agent Work Environment

```text
Agent Work Environment
├── Shared Resources
├── Local Workspace
├── Programmatic Execution Runtime
├── Work Discovery
├── Ownership / Lease
├── Observation Projection
├── Verification
├── Feedback / Oracle
├── Capability Proxy
├── Sandbox / Isolation
└── Telemetry Channel
```

### 10.1 Environment Engineering

Raw Result 需要转换成高信号 Observation，而不是把原始日志和 API Response 全部塞给模型。

### 10.2 Programmatic Execution Runtime

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

允许执行代码不等于允许调用任意业务 Capability。

### 10.3 Program Budget

治理：max_tool_calls、max_runtime、max_cost、max_parallelism、CPU / Memory、data read / write 等。

### 10.4 Generated Code Lifecycle

```text
Ephemeral Code
→ Run scoped

Workspace Code
→ Work scoped

Promoted Capability
→ Cross-Work platform asset
```

晋升为共享 Capability 前必须经过 Eval、安全检查、评审和版本化。

## 11. Data Plane

### 11.1 数据可见性

```text
Model-visible Data
Execution-only Data
Persistent Resource
```

Agent 系统可以被允许处理某些数据，而模型不被允许直接看到这些数据。

### 11.2 Data Flow Policy

```text
Source
+ Data Classification
+ Destination
+ Capability
+ Principal / Tenant
+ Purpose / Work Context
      ↓
Allow / Deny / Redact
```

Capability Permission 与 Data Flow Permission 不是同一个维度。

## 12. Evaluation Architecture

### 12.1 Trial 是基本单位

```text
Eval Suite
   └── Task
        └── Trial
             ├── Harness Revision
             ├── Capability Revisions
             ├── Environment Revision
             ├── Transcript / Trace
             ├── Outcome
             └── Grader Results
```

### 12.2 Transcript / Trace 与 Outcome

Trace 描述过程发生了什么；Outcome 描述执行后真实世界和结果是什么。

二者必须分离。

### 12.3 Evaluation Contract

```text
Evaluation Contract
├── Criterion
├── Evidence Source
├── Grader
├── Threshold / Criticality
└── Aggregation
```

### 12.4 Grader

- Deterministic；
- LLM Judge；
- Human。

Criterion、Evidence 和 Grader 分开建模。

### 12.5 非确定性

- pass@k：至少一次成功，更接近 Capability / Search Potential；
- pass^k：全部成功，更接近 Reliability。

### 12.6 Capability Eval 与 Regression Eval

Capability Eval 探索能力边界；成功案例逐渐晋升到 Regression Suite，守住已有能力。

### 12.7 Eval Infrastructure 与 Eval Content

平台负责 Runner、Environment、Trace、Grader SDK、Statistics、Versioning。

Domain / Capability Owner 负责 Tasks、Criteria、Rubrics、Reference Solutions、Failure Cases、Domain Graders。

> **Eval Infrastructure 是平台能力；Eval Content 是 Capability Asset。**

### 12.8 Eval 是 Capability Specification

```text
Harness
→ How to implement

Eval
→ How to prove
```

## 13. Verification Architecture

### 13.1 Verification Ladder

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

### 13.2 Differential Oracle

Verifier 应尽量告诉 Agent“差在哪里、下一步如何定位”，而不仅是 pass / fail。

### 13.3 Steward / Guardian

维护跨 Work Item 的长期质量维度，例如回归、架构约束、技术债和共享资源健康。

### 13.4 Cost per Successful Outcome

最终成本指标关注“一个成功 Outcome 需要多少总资源”，而不是单次 token / request 价格。

## 14. Security / Governance

安全目标可以理解为：

```text
Deployment Risk
≈ Failure Probability × Blast Radius
```

Model / Classifier / HITL 主要降低 Failure Probability；Containment 负责限制最大 Blast Radius。

### 14.1 三类风险来源

```text
User Misuse
Model Misbehavior
External Attack / Prompt Injection
```

因此需要 Defense in Depth：

```text
Behavioral Security
Content Security
Environment Security
```

### 14.2 Context Ingress Boundary

外部内容进入 Context 前经过：

```text
Raw Content
   ↓
Provenance
Trust Classification
Prompt Injection Detection
Data Inspection
Redaction / Sanitization
Policy
   ↓
Observation
   ↓
Context
```

可信 Tool 不等于可信 Tool Output。

### 14.3 Trust Lifecycle

```text
Discovered
  ↓
Untrusted
  ↓
Trusted for Read
  ↓
Trusted for Instruction
  ↓
Trusted for Execution
```

Locality 不等于 Trust。

对于 Agent，“读”本身可能影响行为，因此 Trust Boundary 需要覆盖 Parse、Load 和 Interpretation。

### 14.4 Trust Propagation

Trust 跟着数据 Provenance 传播，而不是因为信息经过内部 Agent 就自动升级。

```text
Transformation
≠ Trust Elevation
```

### 14.5 Agent Identity

推荐身份链：

```text
Human Principal
      ↓ delegates
Agent Principal
      ↓ narrows
Execution Principal
      ↓ uses
Scoped Credential
```

区分：

```text
Identity   → 我是谁
Delegation → 我代表谁
Authority  → 我能做什么
Credential → 我如何证明权限
```

### 14.6 Authorization Model

核心授权单元：

```text
Principal
× Delegation Chain
× Capability
× Resource
× Scope
× Duration
× Work Context
```

Delegation 传 Goal，不默认复制 Authority。

### 14.7 Just-in-Time Capability Grant

权限按 Work / Stage 动态收缩：

```text
Task Need
  ↓
Capability Request
  ↓
Policy
  ↓
Temporary Scoped Grant
  ↓
Execution
  ↓
Revoke / Narrow
```

Least Privilege 进一步扩展为：

```text
Least Privilege
× Least Duration
× Least Scope
```

### 14.8 Containment = Reachability Control

Containment 不只是 `sandbox=true`，而是控制当前 Agent 可触达的世界：

```text
Agent Reachability
├── Filesystem
├── Network
├── Credentials
├── Capabilities
├── Data
├── Memory
├── Other Agents
└── External Systems
```

目标是让每个 Work / Run / Child 的 Reachability Graph 尽可能小。

### 14.9 Containment Profile

```text
Containment Profile
├── isolation_mode
├── filesystem_scope
├── network_scope
├── credential_scope
├── resource_budget
├── allowed_capabilities
├── approval_boundary
└── user_oversight_level
```

隔离强度需要匹配 Risk、Autonomy 和 User Oversight Capability。

### 14.10 Egress Governance

Domain Allowlist 不够：一个域名可能承载大量不同 Capability 和 Tenant。

```text
Egress Governance
├── Destination
├── Protocol
├── Capability
├── Credential
├── Tenant / Principal
├── Data Classification
└── Provenance
```

> **Allowed Domain 本质上是一组 Capability Grant，而不是简单 Destination Filter。**

### 14.11 Memory Governance

长期 Memory 写入近似于修改未来 Agent 的启动 Context，因此需要：

- provenance；
- trust；
- promotion；
- validation；
- startup scan；
- trust-aware recall。

不可信内容被 Agent 总结后，不能自动变成高可信 Memory。

### 14.12 User Intent 与 Capability Boundary

来自 User 的 Instruction 也可能由攻击者诱导产生。

```text
Instruction Source
≠ Intent Origin
```

User Intent 定义目标，但系统 Capability Boundary 独立存在。

HITL 不应该承担用户根本无法理解的底层安全决策。

### 14.13 Containment 与 Observability

强 Isolation 可能降低 Host Visibility，因此需要 Out-of-band Telemetry Channel。

```text
Governance
= Policy
+ Enforcement
+ Observability
```

### 14.14 Battle-tested Primitives

Agent-specific 创新优先放在 Governance / Policy Composition；Isolation / Enforcement 尽量复用成熟基础设施：

- Hypervisor；
- OS Sandbox；
- seccomp / namespace；
- filesystem ACL；
- firewall / proxy；
- IAM / scoped credential；
- resource limit。

> **Governance 决定边界画在哪里；Infrastructure 保证 Agent 越不过这条边界。**

## 15. Observability / Trace

### 15.1 Agent Trace

用于理解 Agent 为什么这么做：

- model step；
- tool selection；
- delegation；
- evaluation；
- outcome。

### 15.2 Runtime Trace

围绕 Work / Session / Run / Event / Action 记录完整执行关系。

### 15.3 Security Trace

来自更接近 Enforcement 的位置：

- process spawn；
- filesystem access；
- network egress；
- credential use；
- policy decision；
- sandbox violation。

Agent Trace 与 Security Trace 可以通过 work_id、session_id、run_id、action_id、correlation_id 关联，但不应完全依赖同一个采集机制。

### 15.4 PTC Trace

层级关系：

```text
Reasoning Step
  ↓
Program
  ├── Action A
  ├── Action B
  ├── Action C
  └── Policy Decisions
```

不能只记录 `CodeExecutionSucceeded`。

## 16. Recovery / Escalation

### Recovery

解决当前能力范围内的暂时故障：

- worker restart；
- Harness crash；
- temporary tool failure；
- retryable action failure。

### Escalation

解决能力边界：

- 更强模型；
- Specialist Capability；
- Human Decision；
- 新 Tool；
- Scope Reduction。

> **Recovery 解决暂时失败；Escalation 解决能力上限。**

## 17. Harness Engineering

Harness 是持续实验对象：

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

Harness Revision、Skill Revision、Tool Revision、Grader Revision 都应该被版本化。

Harness 发布不等于正在执行 Session 自动迁移。

## 18. Capability Lifecycle

系统中的可复用能力应该经过明确生命周期：

```text
Capability Gap
   ↓
Candidate
   ↓
Prototype
   ↓
Capability Eval
   ↓
Security / Governance Review
   ↓
Publish Revision
   ↓
Regression Eval
   ↓
Production Feedback
   ↓
Revise / Deprecate
```

对于生成代码：

```text
Ephemeral Code
→ Workspace Code
→ Candidate Capability
→ Eval / Review
→ Skill / Tool / Other Reusable Capability
```

Agent 可以提出 Candidate，但不能在活跃生产 Session 中无治理地自发布。

## 19. Human Governance Plane

随着 Agent 自主性增强，人类角色从：

```text
逐步指导 Execution Path
```

转向：

```text
Governance Plane
├── Goal
├── Capability / Acceptance
├── Risk Boundary
├── Budget
├── Escalation
├── Production Acceptance
└── Publish / Deploy Decision
```

HITL 仍然重要，但它应主要承担人类有能力做出的语义决策，而不是替代 Sandbox、Credential Isolation、Egress Policy 等系统硬边界。

## 20. 核心架构不变量

1. **应用形态不等于执行范式。**
2. **Workflow 与 Agent 的核心区别是执行控制权归属。**
3. **Runtime 管理执行事实，Harness 管理执行策略，Business Layer 管理工作意图。**
4. **Runtime 应稳定，Harness 应可替换、可简化甚至消失。**
5. **Work 是长期连续性的载体；Agent、Session、Context 都可以被替换或重建。**
6. **Work、Session、Run 分别表示长期工作、Agent 与 Work 的连续关系、一次触发后的连续执行片段。**
7. **Event 是事实，State 是投影，Snapshot 是优化。**
8. **Context 是 Working Set 和 Query Projection，不是 Source of Truth。**
9. **Compaction 改变模型看到什么，不改变真实历史。**
10. **Notes 是主观工作认知，Memory 是跨时间保留信息，Workspace 是外部工作状态，Artifact 是正式产物。**
11. **Tool 是行动能力，Skill 是程序性知识，MCP 是连接标准，Harness 是当前执行策略。**
12. **Agent 可以由 Base Agent + Skill + Tool + Knowledge + Task Context 动态组装。**
13. **Capability Discovery 与 Loading 必须分离。**
14. **Deterministic mechanics 下沉到 Capability，uncertain decisions 留给 Harness。**
15. **Result 是执行事实，Observation 是模型面对的投影。**
16. **LLM 应是 Control Plane，而不是 Data Plane。**
17. **PTC 是 Execution Strategy，不是 Tool Type；一个 Reasoning Step 可以展开多个受治理 Action。**
18. **Code Permission 不等于 Business Capability Permission。**
19. **Multi-Agent 的关键不是 Agent 数量，而是 Work Frontier 和共享 Work Environment。**
20. **Lead Agent 负责全局编排和 Global Context；Child Session 负责局部自治工作。**
21. **Delegation 传递 Goal，不默认复制 Authority。**
22. **Trial 是 Agent Eval 的基本单位；Transcript / Trace 与 Outcome 分离。**
23. **Outcome 是事实，Eval Score 是 Measurement Projection。**
24. **Eval 是可执行 Capability Specification：Harness 说明怎么实现，Eval 说明怎么证明。**
25. **Capability Eval 探索能力边界，Regression Eval 守住已获得能力。**
26. **Execution、Verification、Acceptance 和 Publish / Deploy 状态必须分离。**
27. **Agent Security 同时治理 Context Ingress、Trust Propagation、Execution Boundary 和 Egress。**
28. **可信 Capability 不代表可信 Observation。**
29. **Trust 跟随 Provenance，不因经过内部 Agent 或 Agent Summary 自动升级。**
30. **User Intent 可以定义目标，但不能自动扩大 Capability Boundary。**
31. **Agent 应成为可独立授权、审计和撤销的 Principal，同时保留 Human Delegation Chain。**
32. **Containment 的本质是 Reachability Control：让 Agent 可达世界保持任务所需最小范围。**
33. **Least Privilege 还要结合 Least Duration 与 Least Scope。**
34. **Probabilistic Defense 降低失败概率，Deterministic Containment 限制最大后果。**
35. **Governance 定义边界；成熟 Infrastructure 执行边界。**
36. **Governance = Policy + Enforcement + Observability。**
37. **Human 应逐渐从 Execution Path 移向 Goal、Risk、Acceptance 和 Escalation 所在的 Governance Plane。**

## 21. 一句话总结

> **Agent Platform 的核心，不是“跑一个 Agent Loop”，而是把一个动态组装、非确定、长期、并行、可编程的智能执行过程，约束在持久、可恢复、可验证、可观测、可治理、能够持续演进的生产系统中。**
