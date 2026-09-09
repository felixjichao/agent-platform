# 上下文是工作集，不是全部世界

## 文章中的关键观点

文章把上下文工程定义为：在不断增长的潜在信息空间中，持续选择当前推理真正需要的 token。上下文窗口有限，因此“放得越多越好”并不是正确策略。

## 我们的架构分析

可以把 Context 理解为操作系统里的 Working Set：

```text
完整世界
├── Session 历史
├── 外部知识
├── 工具定义
├── Workspace
├── Memory
├── Notes
└── Artifacts
        ↓ 选择 / 压缩 / 组织
      Context
```

上下文的目标不是完整，而是**对当前决策足够**。

因此应避免两个极端：

- 把所有历史永久塞进 Context；
- 只保留极短摘要，导致 Agent 失去必要事实和导航能力。

更好的心智模型是：

> **Context contains a map, not the whole world.**

模型看到的是当前可用世界的地图，并能在需要时继续导航和加载。

## 对 Agent Platform 的影响

Context 不应作为唯一状态存储。真正长期的数据应该存在 Session、Workspace、Memory、Artifact 等持久来源中，Context 只负责当前模型调用的工作集。

## 核心结论

> **Context 是有限的工作集，而不是 Agent 世界状态本身。**