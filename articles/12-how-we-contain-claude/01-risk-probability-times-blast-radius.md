# Risk = Failure Probability × Blast Radius

## 文章中的关键观点

随着 Agent 能力和权限扩大，即使模型本身更加可靠，一次失败能够造成的最大影响也可能同步扩大。因此安全不能只关注“模型犯错概率”。

## 我们的架构分析

可以用一个简单心智模型理解部署风险：

```text
Deployment Risk
≈ Failure Probability × Blast Radius
```

模型训练、System Prompt、Classifier、Human Approval 等主要尝试降低 Failure Probability。

Sandbox、Filesystem Boundary、Network Boundary、Credential Isolation 等主要限制 Blast Radius。

二者性质不同：

```text
Probabilistic Defense
→ 让坏事更不容易发生

Deterministic Boundary
→ 即使坏事发生，也不能越过边界
```

因此成熟安全系统必须假设概率防御最终可能漏掉，并由确定性 Containment 承接最后后果。

## 对 Agent Platform 的影响

Execution Environment 的第一安全职责不再只是“能运行 Tool”，而是建立确定性的 Blast Radius Boundary。

## 核心结论

> **Soft controls reduce likelihood; hard containment limits maximum consequence。**

> **Agent 安全的最后边界不能建立在“模型永远做对”这一假设上。**