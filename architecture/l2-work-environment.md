---
title: L2 Agent Work Environment
aside: false
---

# L2 Agent Work Environment

> **LLM / Harness 更适合作为控制面；数据处理、程序执行和真实动作应该进入受治理的 Work Environment。**

<iframe class="architecture-frame" src="../diagrams/layers/l2-work-environment.architecture.html?embed=1" title="L2 Agent Work Environment 架构图"></iframe>

<div class="architecture-links">
  <a href="../diagrams/layers/l2-work-environment.architecture.html">打开独立交互图 ↗</a>
  <a href="./agent-platform#_10-agent-work-environment">阅读 Work Environment →</a>
</div>

## 图中要点

- **Context 不是世界本身**：Workspace 承载文件、代码、数据、检查点和进度等外部持久工作状态。
- **数据 / 动作面下沉**：循环、过滤、聚合、代码执行和 Tool 编排尽量在环境中完成。
- **执行必须受治理**：Capability Proxy、Sandbox、Verification、Telemetry 共同限制 Agent 的真实可达范围。
