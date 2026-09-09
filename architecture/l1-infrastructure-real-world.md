---
title: L1 基础设施 / 真实世界
aside: false
---

# L1 基础设施 / 真实世界

> **真实资源是动作最终落点，但不应该直接暴露成模型的无边界世界。**

<iframe class="architecture-frame" src="../diagrams/layers/l1-infrastructure-real-world.architecture.html?embed=1" title="L1 基础设施 / 真实世界架构图"></iframe>

<div class="architecture-links">
  <a href="../diagrams/layers/l1-infrastructure-real-world.architecture.html">打开独立交互图 ↗</a>
  <a href="./agent-platform#_4-agent-world-七层软件栈">回到七层软件栈 →</a>
</div>

## 图中要点

- **资源不等于能力**：API、MCP、SaaS、DB、Browser、Files、Compute 是底层连接与资源，不是 Agent-facing Capability 本身。
- **真实动作必须经过收缩**：Work Environment → Capability Proxy → Reachability / Data Flow Policy → Real-world Effects。
- **读写都属于安全边界**：权限、数据流、作用范围、持续时间和可达性共同决定最大 Blast Radius。
