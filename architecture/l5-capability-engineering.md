---
title: L5 能力工程
aside: false
---

# L5 能力工程

> **Agent 使用能力，但不拥有能力。能力应该独立资产化、可发现、可组合、可版本化。**

<iframe class="architecture-frame" src="../diagrams/layers/l5-capability-engineering.architecture.html?embed=1" title="L5 能力工程架构图"></iframe>

<div class="architecture-links">
  <a href="../diagrams/layers/l5-capability-engineering.architecture.html">打开独立交互图 ↗</a>
  <a href="./agent-platform#_7-能力工程">阅读能力工程 →</a>
</div>

## 图中要点

- **Discovery ≠ Loading**：先发现能力 Metadata，再按任务选择并加载真正需要的 Skill / Tool。
- **Tool 需要语义适配**：Backend API / MCP Tool → Capability Adapter → Agent-facing Tool。
- **Skill 是程序性知识**：Skill Metadata → SKILL.md → References / Scripts / Resources 渐进披露。
