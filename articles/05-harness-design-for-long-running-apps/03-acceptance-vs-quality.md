# Acceptance Criteria 与 Quality Criteria

## 文章中的关键观点

文章中的长时间应用开发 Harness 不仅检查功能是否存在，还需要从最终用户体验、完整性和质量角度持续评估。

## 我们的架构分析

可以区分两种标准：

### Acceptance Criteria

回答：

> **最低什么条件满足，任务才算完成？**

通常适合明确、可验证的二元条件，例如测试通过、接口存在、功能可运行。

### Quality Criteria

回答：

> **结果做得有多好？**

可能包含可用性、代码质量、一致性、视觉质量、鲁棒性等连续维度。

如果二者混在一起，容易出现：

- 只有质量评分，没有硬验收门槛；
- 只有“测试过了”，却没有整体质量判断。

## 对 Agent Platform 的影响

平台应允许一个 Work 同时拥有硬性 Acceptance Contract 和多维 Quality Evaluation，两者使用不同聚合方式。

## 核心结论

> **Acceptance 决定能否结束，Quality 描述完成得有多好。**