# Task Spec 与 Eval Environment

## 文章中的关键观点

很多看起来像 Agent failure 的问题，实际上来自模糊任务、错误 grader、环境差异或 Eval Harness bug。因此高质量 Eval 首先依赖高质量 Task。

## 我们的架构分析

一个 Eval Task 至少需要描述：

```text
Task Spec
├── Initial State
├── Goal
├── Constraints
├── Available Capabilities
├── Expected / Acceptable Outcomes
├── Evaluation Criteria
└── Environment Requirements
```

Reference Solution 的作用不是要求 Agent 走相同路径，而是验证 Task 本身是可解的、Grader 能正确识别成功。

Eval Environment 也必须：

- 与 Production 行为足够接近；
- 与其他 Trial 隔离；
- 可重置；
- 可观测；
- 对依赖版本进行固定。

否则分数测到的可能是基础设施噪声，而不是 Agent 能力。

## 对 Agent Platform 的影响

Task Spec、Environment Revision 和 Grader Revision 都应成为 Trial 的显式依赖。失败分析需要能够归因到 Agent、Task、Grader、Harness 或 Environment。

## 核心结论

> **Eval 首先是一套实验系统；任务和环境定义错误时，分数本身没有意义。**