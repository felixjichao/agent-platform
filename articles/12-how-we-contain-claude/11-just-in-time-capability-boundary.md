# Just-in-Time Capability Boundary

## 我们的架构分析

Containment 不应是 Agent 创建时永久配置的一组大权限，而应围绕当前 Work 和执行阶段动态收缩可达世界。

传统：

```text
Agent A
→ GitHub Write
→ Slack Write
→ DB Read
→ Browser
→ Shell
```

更合理：

```text
Current Work / Stage
      ↓
Capability Need
      ↓
Policy Decision
      ↓
Temporary Scoped Grant
      ↓
Execution
      ↓
Revoke / Narrow
```

Least Privilege 在 Agent 时代需要加入：

```text
Least Privilege
× Least Duration
× Least Scope
```

同一个 Work 不同阶段还可以使用不同 Containment Profile：Analyze、Modify、Review、Merge、Deploy 的风险完全不同。

Multi-Agent 下尤其不能默认 Parent 权限完整继承给 Child：

```text
Delegate Goal
      ↓
derive minimum capability set
      ↓
Child Capability Grant
```

> **Delegation 传递 Goal，不默认传递 Authority。**

## 对 Agent Platform 的影响

Team Formation 和 Security Boundary Formation 应同步进行。每个 Child、每个 Run / Stage 都可以有自己的短生命周期 Capability Grant。

## 核心结论

> **Containment 的核心是持续压缩 Agent Reachability，使当前可达世界不超过完成 Work 所需最小范围。**