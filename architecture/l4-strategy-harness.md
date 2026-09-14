---
title: L4 执行策略 / 执行框架
aside: false
---

# L4 执行策略 / 执行框架

> **执行框架（Harness）管策略：当前任务准备怎么推进。运行时管事实：实际上发生了什么。**

<iframe class="architecture-frame" src="../diagrams/layers/l4-strategy-harness.architecture.html?embed=1" title="L4 执行策略 / 执行框架架构图"></iframe>

<div class="architecture-links">
  <a href="../diagrams/layers/l4-strategy-harness.architecture.html">打开独立交互图 ↗</a>
  <a href="./agent-platform#_8-执行策略">阅读执行策略 →</a>
</div>

## 图中要点

- **执行控制权是一条连续谱**：静态工作流 → 动态计划 → 智能体循环，而不是工作流与智能体二选一。
- **执行范式与自主性是两个维度**：直接执行、工作流、智能体循环、PTC、多智能体决定任务怎么推进；自主策略决定在当前风险和权限边界内，智能体可以自己决定多少。
- **控制权可以动态转移**：执行框架根据不确定性、信息缺失、能力缺口和风险边界决定继续自治还是升级给人或更高层机制。
- **执行框架应可替换**：规划、委派、上下文、评估、自主、完成和升级等策略会随模型能力演进；运行时不应固化这些假设。
