# 三类风险来源与纵深防御

## 文章中的关键观点

文章把风险来源分成三类：

1. User Misuse：用户恶意、粗心或被误导；
2. Model Misbehavior：没人要求，但模型为了完成目标主动走向危险路径；
3. External Attack：网页、文件、Tool Output、Prompt Injection 等外部攻击。

对应防御也不能只靠一个机制，而要同时覆盖 Environment、Model 和 External Content。

## 我们的架构分析

三类来源说明“用户是可信最高优先级输入”并不足够，“模型足够可靠”也不足够，“Tool 本身经过审核”仍不足够。

可以形成三层 Defense in Depth：

```text
Behavior / Model Defense
├── System Policy
├── Safety Training
├── Classifier
└── HITL / Approval

Content Defense
├── Provenance
├── Prompt Injection Detection
├── Tool Output Inspection
└── Trust Classification

Environment Defense
├── Isolation
├── Filesystem Boundary
├── Network Boundary
├── Credential Boundary
└── Resource Boundary
```

模型与内容层是概率防御，环境层应尽可能提供确定性硬边界。

## 对 Agent Platform 的影响

Security / Governance 不应只等价为 Tool Permission。平台需要独立的 Behavioral Security、Content Security 和 Environment Security。

## 核心结论

> **Agent Threat Model 必须同时考虑用户、模型和外部世界；任何单层防御都不够。**