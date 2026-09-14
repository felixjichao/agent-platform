---
title: L2 智能体工作环境
aside: false
---

# L2 智能体工作环境

> **LLM / 执行框架更适合作为控制面；数据处理、程序执行和真实动作应该进入受治理的智能体工作环境。**

<iframe class="architecture-frame" src="../diagrams/layers/l2-work-environment.architecture.html?embed=1" title="L2 智能体工作环境架构图"></iframe>

<div class="architecture-links">
  <a href="../diagrams/layers/l2-work-environment.architecture.html">打开独立交互图 ↗</a>
  <a href="./agent-platform#_10-agent-work-environment">阅读智能体工作环境 →</a>
</div>

## 图中要点

- **上下文不是世界本身**：工作空间承载文件、代码、数据、检查点和进度等外部持久工作状态。
- **数据面与动作面下沉**：循环、过滤、聚合、代码执行和工具编排尽量在环境中完成。
- **执行必须受治理**：能力代理、沙箱、验证与遥测共同限制智能体的真实可达范围。
