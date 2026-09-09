# LLM 应是 Control Plane，而不是 Data Plane

## 文章中的关键观点

直接 Tool Call 模式中，大量工具定义和中间结果反复进入 Context，既消耗 token，也会把模型变成数据搬运通道。代码执行允许中间数据留在程序内部。

## 我们的架构分析

传统 Agent 容易让 LLM 同时承担：

```text
Reasoning
+ Orchestration
+ Data Transportation
```

更合理的是：

```text
Agent / Harness
= Execution Control Plane

Execution Environment
= Data + Action Plane
```

模型负责：

- 定义目标；
- 选择策略；
- 生成 / 调整程序；
- 解释关键 Observation；
- 做高价值判断。

执行环境负责：

- 批量调用；
- 循环；
- join；
- filter；
- aggregate；
- 临时数据传输。

这还意味着：

> **One Reasoning Step may produce many Environment Actions。**

## 对 Agent Platform 的影响

Runtime 不能假设 `1 Model Step = 1 Tool Call`。Program execution 下面可能展开几十、几百个受治理 Action。

## 核心结论

> **LLM 应成为执行控制面，而不是高成本数据平面。**