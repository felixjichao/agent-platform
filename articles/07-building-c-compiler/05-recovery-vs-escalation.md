# Recovery 与 Escalation 必须分开

## 文章中的关键观点

Agent 团队可以通过重试、换任务、其他 Agent 接手等方式处理大量失败，但有些问题不是“多试几次”能够解决，例如模型能力上限、关键工具缺失或外部系统限制。

## 我们的架构分析

### Recovery

针对可恢复故障：

- Harness crash；
- 临时 Tool failure；
- Worker restart；
- 可重试的局部任务失败。

目标是恢复到继续执行的状态。

### Escalation

针对当前能力边界无法解决的问题：

- 需要更强模型；
- 需要专家 Agent；
- 需要人工决策；
- 需要新 Capability；
- 需要缩小 Scope。

如果把 Capability Ceiling 当成 Recovery 问题，会出现无意义的无限重试。

## 对 Agent Platform 的影响

Harness Completion Strategy 中需要显式包含 Escalation。平台则需要支持把阻塞原因、证据、已尝试方案和所需能力向上交接。

## 核心结论

> **Recovery 解决暂时失败，Escalation 解决能力边界；二者不能用同一套 retry 机制代替。**