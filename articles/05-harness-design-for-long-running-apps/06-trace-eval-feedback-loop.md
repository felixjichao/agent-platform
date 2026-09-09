# Trace + Eval 形成 Harness Engineering 闭环

## 文章中的关键观点

文章对不同 Harness 版本进行系统实验，通过结果比较判断哪些结构真正有效。

## 我们的架构分析

如果只看最终成功率，很难知道 Harness 为什么变好或变差。需要结合 Trace：

```text
Harness Revision
      ↓
     Trial
      ↓
Trace + Outcome
      ↓
     Eval
      ↓
Failure Analysis
      ↓
Harness Revision
```

Trace 负责回答“发生了什么、策略在哪一步失效”，Eval 负责回答“结果是否达到目标”。

因此 Harness Engineering 不是一次 Prompt 编写，而是一个持续实验和版本演进过程。

## 对 Agent Platform 的影响

平台需要为 Harness Revision、Trace、Outcome 和 Eval 建立关联。Harness 发布应独立于 Session，已有长任务不应该因为新 Harness 版本发布而被隐式迁移。

## 核心结论

> **Trace + Eval 是 Harness Engineering 的核心反馈闭环；Harness 的复杂度必须由可测结果证明。**