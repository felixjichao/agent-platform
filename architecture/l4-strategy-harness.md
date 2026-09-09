---
title: L4 执行策略 / Harness
aside: false
---

# L4 执行策略 / Harness

> **Harness 管策略：当前任务准备怎么推进。Runtime 管事实：实际上发生了什么。**

<iframe class="architecture-frame" src="../diagrams/layers/l4-strategy-harness.architecture.html?embed=1" title="L4 执行策略 / Harness 架构图"></iframe>

<div class="architecture-links">
  <a href="../diagrams/layers/l4-strategy-harness.architecture.html">打开独立交互图 ↗</a>
  <a href="./agent-platform#_8-execution-strategy">阅读 Execution Strategy →</a>
</div>

## 图中要点

- **执行控制权是连续谱**：Static Workflow → Dynamic Plan → Agent Loop，而不是 Workflow / Agent 二选一。
- **执行范式可组合**：Direct、Workflow、Agent Loop、PTC、Multi-Agent 是策略，不是五套产品架构。
- **Harness 应可替换**：Planning、Delegation、Context、Evaluation、Completion 等策略随模型能力演进；Runtime 不应固化这些假设。
