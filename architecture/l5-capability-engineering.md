---
title: L5 能力工程
aside: false
---

# L5 能力工程

> **智能体使用能力，但不拥有能力。能力应该独立资产化、可发现、可组合、可版本化。**

<iframe class="architecture-frame" src="../diagrams/layers/l5-capability-engineering.architecture.html?embed=1" title="L5 能力工程架构图"></iframe>

<div class="architecture-links">
  <a href="../diagrams/layers/l5-capability-engineering.architecture.html">打开独立交互图 ↗</a>
  <a href="./agent-platform#_7-能力工程">阅读能力工程 →</a>
</div>

## 图中要点

- **能力发现与加载分离**：先发现能力元数据，再按任务选择并加载真正需要的技能和工具。
- **工具需要语义适配**：后端 API / MCP 工具 → 能力适配器 → 面向智能体的工具。
- **技能是程序性知识**：技能元数据 → `SKILL.md` → 参考资料 / 脚本 / 资源，按需逐步展开。
