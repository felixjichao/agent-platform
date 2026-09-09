---
title: L3 统一 Runtime
aside: false
---

# L3 统一 Runtime

> **Runtime 的核心职责不是替 Agent 做计划，而是把真实执行变成持久、可恢复、可重建的事实。**

<iframe class="architecture-frame" src="../diagrams/layers/l3-runtime.architecture.html?embed=1" title="L3 统一 Runtime 架构图"></iframe>

<div class="architecture-links">
  <a href="../diagrams/layers/l3-runtime.architecture.html">打开独立交互图 ↗</a>
  <a href="./agent-platform#_5-核心领域模型">阅读核心领域模型 →</a>
</div>

## 图中要点

- **三个时间尺度**：Work 承载长期目标，Session 表示 Agent 与 Work 的相对连续关系，Run 表示一次连续执行片段。
- **事实与投影分离**：Event / Result 是事实；State / Observation 是从事实构建出的视图。
- **长期连续性属于 Work**：Agent 可以忘记、退出或替换；Event、Artifact、Workspace 与 Recovery 让工作继续。
