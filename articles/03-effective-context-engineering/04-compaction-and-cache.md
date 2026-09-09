# 压缩、缓存与上下文稳定性

## 文章中的关键观点

长任务最终会超过上下文窗口，因此需要压缩（Compaction）、摘要或上下文重置，使 Agent 能继续执行。

## 我们的架构分析

Compaction 不应该被理解为“删掉旧 Session 内容”。正确关系是：

```text
Session append facts
        ↓
Context Strategy
        ↓
select / summarize / compact
        ↓
Context
```

也就是说：

> **Session 追加事实；Context 选择性投影。**

原始事实仍然保留，摘要只是新的投影或辅助资源。这样后续恢复、审计或重新构建 Context 时仍能回到原始证据。

从缓存角度，Prompt 的稳定前缀应尽量少变，动态内容主要追加在尾部；否则上下文压缩本身可能带来巨大的缓存失效成本。

## 对 Agent Platform 的影响

Compaction 属于 Harness 的 Context Strategy，而不是 Runtime 对 Session 的破坏性修改。运行时只需要允许保存摘要、Checkpoint 等派生资源，并保留它们与来源事实的关联。

## 核心结论

> **Compaction 改变模型看到什么，不改变真实发生过什么。**