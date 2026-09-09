# 从离线 Eval 到整体质量系统

## 文章中的关键观点

离线 Eval 很重要，但无法覆盖 Production 中所有真实分布、用户行为和长期失败模式。可靠 Agent 需要多种质量信号共同工作。

## 我们的架构分析

完整质量系统可以包括：

```text
Offline Eval
Production Monitoring
A/B Experiment
User Feedback
Transcript Review
Human Evaluation
Incident / Failure Mining
```

不同信号回答不同问题：

- 离线 Eval：上线前能否发现回归；
- Production Monitoring：真实分布下发生了什么；
- A/B：新版本是否真正改善用户结果；
- User Feedback：哪些成功标准在实验室没有覆盖；
- Transcript Review：为什么出现失败。

同时指标最好分为：

- Quality；
- Reliability；
- Efficiency；

而不是压成一个无法解释的总分。

## 对 Agent Platform 的影响

Eval Platform 和 Observability Platform 需要共享 Trial / Run / Trace / Outcome 语义，Production failure 还能反向进入 Capability Eval 或 Regression Suite。

## 核心结论

> **Agent Quality 不是一个 Eval Score，而是离线评估、线上观测、用户反馈和人工判断组成的闭环。**