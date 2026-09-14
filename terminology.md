# Agent Platform 术语表

本文档定义 Agent Platform 文档与架构图中的统一术语。目标不是消灭英文，而是让中文承担主要叙述职责，英文只用于首次消歧、标准名称、协议名称和工程标识。

## 1. 使用规则

### 1.1 中文优先

存在稳定、准确的中文表达时，正文和架构图直接使用中文。

例如：

- 上下文，而不是反复写 `Context`
- 记忆，而不是反复写 `Memory`
- 评估，而不是反复写 `Evaluation`
- 验证，而不是反复写 `Verification`
- 运行时，而不是反复写 `Runtime`

### 1.2 核心概念首次中英对照

对容易与工程实现建立对应关系的核心概念，首次出现时采用“中文（English）”，后续优先使用中文。

例如：

- 运行时（Runtime）
- 执行框架（Harness）
- 工作环境（Work Environment）
- 工作（Work）
- 会话（Session）
- 运行（Run）

### 1.3 工程标识保留英文

以下内容不强制翻译：

- 协议和行业缩写：`LLM`、`MCP`、`API`、`SaaS`、`PTC`、`HITL`
- 代码类型名、接口名、事件类型、字段名、配置项
- 目录名、文件名、命令、包名
- JSON / Schema 中的 `id`、`type`、`from`、`to` 等内部标识

### 1.4 领域模型“中文叙述，英文对码”

`Work / Session / Run / Event / Action / Result / Observation / Artifact` 等属于正式领域模型实体：

- 正文：首次使用“中文（English）”，后续可直接使用中文。
- 架构图：面向读者的展示文本优先中文；必要时保留英文原词用于对应代码模型。
- Schema、事件名、代码类型：保持英文，不翻译标识符。

### 1.5 禁止同义漂移

同一概念只使用本术语表规定的一种中文表达。需要调整翻译时，先修改本术语表，再同步正文和架构图。

## 2. 平台与分层术语

| English | 推荐中文 | 使用说明 |
| --- | --- | --- |
| Agent Platform | 智能体平台 | 项目名 `Agent Platform` 可保留；正文概念优先“智能体平台” |
| Agent | 智能体 | 产品名、代码实体可保留 `Agent` |
| Agent Software Stack | 智能体软件栈 | 标题和正文优先中文 |
| Runtime | 运行时 | 首次可写“运行时（Runtime）” |
| Harness | 执行框架 | 首次写“执行框架（Harness）”；不译为“线束” |
| Work Environment | 工作环境 | 完整名称可写“智能体工作环境（Agent Work Environment）” |
| Infrastructure | 基础设施 | 直接使用中文 |
| Real World | 真实世界 | 指平台之外实际资源与系统 |
| Cross-cutting System | 横切系统 | 直接使用中文 |

## 3. 业务与能力术语

| English | 推荐中文 | 使用说明 |
| --- | --- | --- |
| Goal | 目标 | 直接使用中文 |
| Project | 项目 | 直接使用中文 |
| Business Task | 业务任务 | 直接使用中文 |
| Requirement | 需求 | 直接使用中文 |
| Capability | 能力 | 直接使用中文 |
| Capability Contract | 能力契约 | 直接使用中文 |
| Capability Definition | 能力定义 | 直接使用中文 |
| Acceptance Criteria | 验收标准 | 不使用“接受标准” |
| Quality Criteria | 质量标准 | 直接使用中文 |
| Evaluation Contract | 评估契约 | 表示如何证明能力成立 |
| Evidence Requirement | 证据要求 | 直接使用中文 |
| Capability Engineering | 能力工程 | 直接使用中文 |
| Capability Catalog | 能力目录 | 不使用“能力目录册” |
| Taxonomy | 分类体系 | 在能力语境中使用“能力分类体系” |
| Discovery | 发现 | 在能力语境中使用“能力发现” |
| Capability Adapter | 能力适配器 | 直接使用中文 |
| Capability Proxy | 能力代理 | 指工作环境中的受治理代理层 |
| Skill | 技能 | 首次可写“技能（Skill）” |
| Tool | 工具 | 首次可写“工具（Tool）” |
| Binding | 绑定 | 如“MCP 绑定” |

## 4. 执行策略术语

| English | 推荐中文 | 使用说明 |
| --- | --- | --- |
| Direct | 直接执行 | 表示无需复杂编排的执行策略 |
| Workflow | 工作流 | 保留行业惯用译法 |
| Dynamic Workflow | 动态工作流 | 直接使用中文 |
| Agent Loop | 智能体循环 | 首次可保留 `Agent Loop` |
| Multi-Agent | 多智能体 | 直接使用中文 |
| Planning | 规划 | 不统一使用“计划”表示机制本身 |
| Plan | 计划 | 指一次具体计划产物 |
| Delegation | 委派 | 直接使用中文 |
| Context Strategy | 上下文策略 | 直接使用中文 |
| Evaluation Strategy | 评估策略 | 直接使用中文 |
| Completion Strategy | 完成策略 | 直接使用中文 |
| Escalation Strategy | 升级策略 | 指升级到其他 Agent、人或流程 |

## 5. 运行时领域模型

| English | 推荐中文 | 使用说明 |
| --- | --- | --- |
| Work | 工作 | 正式领域实体，首次“工作（Work）” |
| Session | 会话 | 正式领域实体，首次“会话（Session）” |
| Run | 运行 | 正式领域实体，首次“运行（Run）” |
| Event | 事件 | 正式领域实体，首次“事件（Event）” |
| State | 状态 | 直接使用中文 |
| Command | 命令 | 直接使用中文 |
| Action | 动作 | 正式领域实体，首次“动作（Action）” |
| Result | 结果 | 正式领域实体，首次“结果（Result）” |
| Observation | 观察 | 正式领域实体，首次“观察（Observation）” |
| Artifact | 制品 | 指正式工作产物；避免与普通“结果”混用 |
| Trigger | 触发器 | 直接使用中文 |
| Recovery | 恢复 | 直接使用中文 |
| Handoff | 交接 | 直接使用中文 |
| Event Log | 事件日志 | 直接使用中文 |
| Snapshot | 快照 | 直接使用中文 |
| Event Envelope | 事件信封 | 仅在描述事件公共封装结构时使用 |
| Source of Truth | 事实源 | 优先中文，不使用“真相源” |

## 6. 上下文、记忆与工作空间

| English | 推荐中文 | 使用说明 |
| --- | --- | --- |
| Context | 上下文 | 首次可写“上下文（Context）” |
| Context Builder | 上下文构建器 | 直接使用中文 |
| Memory | 记忆 | 首次可写“记忆（Memory）” |
| Working Memory | 工作记忆 | 直接使用中文 |
| Episodic Memory | 情景记忆 | 直接使用中文 |
| Semantic Memory | 语义记忆 | 直接使用中文 |
| Workspace | 工作空间 | 首次可写“工作空间（Workspace）” |
| Working Set | 工作集 | 指当前模型实际装载内容 |
| Projection | 投影 | 直接使用中文 |
| Context Projection | 上下文投影 | 直接使用中文 |
| Observation Projection | 观察投影 | 直接使用中文 |
| Compaction | 压缩 | 指上下文压缩机制 |
| Recall | 召回 | 指记忆召回 |
| Promotion | 晋升 | 指候选记忆晋升为长期记忆 |
| Checkpoint | 检查点 | 直接使用中文 |
| Note | 笔记 | 指智能体当前主观认知 |
| Todo | 待办 | 直接使用中文 |

## 7. 验证、治理与可观测术语

| English | 推荐中文 | 使用说明 |
| --- | --- | --- |
| Evaluation / Eval | 评估 | `Eval` 仅在行业简称或代码名中保留 |
| Verification | 验证 | 与“评估”区分：验证执行结果是否满足明确条件 |
| Acceptance | 验收 | 与“验证”区分：业务是否接受结果 |
| Grader | 评分器 | 直接使用中文 |
| Evidence | 证据 | 直接使用中文 |
| Oracle | 判定器 | 指提供确定判断依据的机制 |
| Observability | 可观测性 | 直接使用中文 |
| Trace | 追踪 | 不统一使用“链路”替代概念本身 |
| Metric | 指标 | 直接使用中文 |
| Replay | 重放 | 直接使用中文 |
| Security | 安全 | 直接使用中文 |
| Governance | 治理 | 直接使用中文 |
| Identity | 身份 | 直接使用中文 |
| Authority | 权限 | 在授权语境中优先“权限” |
| Isolation | 隔离 | 直接使用中文 |
| Reachability | 可达范围 | 指 Agent 能触达的资源边界 |
| Registry | 注册表 | 指能力、版本等注册信息集合 |
| Versioning | 版本管理 | 直接使用中文 |
| Revision | 修订版本 | 指 Harness、能力等的具体修订 |
| Budget | 预算 | 直接使用中文 |
| Cost | 成本 | 直接使用中文 |

## 8. 系统设计术语

| English | 推荐中文 | 使用说明 |
| --- | --- | --- |
| Control Plane | 控制面 | 直接使用中文 |
| Data Plane | 数据面 | 直接使用中文 |
| Action Plane | 动作面 | 用于强调实际动作执行层 |
| Execution Control | 执行控制 | 直接使用中文 |
| Execution Environment | 执行环境 | 与工作环境相关但不完全等价 |
| Programmatic Execution | 程序化执行 | 直接使用中文 |
| Shared Resource | 共享资源 | 直接使用中文 |
| Shared State | 共享状态 | 直接使用中文 |
| Ownership | 所有权 | 指任务或资源归属 |
| Lease | 租约 | 指带期限的占有权 |
| Isolation Boundary | 隔离边界 | 直接使用中文 |
| Trust Propagation | 信任传播 | 直接使用中文 |
| Capability Grant | 能力授权 | 直接使用中文 |
| Work Frontier | 工作前沿 | 指当前可推进的任务边界 |

## 9. 架构图规则

架构图中的用户可见文本与正文遵循同一术语表：

- `label`、`sublabel`、`tag`、`note`、`cards`、连接文字优先中文。
- 标准缩写如 `LLM`、`MCP`、`API` 可以保留。
- 不因中文化修改 JSON 内部 `id`、`type`、连接端点、文件名和路径。
- 图中空间有限时，可以省略英文原词，但不得引入与正文不同的中文译法。

## 10. 修改流程

新增或调整核心术语时：

1. 先修改本术语表。
2. 再同步规范性架构文档与相关架构图。
3. 最后按需更新研究文章中的表述。
4. 不直接修改 `public/diagrams/**` 生成文件；应修改 `.architecture.json` 图源并通过现有渲染流程生成。

## 11. 自动术语门禁

仓库通过 `npm run check:terminology` 检查当前架构正文和 Archify 图源中的高频术语一致性，并在 Docs CI 中自动执行。

自动检查的范围和边界：

- 扫描 `architecture/**/*.md` 与 `diagrams/**/*.architecture.json`。
- Markdown 中忽略 fenced code block 和行内代码，避免把事件类型、字段名、命令等工程标识误判为正文。
- 允许首次采用“中文（English）”形式进行概念对码。
- 架构图只检查 `title`、`subtitle`、`label`、`sublabel`、`tag`、`note`、卡片和连接文字等用户可见字段；不检查 `id`、`type`、`from`、`to`、`sources` 等内部结构字段。
- `LLM`、`MCP`、`API`、`SaaS`、`PTC`、`HITL` 等标准缩写进入允许列表。

`terminology-rules.json` 是本术语表的**机器可执行子集**，用于承载需要自动阻断的高频英文回退、废弃中文译法和显式豁免。术语语义仍以本文件为唯一基准；新增规则时应先更新本术语表，再同步机器规则。

确有特殊场景需要保留某个受检查术语时，应在 `terminology-rules.json` 的 `fileAllowlist` 中按文件显式豁免，而不是放宽全局规则。
