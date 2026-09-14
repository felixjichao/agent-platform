---
title: 横切系统与治理
aside: false
---

# 横切系统与治理

> **上下文、评估、可观测性、安全治理和人工监督不是独立的一层，而是贯穿能力定义、执行、验证与真实动作。**

<iframe class="architecture-frame" src="../diagrams/layers/cross-cutting-governance.architecture.html?embed=1" title="Agent Platform 横切系统架构图"></iframe>

<div class="architecture-links">
  <a href="../diagrams/layers/cross-cutting-governance.architecture.html">打开独立交互图 ↗</a>
  <a href="./agent-platform#_14-安全与治理">阅读安全与治理 →</a>
</div>

## 图中要点

- **上下文 / 记忆**决定模型当前看到什么，但不会改变底层执行事实。
- **评估 / 验证**定义如何证明能力和结果；上线前评估与部署后监控共同形成生产反馈闭环。
- **可观测性 / 追踪**让事件、因果链、控制权转移、重试、委派和资源消耗可见，也是自主性测量的事实基础。
- **安全 / 治理**约束身份、权限、信任、可达范围、数据流和自主空间；自主性应随风险、可逆性与验证能力动态分配。
- **人工监督**关注人能否看清执行状态，并在需要时中断、纠偏、评审、升级或验收，而不是是否对每个动作弹出审批框。
- **注册表 / 版本管理和预算 / 成本**贯穿整个能力与执行生命周期。
