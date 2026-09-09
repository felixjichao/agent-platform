# 预加载与即时加载

## 文章中的关键观点

文章建议在预加载（preload）与即时加载（just-in-time）之间取得平衡。对 Agent 有稳定指导作用的信息适合提前进入上下文，大量、稀疏、任务相关性不确定的信息更适合按需获取。

## 我们的架构分析

Context 可以分成几类：

```text
稳定部分
├── System / Policy
├── Agent Definition
└── Tool / Capability 元数据

阶段性稳定部分
├── 当前 Goal
├── Checkpoint
├── 当前 Plan / Summary
└── 关键状态

动态部分
├── 最近工作历史
├── JIT Knowledge
├── Tool Result
└── External Resource
```

这个分层同时有两个价值：

1. 减少无关信息污染；
2. 提高 Prompt Cache 命中，避免每轮在前缀大幅变动。

## 对 Agent Platform 的影响

Capability、Skill、Memory 和 Knowledge 不应默认全量注入 Context。平台需要“发现”和“加载”分离，让 Agent 先知道有哪些资源，再在需要时取回具体内容。

## 核心结论

> **稳定信息前置，稀疏信息即时加载；Context 的组织目标既包括相关性，也包括前缀稳定性。**