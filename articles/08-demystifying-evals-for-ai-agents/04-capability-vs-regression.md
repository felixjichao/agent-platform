# Capability Eval 与 Regression Eval

## 文章中的关键观点

文章区分了探索系统“能否做到”的能力评估，以及持续确保已具备能力“不再退化”的回归评估。

## 我们的架构分析

### Capability Eval

用于回答：

> 新模型 / 新 Harness / 新 Tool 是否打开了以前做不到的能力？

任务可以较难，允许 pass@k 较低，用于探索能力边界和失败模式。

### Regression Eval

用于回答：

> 已经证明能做的事情，这次版本升级有没有退化？

要求更稳定，通常使用固定任务集、更严格阈值和持续 CI。

一个成熟流程是：

```text
Capability Task
   ↓ 证明能力
Graduation
   ↓
Regression Suite
```

也就是能力测试成功后，应把代表性任务晋升为长期回归资产。

## 对 Agent Platform 的影响

Eval Suite 需要生命周期，不是一个静态题库。平台应支持 Task 标签、套件版本、毕业 / 淘汰和不同统计阈值。

## 核心结论

> **Capability Eval 用来寻找能力边界，Regression Eval 用来守住已经获得的能力。**