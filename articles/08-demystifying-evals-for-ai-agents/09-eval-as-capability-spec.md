# Eval 是可执行的 Capability Specification

## 我们的架构分析

把前面的结论进一步推导，可以得到：Eval 不只是上线前测试，而是 Capability 的可执行定义。

```text
Requirement
   ↓
Capability Eval
   ↓
Harness / Skill / Tool Development
   ↓
Trial
   ↓
Gap Analysis
   ↓
Iteration
```

这使 Capability Contract 出现两个互补部分：

```text
Harness
→ 如何实现能力

Eval
→ 如何证明能力
```

一个 Capability 如果只有 Prompt / Harness，没有可重复 Eval，就很难知道：

- 它真的具备什么能力；
- 版本升级后是否退化；
- 新 Tool / Skill 是否真正改善结果；
- 什么时候可以进入 Production。

### Eval Infrastructure 与 Eval Content

平台负责：

- Runner；
- Environment；
- Trace；
- Grader SDK；
- Statistics；
- Versioning。

业务 / Capability Owner 负责：

- Task；
- Criterion；
- Rubric；
- Reference Solution；
- Domain Grader；
- Failure Cases。

## 对 Agent Platform 的影响

Eval 成为 Capability Engineering 的核心基础设施，而不是 QA 团队的外部附件。

## 核心结论

> **Eval 是可执行的 Capability Specification：Harness 说明怎么实现，Eval 说明怎么证明。**