# Notes、Memory 与 Workspace 的边界

## 文章中的关键观点

文章强调 Agent 可以通过 notes 等外部化方式记录进度，也可以通过文件系统等环境把信息移出上下文窗口。

## 我们的架构分析

需要避免把所有“上下文之外的信息”都称为 Memory。

### Notes / Todo

Agent 当前的主观工作记忆：

- 当前假设；
- 计划；
- 待办；
- 临时结论。

它可能出错，也可能被修改。

### Memory

跨时间保留并在未来召回的信息，可进一步区分工作记忆、情景记忆和语义记忆。

### Workspace

外部持久工作状态：

- 文件；
- 代码；
- 中间结果；
- Checkpoint；
- 可执行程序。

它描述的是“工作世界”，而不是模型脑内记忆。

### Artifact

正式结果或交付物，需要版本化、评审或发布语义。

## 对 Agent Platform 的影响

这些资源可以共享底层 Resource Store，但必须保留不同语义。Note 可以被提升为 Artifact，Session 中的经验也可以经过整理进入长期 Memory，但不能把它们混成一个 KV Store。

## 核心结论

> **Notes 是当前工作认知，Memory 是跨时间保留的信息，Workspace 是外部工作状态，Artifact 是正式结果。**