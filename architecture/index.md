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

## 从业务到能力

<div class="diagram-grid">
  <a class="diagram-card" href="./l7-business-product">
    <span class="diagram-card__eyebrow">L7 · Business / Product</span>
    <strong>业务 / 产品</strong>
    <p>从业务目标到 Business Task；明确产品形态与执行范式不是一回事。</p>
  </a>
  <a class="diagram-card" href="./l6-capability-contract">
    <span class="diagram-card__eyebrow">L6 · Capability Contract</span>
    <strong>能力契约</strong>
    <p>Acceptance、Quality、Evaluation、Evidence 先定义“什么叫真正具备能力”。</p>
  </a>
  <a class="diagram-card" href="./l5-capability-engineering">
    <span class="diagram-card__eyebrow">L5 · Capability Engineering</span>
    <strong>能力工程</strong>
    <p>Capability Catalog、Discovery、Adapter、Tool、Skill 与运行时动态组装。</p>
  </a>
</div>

## 执行核心

<div class="diagram-grid">
  <a class="diagram-card" href="./l4-strategy-harness">
    <span class="diagram-card__eyebrow">L4 · Execution Control</span>
    <strong>执行策略 / Harness</strong>
    <p>Direct、Workflow、Agent Loop、PTC、Multi-Agent 如何动态选择；Harness 管策略。</p>
  </a>
  <a class="diagram-card" href="./l3-runtime">
    <span class="diagram-card__eyebrow">L3 · Execution Facts</span>
    <strong>统一 Runtime</strong>
    <p>Work、Session、Run、Event、State 如何组成持久、可恢复的执行事实。</p>
  </a>
  <a class="diagram-card" href="./l2-work-environment">
    <span class="diagram-card__eyebrow">L2 · Data + Action Plane</span>
    <strong>Agent Work Environment</strong>
    <p>Workspace、程序执行、能力代理、验证与隔离组成 Agent 可作用的工作世界。</p>
  </a>
</div>

## 真实世界与横切治理

<div class="diagram-grid diagram-grid--two">
  <a class="diagram-card" href="./l1-infrastructure-real-world">
    <span class="diagram-card__eyebrow">L1 · Infrastructure / Real World</span>
    <strong>基础设施 / 真实世界</strong>
    <p>API、SaaS、DB、Browser、Files、Compute 等真实资源如何通过受治理出口被 Agent 触达。</p>
  </a>
  <a class="diagram-card" href="./cross-cutting-governance">
    <span class="diagram-card__eyebrow">Cross-cutting Systems</span>
    <strong>Context · Eval · Observability · Security</strong>
    <p>上下文、评估、追踪、安全、版本和预算为什么不是独立层，而是贯穿执行系统。</p>
  </a>
</div>

## 阅读坐标

总体架构负责建立全局心智模型；七层图负责逐层放大职责边界；横切图负责解释贯穿所有层的治理系统。[规范性架构文档](./agent-platform)仍然是完整架构结论的事实入口。
