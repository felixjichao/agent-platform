# Initializer 是 Harness 启动策略

## 文章中的关键观点

文章使用 initializer agent 建立初始项目结构、测试和进度文件，使后续多个 coding session 能在稳定基础上继续。

## 我们的架构分析

Initializer 很有用，但不应因为它在某个 Harness 中效果好，就升级成 Runtime 的核心概念。

它更像：

> **Harness Bootstrap Strategy。**

不同任务可能采用完全不同的启动策略：

- 初始化仓库和测试；
- 建立 Work Frontier；
- 加载现有 Workspace；
- 读取上次 Checkpoint；
- 对真实环境进行健康检查。

运行时真正需要支持的是“能够启动 / 恢复一个 Run，并读取持久资源”，而不是硬编码某个 initializer 角色。

## 对 Agent Platform 的影响

Initializer、Planner、Reviewer 等角色都先归入 Harness。只有当跨多个 Harness 都稳定存在且具备明确持久语义时，才考虑下沉为平台原语。

## 核心结论

> **不要把某个成功 Harness 的角色设计误当成 Runtime Domain Model。**