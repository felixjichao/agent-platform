# Steward、Verifier 与长期质量

## 文章中的关键观点

大规模并行 Agent 容易局部优化：每个 Agent 都修自己的问题，但系统整体质量、回归和长期一致性可能持续恶化。因此实验中需要专门关注测试、清理、合并和质量维度的角色。

## 我们的架构分析

可以区分两类职责：

### Verifier

判断一个 Work Item 或系统状态是否满足验证条件，防止“Agent 说完成了”直接变成已完成事实。

### Steward / Guardian

持续维护跨 Work Item 的长期质量，例如：

- 回归测试；
- 代码一致性；
- 技术债；
- 架构约束；
- 共享资源健康度。

Steward 不一定是固定 Agent 类型，也可以是周期性 Capability / Harness Role。

## 对 Agent Platform 的影响

Work Item 需要区分执行状态和验证状态；系统还需要允许横跨多个 Work Item 的持续质量任务存在。

## 核心结论

> **局部完成不会自动产生全局质量；Verifier 保护完成边界，Steward 保护长期系统属性。**