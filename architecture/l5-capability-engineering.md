---
title: L5 能力工程
aside: false
---

# L5 能力工程

> **L5 负责把“系统能做什么”工程成稳定、可发现、可解析的能力语义；L4 选择能力，L3 把能力调用物化为可靠动作，L2 让执行尝试真实发生。**

<iframe class="architecture-frame" src="../diagrams/layers/l5-capability-engineering.architecture.html?embed=1" title="L5 能力工程架构图"></iframe>

<div class="architecture-links">
  <a href="../diagrams/layers/l5-capability-engineering.architecture.html">打开独立交互图 ↗</a>
  <a href="./agent-platform#_7-能力工程">阅读能力工程 →</a>
</div>

## L5 回答什么问题

L5 不回答“当前下一步做什么”，也不拥有动作生命周期。它回答三个稳定问题：

```text
能力定义
→ 系统到底能提供什么稳定工作能力？

能力发现
→ 当前决策点应该让执行框架看到哪些能力？

能力解析
→ 已选择的能力当前如何落到兼容、可用的实现？
```

因此：

```text
L4
→ 选择能力

L5
→ 定义 / 发现 / 解析能力

L3
→ 把能力调用意图物化为 Action，并管理可靠生命周期

L2
→ 让 Execution Attempt 真正发生
```

实现上可以把能力注册、工具定义、适配器和执行器放在同一个进程中，但语义归属不能由类名或服务名决定。

## Capability 是什么

能力不是 API 端点、工具名或完整业务任务。

> **Capability 是平台向执行策略暴露的、具有稳定语义边界、值得被独立选择和治理，并具有可描述输入、结果与副作用语义的工作能力。**

一个适合成为能力的语义边界通常满足：

1. 执行框架有理由独立选择它；
2. 平台有理由独立治理它；
3. 输入、结果和副作用语义可以被描述；
4. 多个具体实现可以在同一语义契约下互换。

例如：

```text
任务
→ 修复登录接口测试失败

能力
→ 搜索代码
→ 读取文件
→ 修改文件
→ 运行测试
```

而 `HTTP GET` 通常过低，`fix_issue` 通常又包含多轮策略决策而过高。

> **能力粒度应该尽量对齐“值得成为一次独立策略选择”的工作语义。**

## Task / Capability / Tool / Skill / API / Executor

这些概念回答不同问题：

| 概念 | 回答的问题 |
| --- | --- |
| 任务 | 要完成什么？ |
| 能力 | 系统能做什么？ |
| 工具 | 执行框架 / 模型如何表达一次能力调用？ |
| 技能 | 这类任务通常应该怎么做？ |
| API | 后端系统暴露什么技术接口？ |
| 执行器 | 这一次执行尝试具体怎样发生？ |

因此：

```text
Task ≠ Capability
Capability ≠ Tool
Tool Call ≠ Action
Capability Binding ≠ Executor
Skill ≠ Capability Grant
API ≠ Agent-facing Capability
```

## 三个核心责任

### 能力定义

能力定义建立稳定语义，不绑定某个当前实现。

例如：

```text
能力：
repository.search_code

语义：
在当前代码工作空间中查找匹配内容，并返回可定位的结果引用
```

今天可以由本地文本搜索实现，明天可以由代码索引或远程搜索服务实现。只要这些实现满足同一能力语义，L4 不应该因为实现替换而改变决策逻辑。

> **能力语义稳定，执行实现可替换。**

能力定义应能够描述或引用：

- 身份与修订版本；
- 适用语义；
- 输入与结果；
- 副作用类别；
- 幂等 / 重试相关性质；
- 权限和资源要求；
- 可逆性 / 风险提示；
- 工具接口；
- 相关技能、参考资料或辅助资源；
- 可兼容的能力绑定。

这些信息不要求全部复制在一个对象中，也不要求第一版建设复杂能力注册服务。

### 能力发现

能力数量较少时，可以把所有能力直接提供给执行框架；能力规模扩大后，必须把“能力空间”投影成当前决策点真正需要的能力集合：

```text
能力空间
   ↓
能力发现
   ↓
能力视图
   ↓
L4 决策上下文
```

能力视图只暴露决策相关语义，例如：

```text
能力引用
描述
输入契约
结果语义
副作用类别
成本 / 时延提示
风险 / 可逆性提示
当前可用性
```

它不应该暴露：

```text
MCP endpoint
API token
Worker id
Executor id
Pod name
Credential
内部路由配置
```

> **L4 消费能力语义，不消费能力执行基础设施。**

同时：

```text
Capability Visible
≠ Capability Authorized
```

能力视图是决策输入，不是执行授权事实。即使发现阶段已做预过滤，具体 Action 物化前仍需要结合身份、资源、风险和当前策略重新授权。

### 能力解析

当 L4 返回一个能力调用意图后，L5 负责把稳定能力语义映射到当前兼容、可用的实现：

```text
capability_ref
+ execution context
        ↓
能力解析
        ↓
能力绑定
```

能力解析可以考虑：

- 当前环境；
- 租户 / 区域；
- 数据位置；
- 可用性；
- 成本 / 时延；
- 语义兼容性；
- 当前资源和执行约束。

但能力解析不能静默改变能力语义。

如果“实现差异”已经影响策略决策，例如一个实现代表低成本快速搜索，另一个代表高质量深度研究，那么这些差异应该提升为不同能力语义或能力变体，而不是隐藏在绑定选择里。

## L4 → L5 → L3 的稳定调用链

推荐主链：

```text
能力视图
   ↓
L4 Harness / Model
   ↓
Tool Call / internal invocation
   ↓
Harness translate
   ↓
Execute(
  capability_ref,
  input
)
   ↓
L3 Runtime
   ↓ validate
L5 capability resolution
   ↓
Governance authorization
   ↓
Action materialization
   ↓
Execution Attempt
   ↓
L2 Executor
   ↓
Real World
```

因此：

> **L3 接收能力语义，不接收 MCP server、API endpoint 或工具实现细节。**

模型工具调用只是 L4 的调用表达。Harness 将其翻译成能力调用意图；L3 再把被接受的意图物化为 Action。

## Action 与能力绑定

Action 是 L3 的可靠执行意图。能力绑定是 L5 对该能力具体语义实现的解析结果。

推荐至少保留：

```text
Action
├── capability_ref
├── binding_ref
├── input
├── idempotency_key
└── runtime state

Execution Attempt
├── executor
├── execution_ref
├── timestamps
├── raw result ref
└── error / cost
```

因此：

> **Action 绑定逻辑实现；Execution Attempt 绑定物理执行。**

能力绑定更接近 Action 级语义，因为它会影响幂等性、结果核对、权限主体和副作用语义；执行器则回答某一次 Attempt 实际在哪里、通过什么机制执行。

默认重试同一个 Action 时，不应静默切换到另一个不兼容绑定。只有平台明确知道多个绑定在当前能力契约下语义兼容时，才能进行重新解析。

对于只读 / 纯操作可以更宽松；对于状态改变或非幂等能力应更严格，结果未知时仍必须先核对真实世界状态。

## 能力适配器

能力适配器负责把具体系统接口适配成平台能力要求的执行语义：

```text
Provider / API / MCP Tool
          ↓
     能力适配器
          ↓
   Capability Binding
```

它可以处理：

- 参数映射；
- 多个后端调用聚合；
- 错误归一化；
- 原始结果引用；
- 状态查询；
- 取消 / 结果核对所需机制；
- 结果结构化。

但：

```text
Adapter can reconcile
≠ Adapter owns reconciliation lifecycle

Adapter can cancel
≠ Adapter owns cancellation semantics
```

是否重试、什么时候核对、取消竞争如何处理、最终 Action Outcome 如何提交，仍属于 L3。

## Tool 是能力调用接口，不是能力本身

工具主要解决：

> **执行框架 / 模型如何理解并表达一次能力调用？**

例如：

```text
Capability
repository.search_code

Tool Interface
search_code(query, path?)
```

一个能力可以有多个调用接口，一个工具也可能错误地把多个不同风险语义揉在一起。平台不需要强制“一 Tool 一 Capability”，但工具设计应尽量对齐能力的策略选择和治理边界。

默认应该让工具绑定稳定能力语义，而不是直接绑定具体实现。

执行框架应该看到：

```text
search_code
```

而不是：

```text
search_code_via_rg
search_code_via_remote_index
search_code_via_mcp_server_x
```

除非这些实现差异本身需要成为策略决策。

## Skill 是程序性知识包，不是执行权限

技能是：

> **可发现、可按需加载的程序性知识包，用于指导执行框架在特定任务或领域中如何组织决策、使用能力和处理结果。**

典型结构：

```text
技能元数据
    ↓
SKILL.md
    ↓
参考资料 / 脚本 / 静态资源
```

技能主要改变：

```text
怎么思考
怎么组合能力
什么时候使用某项能力
如何检查结果
```

而不会自动增加：

```text
执行权限
新的 Action lifecycle
新的 Resource Reachability
新的 Capability Grant
```

因此：

> **Skill availability ≠ Authority grant。**

技能中的 `allowed-tools`、工具建议或执行步骤最多表示策略提示 / 请求范围，不能替代安全与治理授权。

### Skill 中的脚本

Skill 可以携带脚本。脚本是否需要跨 Runtime Boundary，仍按实际行为判断：

```text
纯内部计算 / 转换
→ 可以作为 Harness 内部机制

产生受治理工作世界效果
需要可靠执行 / 恢复 / 取消 / 审计
→ 必须转化成 Capability Invocation
→ L3 Action
→ L2 Executor
```

不能因为代码文件位于 Skill 包内，就允许它绕过 Runtime 修改真实世界。

## Skill Discovery ≠ Capability Discovery

二者都可能使用“先元数据、后详细内容”的渐进加载方式，但回答的问题不同：

```text
技能发现
→ 当前任务有哪些方法知识值得加载？

能力发现
→ 当前决策点有哪些执行能力可以选择？
```

前者属于策略知识选择，后者属于可执行能力空间投影。

## MCP / API / SDK 的位置

> **MCP 是连接标准，API / SDK 是系统接口；它们都不是能力设计标准。**

推荐理解为：

```text
Capability
     ↓
Capability Binding
     ↓
Adapter
     ↓
MCP / API / SDK / local implementation
```

MCP Tool 可以被适配为某个能力绑定，但平台仍需要判断它到底提供什么稳定能力语义。

因此不要把：

```text
MCP Tool List
API Endpoint List
```

直接当成能力目录。

## 动态 Tool Search

当工具数量很大时，动态 Tool Search 本质上是能力发现的一种实现：

```text
大量工具 / 能力资产
      ↓
索引 / 搜索 / 过滤
      ↓
当前 Capability View
      ↓
少量 Tool Interfaces
      ↓
L4
```

索引、向量检索、关键词检索、分类体系、注册表服务都是实现机制；L5 Core 只要求当前决策点能够获得正确的能力视图。

## PTC / Code Execution

PTC 决定“当前策略是逐个调用能力，还是生成程序批量编排能力”，属于 L4。

L5 提供程序可调用的稳定能力语义和绑定；真正代码执行仍然进入：

```text
L3 Action
→ Execution Attempt
→ L2 Executor
```

如果生成代码只是 Harness 内部的纯计算，则无需创建 Action；如果代码会产生受治理外部效果，就不能因为它是“生成程序”而绕过能力和 Runtime 边界。

## Agent 作为能力实现

专用 Agent 也可以成为某个能力的实现，但仍按行为判断：

```text
只是当前 Harness 内部 specialist / policy computation
→ L4 internal

以稳定能力语义被调用，但没有独立可靠生命周期
→ 可以作为 L5 某个 binding 的内部实现

需要独立等待 / 恢复 / 取消 / 完成
→ L3 Child Run
```

“Agent-as-Tool”或“Agent-as-Capability”只是调用表面，不能自动决定领域模型。

## 能力工程资产

Capability 是稳定工作能力；实现它可以依赖多种工程资产：

```text
Capability
├── Tool Interface
├── Skill
├── Capability Adapter
├── Script
├── Reference / Prompt
└── MCP / API / SDK Binding
```

这不表示 `Capability = Tool + Skill`，而表示能力可以由多种工程资产共同实现和增强。

第一版不需要建设 Capability Dependency Graph、Marketplace 或独立 Resolver Service。单体实现完全可以把 definition、tool schema、handler 和 binding 放在同一个 Python / Go 对象里，只要语义边界不混淆。

## 与 L6 能力契约的边界

L5 回答：

> **这个能力是什么、怎样被发现、怎样落到当前实现。**

L6 回答：

> **什么叫真正具备这项能力，以及怎样证明。**

因此：

```text
Capability Definition
≠ Capability Contract
```

L5 可以提供风险、副作用、输入输出和实现语义；质量标准、验收标准、评估契约和能力证据属于 L6。

## 核心不变量

1. **Capability 是稳定工作语义，不等于 Task、Tool、API、MCP Tool 或 Executor。**
2. **L5 的核心责任是 Definition / Discovery / Resolution，而不是拥有动作生命周期。**
3. **能力粒度应对齐值得被独立策略选择和治理的工作语义。**
4. **L4 看到 Capability View，不看到绑定拓扑和执行基础设施。**
5. **Capability Visible ≠ Capability Authorized。**
6. **L3 接收能力调用意图并物化 Action；Tool Call 本身不是 Action。**
7. **Action 保留 capability / binding 来源；Execution Attempt 保留具体 executor / execution reference。**
8. **Binding 变化不是普通 Retry；只有明确语义兼容时才允许重新解析。**
9. **Adapter 提供执行、查询、取消、核对等机制，但不拥有 L3 可靠执行生命周期。**
10. **Tool 是能力调用接口；Skill 是程序性知识包；MCP / API / SDK 是连接和实现机制。**
11. **Skill availability ≠ Capability Grant。**
12. **Skill 脚本是否进入 Action，由实际可靠执行和治理语义决定。**
13. **Skill Discovery 与 Capability Discovery 解决不同问题。**
14. **专用 Agent 是否形成 Child Run 取决于真实生命周期，而不是调用名称。**
15. **逻辑语义边界不要求物理拆成 Capability Service / Registry / Resolver 等独立服务。**
