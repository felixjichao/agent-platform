# 智能体平台总体架构

本文档记录 Agent Platform 当前已经形成的规范性架构结论，并随着研究持续演进。

> 当前版本已吸收《Building effective agents》和《Scaling Managed Agents: Decoupling the brain from the hands》的架构结论。

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

其中：

- 业务 / 产品决定要完成什么；
- 执行策略与 Harness 决定当前如何推进；
- 统一运行时保存持久执行事实；
- 执行环境负责真正观察和作用于外部世界。

## 2. 核心设计原则

### 2.1 应用形态与执行范式分离

对话、研究、知识库、Coding 等是应用形态；直接执行、工作流和智能体是执行范式。两者不建立一一对应关系。

### 2.2 执行控制权是工作流与智能体的核心边界

- 工作流：下一步主要由预定义代码或图决定。
- 智能体：下一步主要由模型根据当前上下文动态决定。

运行时不绑定某一种控制方式。

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

复杂度和自主性应按任务需要逐渐增加。

### 2.4 Runtime 稳定，Harness 可替换

Harness 编码了“当前模型还需要哪些脚手架”的假设，这些假设会随着模型能力变化。

因此：

> **Runtime should be stable; Harness should be replaceable.**

Harness 可以增删计划、评估、上下文重置等策略，但 Session、持久事实、动作执行和恢复能力不能依赖某个 Harness 进程长期存在。

### 2.5 脑与手解耦

模型与 Harness 构成控制侧；Execution Environment 构成执行侧。两侧通过稳定的动作接口连接。

```text
模型 + Harness
    │
    │ Action Request
    ▼
Execution Environment
    │
    ▼
Result / Observation
```

## 3. 当前软件栈

```text
L5 业务 / 产品
   Goal · Application

L4 执行策略 / Harness
   Direct · Workflow · Agent Loop · Harness

L3 统一运行时
   Session · Execution · State · Action · Result

L2 执行环境
   Sandbox · API · MCP · DB · Browser · Filesystem

L1 基础设施 / 真实世界
   Compute · SaaS · Data · Devices
```

这一分层仍会继续演进，但“策略—运行时—执行环境”的边界已经开始稳定。

## 4. 核心领域边界

### 4.1 Session

Session 不是简单聊天记录，而是一个 Agent 持续执行关系中的持久历史容器。它回答：

> **发生过什么？**

长期事实必须独立于 Harness 生命周期保存。

### 4.2 Harness

Harness 是当前模型的执行脚手架，负责：

- 当前如何推进任务；
- 如何规划或循环；
- 什么时候评估；
- 什么时候结束或继续。

这些属于策略，不应过早固化为 Runtime Core。

### 4.3 Execution Environment

执行环境回答：

> **Agent 实际在哪里、以什么方式行动？**

它可以是 Sandbox，也可以是 API、MCP、数据库、浏览器、远程计算机或设备。Sandbox 是一种实现，不是平台唯一抽象。

## 5. 执行策略

### 5.1 工作流控制原语

典型模式可以归约为：

- 顺序执行（Sequence）
- 条件分支（Branch）
- 分叉 / 汇合（Fork / Join）
- 循环（Loop）
- 动态展开（Dynamic Expansion）

工作流 DSL 和 DAG 属于上层表达，可以映射到这些控制能力。

### 5.2 工作流图与智能体执行图

```text
Workflow Graph
= 执行前给定的输入结构

Agent Graph
= 运行过程中动态形成的执行结果
```

统一运行时不以固定 DAG 作为唯一事实模型。

### 5.3 多智能体的位置

多智能体暂时视为更高层执行拓扑，而不是统一运行时的基础原语。

## 6. 持久状态原则

真正影响恢复、审计和后续执行的状态必须进入运行时持久层：

```text
Harness
  ↓ append / read
Durable Session State
  ↓ recover
New Harness
```

Harness 可以短生命周期甚至无状态化；Session 的持续时间可以远长于 Harness 进程。

## 7. 当前架构不变量

1. **应用形态不等于执行范式。**
2. **工作流与智能体的核心区别是执行控制权归属。**
3. **统一运行时负责承载持久执行事实，不固化某一种“下一步如何决定”的策略。**
4. **静态工作流、动态计划和 Agent Loop 是执行控制逐渐动态化的连续谱。**
5. **Workflow Graph 是输入表达；Agent Graph 更接近运行时结果。**
6. **Session、Harness、Execution Environment 分别回答“发生了什么、怎么推进、在哪里行动”。**
7. **持久状态不能依赖 Harness 进程。**
8. **Runtime 应稳定，Harness 应可替换、可简化甚至消失。**
9. **Sandbox 是执行环境的一种实现，而不是执行环境本身。**
