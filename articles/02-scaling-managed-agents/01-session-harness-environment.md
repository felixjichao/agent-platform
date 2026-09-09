# Session、Harness 与 Execution Environment

## 文章中的关键观点

Managed Agents 把长时间运行的 Agent 拆成相对独立的组成部分：持久会话、负责模型控制循环的 Harness，以及真正运行代码和工具的执行侧。

## 我们的架构分析

这三个概念解决的是完全不同的问题：

```text
Session
→ 发生过什么？

Harness
→ 当前应该怎样思考和推进？

Execution Environment
→ 实际可以在哪里、以什么方式行动？
```

Session 不应该退化成聊天记录；它更接近一个长期执行关系中的持久历史。Harness 也不是 Agent Platform 本身，而是围绕当前模型能力构建的执行脚手架。

## 对 Agent Platform 的影响

运行时开始出现三个稳定边界：

- 持久化边界：Session；
- 策略边界：Harness；
- 动作边界：Execution Environment。

平台接口应该围绕这三个边界设计，而不是把它们揉进一个 Agent 进程。

## 核心结论

> **Session 记录发生过什么，Harness 决定当前怎么推进，Execution Environment 负责真正行动。**