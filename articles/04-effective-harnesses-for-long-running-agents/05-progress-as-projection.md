# Progress / Notes 是 Handoff Projection

## 文章中的关键观点

文章实践中使用进度文件帮助新 Agent 快速了解工作状态。

## 我们的架构分析

进度文件很有价值，但它的正确定位是：

> **Handoff Projection，而不是 Source of Truth。**

例如：

```text
Event / Git / Test / Artifact / Workspace
              ↓
         Progress View
              ↓
          Next Agent
```

如果 progress.md 与实际代码或测试冲突，应以可验证事实为准。

这和 Context 的关系是一致的：

- Session / Workspace 保存真实状态；
- Progress 是面向 Agent 恢复的可读投影；
- Context 再从这些来源中选择当前工作集。

## 对 Agent Platform 的影响

平台可以允许 Harness 生成 Progress / Checkpoint / Handoff 资源，但应保留其派生性质和来源引用，避免把主观总结升级成事实库。

## 核心结论

> **Progress 是为续接而生成的状态视图，不是持久事实本身。**