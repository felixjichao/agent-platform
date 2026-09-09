# Durable Handoff：告诉下一轮还剩什么

## 文章中的关键观点

文章通过进度文件、明确功能列表、Git 状态等方式，让下一次全新的 Agent 能够继续工作。

## 我们的架构分析

可靠 Handoff 至少要回答三类问题：

```text
What remains?
→ 目标、验收标准、剩余工作

What happened?
→ 已完成事实、关键决策、失败尝试

How to resume?
→ Workspace、环境、分支、测试、启动方式
```

这里最重要的是 **What remains**。如果只保存“我做了什么”，新 Agent 很容易因为看到大量进展而误判完成度。

Handoff 不需要保存完整 private reasoning。真正需要的是：

- 可恢复的执行事实；
- 当前状态；
- 未完成项；
- 必要证据和资源引用。

## 对 Agent Platform 的影响

可以把 Handoff 理解为从 Session / Work 持久状态构建出的一个恢复投影。不同 Harness 可以有自己的格式，但底层事实应来自 Runtime 和 Workspace。

## 核心结论

> **好的 Handoff 不是“上一轮说了什么”，而是“下一轮需要哪些可验证信息才能继续”。**