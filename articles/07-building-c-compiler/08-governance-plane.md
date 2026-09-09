# Human 从 Execution Path 移向 Governance Plane

## 文章中的关键观点

大规模 Agent Team 的价值之一，是人不需要逐步告诉每个 Agent 下一步做什么。但最终系统是否可以发布、部署、接受，仍然需要更高层的治理判断。

## 我们的架构分析

自动化程度提高后，人类角色从：

```text
Human
→ 指导每一步 Execution
```

逐渐转向：

```text
Human / Governance
→ 定义目标和边界
→ 设置 Acceptance / Risk
→ 处理 Escalation
→ 最终接受 / 发布
```

必须区分：

```text
VerificationPassed
≠ AcceptedForProduction
≠ Published / Deployed
```

前者可以由自动 Verifier 完成，后两者可能涉及业务责任、安全和治理。

## 对 Agent Platform 的影响

HITL 不应该只被理解成“每一步弹审批框”。更高级的 Human role 是 Governance Plane：定义规则、处理例外、接受结果和承担最终责任。

## 核心结论

> **随着自治增强，人类应逐渐退出 Execution Path，转向 Goal、Risk、Acceptance 和 Escalation 所在的 Governance Plane。**