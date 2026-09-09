# 智能体平台总体架构

本文档记录 Agent Platform 当前已经形成的规范性架构结论，并随着研究持续演进。

> 当前版本已吸收《Building effective agents》《Scaling Managed Agents》和《Effective context engineering for AI agents》的架构结论。

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

同时，上下文不是一条独立的持久状态链，而是由多个持久来源动态构建的模型工作集。

## 2. 核心设计原则

### 2.1 应用形态与执行范式分离

对话、研究、知识库、Coding 等是应用形态；直接执行、工作流和智能体是执行范式。两者不建立一一对应关系。

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

Harness 编码了当前模型需要的执行脚手架；Session、持久事实、动作执行和恢复能力不能依赖某个 Harness 进程长期存在。

### 2.5 Context 是投影，不是事实源

> **Session 追加事实，Context 选择性投影。**

Context 丢失后应能从 Session、State、Memory、Notes、Artifacts、Workspace 等来源重新构建。

### 2.6 Context 是工作集

Context 的目标不是包含全部世界，而是对当前决策足够。它应该保留“地图”和导航入口，而不是把所有资源一次性塞入模型窗口。

## 3. 当前软件栈

```text
L5 业务 / 产品
   Goal · Application

L4 执行策略 / Harness
   Direct · Workflow · Agent Loop · Harness · Context Strategy

L3 统一运行时
   Session · State · Action · Result · Resource

L2 执行环境
   Workspace · Sandbox · API · MCP · DB · Browser · Filesystem

L1 基础设施 / 真实世界
   Compute · SaaS · Data · Devices

横切：Context / Memory
```

## 4. 核心领域边界

### 4.1 Session

Session 不是聊天记录，而是一个 Agent 持续执行关系中的持久历史容器。它回答“发生过什么”。

### 4.2 State

State 是当前执行状态的可变视图，用于快速回答“现在是什么状态”。它不是完整历史。

### 4.3 Context

Context 是当前模型调用的工作集：

```text
Session
State
Memory
Notes
Artifacts
Workspace
Skills / Capabilities
External Resources
      ↓
Context Builder
      ↓
Context
```

因此：

> **Session != Chat History != Context Window。**

### 4.4 Harness

Harness 负责当前任务如何推进，以及如何规划、评估、压缩上下文或结束任务。它属于策略层。

### 4.5 Execution Environment

执行环境描述 Agent 实际可以观察和操作的世界，包括 Sandbox、API、MCP、数据库、浏览器、文件系统和远程设备。

## 5. 上下文与持久资源

### 5.1 Context Builder

Context Builder 是 Harness 的策略组件，负责：

- 选择相关历史；
- 加载必要 Memory；
- 读取 Notes / Artifact / Workspace；
- 按需加载 Skill、Tool 定义或外部知识；
- 做摘要、压缩和排序。

### 5.2 稳定信息与即时加载

Context 可以按变化频率分成：

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

这既减少无关信息，也有利于 Prompt Cache。

### 5.3 Compaction

Compaction 属于 Context Strategy：

```text
Session facts
    ↓
select / summarize / compact
    ↓
Context
```

它不应该删除或重写真实历史。摘要是派生资源，而不是新的 Source of Truth。

### 5.4 Notes、Memory、Workspace、Artifact

- **Notes / Todo**：Agent 当前主观工作认知，可能被修改或证明错误。
- **Memory**：跨时间保留、未来可召回的信息。
- **Workspace**：外部持久工作状态，如文件、代码、中间结果和 Checkpoint。
- **Artifact**：正式结果或交付物，具有版本、评审或发布语义。

它们可以共享底层资源存储，但语义必须分开。

## 6. 执行策略

### 6.1 工作流控制原语

典型模式可以归约为顺序执行、条件分支、分叉 / 汇合、循环和动态展开。

### 6.2 工作流图与智能体执行图

```text
Workflow Graph = 执行前给定的输入结构
Agent Graph    = 运行过程中动态形成的执行结果
```

### 6.3 Sub-agent 的边界

需要区分：

- **Agent-as-Tool**：一次聚焦调用，可作为 Parent Session 中的一次 Action。
- **Autonomous Sub-agent**：具有独立目标、多轮上下文、Artifact 和恢复需求，应使用 Child Session。

Sub-agent 的重要价值是上下文隔离和卸载，而不仅是增加模型实例。

## 7. 持久状态原则

真正影响恢复、审计和后续执行的状态必须进入运行时持久层。Harness 可以短生命周期甚至无状态化。

## 8. 当前架构不变量

1. **应用形态不等于执行范式。**
2. **工作流与智能体的核心区别是执行控制权归属。**
3. **统一运行时负责持久执行事实，不固化某一种执行控制策略。**
4. **静态工作流、动态计划和 Agent Loop 是连续谱。**
5. **Workflow Graph 是输入表达；Agent Graph 更接近运行时结果。**
6. **Session、Harness、Execution Environment 分别回答“发生了什么、怎么推进、在哪里行动”。**
7. **持久状态不能依赖 Harness 进程。**
8. **Runtime 稳定，Harness 可替换、可简化甚至消失。**
9. **Context 是持久事实的可重建投影，不是 Source of Truth。**
10. **Context 是当前 Working Set，不是整个世界。**
11. **Compaction 改变模型看到什么，不改变真实发生过什么。**
12. **Agent-as-Tool 是 Action；真正自治且需要持久生命周期的 Sub-agent 才是 Child Session。**
