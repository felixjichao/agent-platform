# 智能体平台总体架构

本文档记录 Agent Platform 当前已经形成的规范性架构结论，并随着研究持续演进。

> 当前版本已吸收《Building effective agents》《Scaling Managed Agents》《Effective context engineering for AI agents》和《Effective harnesses for long-running agents》的架构结论。

## 1. 架构主张

Agent Platform 不应该按“对话 Agent、科研 Agent、知识库 Agent、工作流 Agent”等产品形态分别建设执行内核。

更稳定的抽象是：

```text
业务 / 产品
    ↓
执行策略
    ↓
Harness
    ↓
统一运行时
    ↓
Execution Environment
    ↓
真实世界
```

与此同时，长任务连续性不依赖一个模型上下文永久存在，而依赖持久事实、Workspace、Checkpoint 和 Recovery。

## 2. 核心设计原则

### 2.1 应用形态与执行范式分离

对话、研究、知识库、Coding 等是应用形态；直接执行、工作流和智能体是执行范式。

### 2.2 执行控制权是工作流与智能体的核心边界

- 工作流：下一步主要由预定义代码或图决定。
- 智能体：下一步主要由模型根据当前上下文动态决定。

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

Harness 编码当前模型所需脚手架；Session、持久事实、动作执行和恢复能力不能依赖某个 Harness 进程长期存在。

### 2.5 Context 是投影，不是事实源

> **Session 追加事实，Context 选择性投影。**

Context 可以从 Session、State、Memory、Notes、Artifacts、Workspace 等来源重建。

### 2.6 长任务依靠可恢复性，而不是无限 Context

一个执行轮次可以主动结束，只要下一轮能够从持久事实重新建立一致状态并明确剩余工作。

## 3. 当前软件栈

```text
L5 业务 / 产品
   Goal · Application

L4 执行策略 / Harness
   Direct · Workflow · Agent Loop · Context Strategy · Bootstrap · Handoff

L3 统一运行时
   Session · State · Action · Result · Resource · Recovery

L2 执行环境
   Workspace · Sandbox · API · MCP · DB · Browser · Filesystem

L1 基础设施 / 真实世界
   Compute · SaaS · Data · Devices

横切：Context / Memory
```

## 4. 核心领域边界

### 4.1 Session

Session 是一个 Agent 持续执行关系中的持久历史容器。它回答“发生过什么”，而不是“模型当前看见什么”。

### 4.2 State

State 是当前执行状态的可变视图，用于快速回答“现在是什么状态”。

### 4.3 Context

Context 是当前模型调用的工作集：

```text
Session / State / Memory / Notes / Artifacts / Workspace
                         ↓
                   Context Builder
                         ↓
                      Context
```

因此：

> **Session != Chat History != Context Window。**

### 4.4 Harness

Harness 负责当前任务如何推进，包括规划、评估、上下文压缩、Bootstrap、Handoff 和完成策略。这些属于策略层。

### 4.5 Execution Environment

执行环境描述 Agent 实际可以观察和操作的世界，包括 Workspace、Sandbox、API、MCP、数据库、浏览器、文件系统和远程设备。

### 4.6 Recovery

Recovery 是运行时需要提供的稳定能力：恢复执行环境、加载持久资源、重建当前状态，并允许 Harness 对真实环境进行一致性校验。

Recovery 不等于“重新读一份 progress.md”。

## 5. 长任务连续性

### 5.1 一个 Context 窗口只是一次工作班次

长任务需要接受一个事实：单轮上下文可能随时结束。因此每个执行阶段都应能够：

1. 在上下文耗尽前停止；
2. 保存必要持久事实；
3. 标记剩余工作；
4. 让下一轮重新进入任务。

### 5.2 Durable Handoff

可靠 Handoff 至少回答：

```text
What remains?
→ Goal / Acceptance / Remaining Work

What happened?
→ 已完成事实、关键结果、失败尝试

How to resume?
→ Workspace、环境、版本、测试和入口
```

Handoff 的目标是支持恢复，不是保存完整 private reasoning。

### 5.3 Progress / Notes 的定位

```text
Runtime Events / Git / Test / Artifact / Workspace
                    ↓
               Progress View
                    ↓
                 Context
```

Progress、Notes 和 Summary 都是投影。当它们与 Ground Truth 冲突时，必须重新校验。

### 5.4 Bootstrap 是 Harness 策略

Initializer、Planner、Reviewer 等具体角色属于 Harness。Runtime 只提供启动、恢复、持久资源和动作执行能力，不固化某一套角色架构。

## 6. 上下文与持久资源

### 6.1 Context Builder

Context Builder 负责选择相关历史、加载 Memory、读取 Notes / Artifacts / Workspace、按需加载能力或外部知识，并执行摘要和压缩。

### 6.2 稳定信息与即时加载

```text
稳定前缀
├── System / Policy
├── Agent Definition
└── Capability Metadata

阶段性稳定
├── Goal
├── Checkpoint
└── Summary / Plan

动态尾部
├── recent working history
├── tool observations
└── JIT resources
```

### 6.3 Compaction

Compaction 改变模型当前看到什么，不修改真实历史。摘要必须被视为派生资源。

### 6.4 Notes、Memory、Workspace、Artifact

- **Notes / Todo**：Agent 当前主观工作认知。
- **Memory**：跨时间保留并可召回的信息。
- **Workspace**：文件、代码、中间结果、Checkpoint 等外部工作状态。
- **Artifact**：正式结果或交付物。

## 7. 执行策略

### 7.1 工作流控制原语

典型模式可以归约为顺序执行、条件分支、分叉 / 汇合、循环和动态展开。

### 7.2 工作流图与智能体执行图

```text
Workflow Graph = 执行前给定的输入结构
Agent Graph    = 运行过程中动态形成的执行结果
```

### 7.3 Sub-agent 的边界

- Agent-as-Tool：一次聚焦调用，可作为 Parent Session 中的一次 Action。
- Autonomous Sub-agent：需要独立目标、多轮上下文、Artifact 和 Recovery 时，使用 Child Session。

## 8. 当前架构不变量

1. **应用形态不等于执行范式。**
2. **工作流与智能体的核心区别是执行控制权归属。**
3. **统一运行时承载持久执行事实，不固化某一种控制策略。**
4. **静态工作流、动态计划和 Agent Loop 是连续谱。**
5. **Workflow Graph 是输入表达；Agent Graph 更接近运行时结果。**
6. **Session、Harness、Execution Environment 分别回答“发生了什么、怎么推进、在哪里行动”。**
7. **持久状态不能依赖 Harness 进程。**
8. **Runtime 稳定，Harness 可替换、可简化甚至消失。**
9. **Context 是持久事实的可重建投影，不是 Source of Truth。**
10. **Context 是当前 Working Set，不是整个世界。**
11. **Compaction 改变模型看到什么，不改变真实发生过什么。**
12. **长任务连续性来自 Durable State + Handoff + Recovery，而不是无限增长的 Context。**
13. **Progress / Notes 是 Handoff Projection，不是 Source of Truth。**
14. **Recovery 必须回到 Ground Truth，并重新协调主观总结与真实状态。**
15. **Initializer 等具体角色属于 Harness Bootstrap Strategy，不属于 Runtime Core。**
