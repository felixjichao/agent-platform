---
title: L4 执行策略 / 执行框架
aside: false
---

# L4 执行策略 / 执行框架

> **执行框架（Harness）管策略：当前任务准备怎么推进。运行时管事实：实际上发生了什么。**

<iframe class="architecture-frame" src="../diagrams/layers/l4-strategy-harness.architecture.html?embed=1" title="L4 执行策略 / 执行框架架构图"></iframe>

<div class="architecture-links">
  <a href="../diagrams/layers/l4-strategy-harness.architecture.html">打开独立交互图 ↗</a>
  <a href="./agent-platform#_8-execution-strategy">阅读执行策略 →</a>
</div>

## 图中要点

- **执行控制权是一条连续谱**：静态工作流 → 动态计划 → 智能体循环，而不是工作流与智能体二选一。
- **执行范式可以组合**：直接执行、工作流、智能体循环、PTC、多智能体都是策略，不是五套产品架构。
- **执行框架应可替换**：规划、委派、上下文、评估、完成等策略会随模型能力演进；运行时不应固化这些假设。
