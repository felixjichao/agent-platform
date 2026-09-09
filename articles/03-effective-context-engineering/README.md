# Effective context engineering for AI agents

- 原文：<https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents>
- 研究主题：把上下文从“不断增长的聊天历史”重新定义为运行时动态构建的模型工作集。

## 小节

1. [上下文是工作集，不是全部世界](01-context-as-working-set.md)
2. [Context 是持久事实的投影](02-context-projection.md)
3. [预加载与即时加载](03-preload-vs-jit.md)
4. [压缩、缓存与上下文稳定性](04-compaction-and-cache.md)
5. [Notes、Memory 与 Workspace 的边界](05-notes-memory-workspace.md)
6. [Sub-agent 的核心价值是上下文隔离](06-sub-agent-context-isolation.md)

## 对平台架构的核心影响

- `Session != Context Window`。
- Context 应由 Context Builder 从 Session、State、Memory、Notes、Artifacts、Workspace 等来源按需投影。
- Compaction 是上下文策略，不应修改 Session 的事实历史。
- Sub-agent 的重要价值是隔离和卸载上下文，而不只是“增加一个模型实例”。