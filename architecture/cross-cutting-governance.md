---
title: 横切系统与治理
aside: false
---

# 横切系统与治理

> **Context、Eval、Observability、Security 不是独立的一层，而是贯穿能力定义、执行、验证与真实动作。**

<iframe class="architecture-frame" src="../diagrams/layers/cross-cutting-governance.architecture.html?embed=1" title="Agent Platform 横切系统架构图"></iframe>

<div class="architecture-links">
  <a href="../diagrams/layers/cross-cutting-governance.architecture.html">打开独立交互图 ↗</a>
  <a href="./agent-platform#_11-横切系统">阅读横切系统 →</a>
</div>

## 图中要点

- **Context / Memory** 决定模型当前看到什么，但不会改变底层执行事实。
- **Evaluation / Verification** 定义如何证明能力和结果，而不是只做离线打分。
- **Observability / Trace** 让 Event、因果链、重试、委托和资源消耗可见。
- **Security / Governance** 约束 Identity、Authority、Trust、Reachability 与 Data Flow；Registry / Versioning 和 Budget / Cost 贯穿整个生命周期。
