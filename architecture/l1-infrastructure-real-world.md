---
title: L1 基础设施 / 真实世界
aside: false
---

# L1 基础设施 / 真实世界

> **真实资源是动作最终落点，但不应该直接暴露成智能体的无边界世界。**

<iframe class="architecture-frame" src="../diagrams/layers/l1-infrastructure-real-world.architecture.html?embed=1" title="L1 基础设施 / 真实世界架构图"></iframe>

<div class="architecture-links">
  <a href="../diagrams/layers/l1-infrastructure-real-world.architecture.html">打开独立交互图 ↗</a>
  <a href="./agent-platform#_4-agent-world-七层软件栈">回到七层软件栈 →</a>
</div>

## 图中要点

- **资源不等于能力**：API、MCP、SaaS、数据库、浏览器、文件、计算资源是底层连接与资源，不等于面向智能体的能力。
- **真实动作必须经过收缩**：智能体工作环境 → 能力代理 → 可达范围 / 数据流策略 → 真实世界副作用。
- **读写都属于安全边界**：权限、数据流、作用范围、持续时间和可达范围共同决定系统的最大影响范围。
