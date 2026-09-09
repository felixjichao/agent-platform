# 智能体平台总体架构

本文档记录 Agent Platform 当前已经形成的规范性架构结论，并随着研究持续演进。

> 当前版本已吸收前五篇研究：执行控制、Managed Agents、上下文工程、长任务连续性，以及长时间应用开发 Harness 设计。

## 1. 架构主张

Agent Platform 不按对话、科研、知识库、工作流等产品形态分别建设执行内核，而是围绕稳定的平台边界组织：

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

- 业务层决定要完成什么；
- Harness 决定当前怎么完成；
- Evaluation Contract 决定怎样证明完成；
- Runtime 保存真实执行事实并支持恢复；
- Execution Environment 负责真正作用于外部世界。

## 2. 核心设计原则

### 2.1 应用形态与执行范式分离

对话、研究、知识库、Coding 等是应用形态；Direct、Workflow、Agent Loop 等是执行范式。

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
```

### 2.4 Runtime 稳定，Harness 可替换

Harness 是对当前模型能力缺口的适应性脚手架。Planner、Evaluator、Context Reset 等组件必须允许被版本化、实验、替换或删除。

### 2.5 Context 是可重建投影

> **Session 追加事实，Context 选择性投影。**

Context 是当前 Working Set，不是持久事实源。

### 2.6 长任务依靠恢复而不是无限 Context

持续工作依赖 Durable State、Handoff、Workspace 和 Recovery，而不是让一个 Context 无限增长。

### 2.7 Execution State 与 Acceptance State 分离

“执行结束”不等于“结果被接受”。生成结果和验证结果需要独立建模。

## 3. 当前软件栈

```text
L6 业务 / 产品
   Goal · Requirement · Application

L5 能力契约
   Acceptance Criteria · Quality Criteria · Evaluation Contract

L4 执行策略 / Harness
   Direct · Workflow · Agent Loop
   Planning · Context Strategy · Bootstrap · Evaluator

L3 统一运行时
   Session · State · Action · Result · Resource · Recovery

L2 执行环境
   Workspace · Sandbox · API · MCP · DB · Browser · Filesystem

L1 基础设施 / 真实世界
   Compute · SaaS · Data · Devices

横切：Context / Memory · Trace
```

## 4. 核心领域边界

### 4.1 Session

Session 是一个 Agent 持续执行关系中的持久历史容器，回答“发生过什么”。它不等于聊天记录或 Context Window。

### 4.2 State

State 是根据持久事实形成的当前执行视图，用于快速回答“现在是什么状态”。

### 4.3 Context

Context 由多个来源动态投影：

```text
Session / State / Memory / Notes / Artifacts / Workspace
                         ↓
                   Context Builder
                         ↓
                      Context
```

### 4.4 Harness

Harness 负责“当前如何推进”，可以包含：

- Planner；
- Evaluator；
- Context Strategy；
- Bootstrap；
- Handoff；
- Completion / Escalation Strategy。

这些机制默认属于策略层，而不是 Runtime primitive。

### 4.5 Execution Environment

执行环境描述 Agent 实际可以观察和操作的世界。Sandbox 是其中一种实现，而不是平台唯一抽象。

### 4.6 Recovery

Recovery 恢复执行环境、加载持久资源、重建状态并重新校验 Ground Truth。恢复不能只相信 Progress / Notes。

## 5. 能力契约与验收

### 5.1 Plan 与 Evaluation Contract

```text
Plan
→ How to do

Evaluation Contract
→ How to prove it is done
```

Plan 可以随着执行快速变化；Evaluation Contract 应相对稳定。

### 5.2 Acceptance Criteria 与 Quality Criteria

- **Acceptance Criteria**：最低什么条件满足，任务才允许结束。
- **Quality Criteria**：结果完成得有多好，通常是多维连续指标。

两者不能用一个模糊总分替代。

### 5.3 Evaluation Contract 结构

```text
Evaluation Contract
├── Criterion
├── Evidence
├── Grader / Verifier
├── Threshold
└── Aggregation
```

平台需要让验收标准和证据结构成为可共享资源，而不是只藏在 Prompt 中。

### 5.4 Generator / Evaluator 分离

Generator 产生候选结果，Evaluator 根据独立标准验证。逻辑分离比“是否使用两个模型实例”更重要。

> **Execution State != Acceptance State。**

## 6. 长任务连续性

### 6.1 Durable Handoff

Handoff 至少回答：

```text
What remains?
→ Goal / Acceptance / Remaining Work

What happened?
→ 已完成事实、结果和失败尝试

How to resume?
→ Workspace、环境、版本、测试和恢复入口
```

### 6.2 Progress / Notes 是投影

```text
Runtime Events / Git / Test / Artifact / Workspace
                    ↓
               Progress View
                    ↓
                 Context
```

当 Progress 与真实状态冲突时，应重新校验 Ground Truth。

### 6.3 Bootstrap 属于 Harness

Initializer、Planner、Reviewer 等具体角色不直接进入 Runtime Core。

## 7. 上下文与持久资源

### 7.1 Context Builder

负责选择历史、加载 Memory、读取 Notes / Artifacts / Workspace、即时加载能力和知识，并做摘要和压缩。

### 7.2 Compaction

Compaction 改变模型看到什么，不改变真实发生过什么。摘要是派生资源。

### 7.3 Notes、Memory、Workspace、Artifact

- Notes / Todo：当前主观工作认知。
- Memory：跨时间保留并可召回的信息。
- Workspace：文件、代码、中间结果和 Checkpoint 等外部工作状态。
- Artifact：正式结果或交付物。

## 8. 执行策略

### 8.1 工作流控制原语

顺序执行、条件分支、分叉 / 汇合、循环和动态展开构成基础控制能力。

### 8.2 Workflow Graph 与 Agent Graph

```text
Workflow Graph = 执行前给定的输入结构
Agent Graph    = 运行过程中动态形成的执行结果
```

### 8.3 Sub-agent

- Agent-as-Tool：聚焦调用，可作为 Parent Session 中的一次 Action。
- Autonomous Sub-agent：需要独立目标、多轮上下文和恢复时，使用 Child Session。

## 9. Harness 工程

Harness 的每个组件都隐含一个“模型当前做不到”的假设，因此需要持续实验：

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

复杂度必须通过结果证明。模型升级后，应重新验证 Planner、Evaluator、Context Reset 等组件是否仍然必要。

Harness Revision 与 Session 生命周期分离；发布新 Harness 不意味着隐式迁移正在执行的 Session。

## 10. 当前架构不变量

1. **应用形态不等于执行范式。**
2. **Workflow 与 Agent 的核心区别是执行控制权归属。**
3. **统一运行时承载持久执行事实，不固化某一种控制策略。**
4. **静态 Workflow、动态 Plan 和 Agent Loop 是连续谱。**
5. **Workflow Graph 是输入表达；Agent Graph 更接近运行时结果。**
6. **Session、Harness、Execution Environment 分别回答“发生了什么、怎么推进、在哪里行动”。**
7. **持久状态不能依赖 Harness 进程。**
8. **Runtime 稳定，Harness 可替换、可简化甚至消失。**
9. **Context 是持久事实的可重建投影和当前 Working Set。**
10. **Compaction 改变模型看到什么，不改变真实历史。**
11. **长任务连续性来自 Durable State + Handoff + Recovery。**
12. **Progress / Notes 是 Handoff Projection，不是 Source of Truth。**
13. **Recovery 必须重新校验 Ground Truth。**
14. **Plan 负责怎么做，Evaluation Contract 负责如何证明已经做成。**
15. **Execution State 与 Acceptance State 必须分离。**
16. **Acceptance 决定能否结束，Quality 描述完成得有多好。**
17. **Harness 复杂度必须由 Trace + Eval 的结果证明。**
