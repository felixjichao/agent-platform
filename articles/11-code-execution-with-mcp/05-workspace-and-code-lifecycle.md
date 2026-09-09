# Workspace 与生成代码生命周期

## 文章中的关键观点

代码执行让 Agent 能生成程序、保存中间文件、复用结果，而不是每个 Tool Call 都完全瞬时存在。

## 我们的架构分析

这使 Workspace 进一步成为 Agent Work Environment 的核心：

```text
Workspace
├── Intermediate Files
├── Generated Programs
├── Checkpoints
├── Data Artifacts
└── Progress
```

生成代码还应区分生命周期：

### Ephemeral Code

- 当前 Run 临时生成；
- 用完即可销毁。

### Workspace Code

- 当前 Work 会重复使用；
- 需要版本和持久状态。

### Promoted Capability

- 多个 Work 都值得复用；
- 需要评审、Eval、安全检查、版本化；
- 最终可以沉淀成 Skill Script、Tool 或其他平台 Capability。

```text
Ephemeral
   ↓ useful
Workspace
   ↓ reusable
Candidate Capability
   ↓ Eval / Security / Review
Promoted Capability
```

## 对 Agent Platform 的影响

Agent 可以提出 Capability Candidate，但不应在一个正在执行的生产 Session 中直接把临时代码“自发布”为全局可信能力。

## 核心结论

> **生成代码有 Run、Work、Platform 三个生命周期；从临时代码到共享 Capability 必须经过治理晋升。**