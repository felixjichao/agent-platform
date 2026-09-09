# Skill Registry 与动态组合

## 我们的架构分析

Skill 不应该永久嵌入某个 Agent 定义中：

> **Agent uses Skill; Agent does not own Skill。**

理想 Skill 具有：

- independent；
- portable；
- versioned；
- discoverable；
- composable；
- governed。

于是一个运行时 Agent 可以被理解为动态组装结果：

```text
Base Agent
+ Selected Skills
+ Selected Tools
+ Retrieved Knowledge
+ Task Context
        ↓
Effective Agent
```

Skill 之间不需要预先构造固定 DAG。Harness 根据任务动态激活组合即可；真正存在强依赖时再在 Skill metadata 中表达 requirement。

## 对 Agent Platform 的影响

平台需要统一 Capability Catalog，至少支持 Procedural Capability（Skill）和 Action Capability（Tool）。Agent Definition 逐渐从“静态能力全集”转向“基础身份 + 动态能力选择”。

## 核心结论

> **Agent 可以在运行时由 Skill、Tool、Knowledge 和 Task Context 动态组装，而不是预先定义大量静态 Agent 类型。**