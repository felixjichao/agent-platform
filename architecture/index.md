---
title: Agent Platform 架构图谱
aside: false
---

# Agent Platform 架构图谱

架构图不是文档的装饰，而是当前架构结论的另一种可执行表达。图源统一使用 Archify Typed JSON IR，经过 `showcase` 校验后生成交互 HTML。

## 总体架构

<iframe class="architecture-frame architecture-frame--overview" src="../diagrams/core/agent-platform-overview.architecture.html?embed=1" title="Agent Platform 总体架构"></iframe>

<div class="architecture-links">
  <a href="../diagrams/core/agent-platform-overview.architecture.html">打开独立交互图 ↗</a>
  <a href="./agent-platform">阅读规范性架构文档 →</a>
</div>

## 三个关键执行层

<div class="diagram-grid">
  <a class="diagram-card" href="./l4-strategy-harness">
    <span class="diagram-card__eyebrow">L4 · Execution Control</span>
    <strong>执行策略 / Harness</strong>
    <p>Direct、Workflow、Agent Loop、PTC、Multi-Agent 如何被动态选择，以及 Harness 与 Runtime 的边界。</p>
  </a>
  <a class="diagram-card" href="./l3-runtime">
    <span class="diagram-card__eyebrow">L3 · Execution Facts</span>
    <strong>统一 Runtime</strong>
    <p>Work、Session、Run、Event、State 如何构成长期执行的稳定事实模型。</p>
  </a>
  <a class="diagram-card" href="./l2-work-environment">
    <span class="diagram-card__eyebrow">L2 · Data + Action Plane</span>
    <strong>Agent Work Environment</strong>
    <p>Workspace、程序执行、能力代理、验证与隔离如何组成 Agent 可作用的工作世界。</p>
  </a>
</div>

## 阅读坐标

总体架构负责建立全局心智模型；分层图负责放大关键边界；[规范性架构文档](./agent-platform)仍然是完整架构结论的事实入口。
