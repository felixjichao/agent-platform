---
title: 横切系统与治理
aside: false
---

# 横切系统与治理

> **上下文、评估、可观测性和安全治理不是独立的一层，而是贯穿能力定义、执行、验证与真实动作。**

<iframe class="architecture-frame" src="../diagrams/layers/cross-cutting-governance.architecture.html?embed=1" title="Agent Platform 横切系统架构图"></iframe>

<div class="architecture-links">
  <a href="../diagrams/layers/cross-cutting-governance.architecture.html">打开独立交互图 ↗</a>
  <a href="./agent-platform#_11-横切系统">阅读横切系统 →</a>
</div>

## 图中要点

- **上下文 / 记忆**决定模型当前看到什么，但不会改变底层执行事实。
- **评估 / 验证**定义如何证明能力和结果，而不是只做离线打分。
- **可观测性 / 追踪**让事件、因果链、重试、委派和资源消耗可见。
- **安全 / 治理**约束身份、权限、信任、可达范围与数据流；注册表 / 版本管理和预算 / 成本贯穿整个生命周期。
