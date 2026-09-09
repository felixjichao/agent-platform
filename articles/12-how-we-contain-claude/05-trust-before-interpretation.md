# Trust before privileged interpretation

## 文章中的关键观点

Claude Code 曾出现过在用户确认信任项目之前，就读取或执行项目配置 / hook 的问题。核心教训是 Trust Boundary 必须建立在任何有副作用的加载和执行之前。

## 我们的架构分析

Agent 场景比传统软件更进一步，因为“读取内容”本身也可能改变模型行为。

```text
read README
→ enters Context
→ influences model
→ changes Action decisions
```

所以 Observation Channel 本身可能成为控制通道。

推荐 Trust Lifecycle：

```text
Discovered
   ↓
Untrusted
   ↓ validate / policy
Trusted for Read
   ↓
Trusted for Instruction
   ↓
Trusted for Execution
```

这不是一个简单 `trusted=true`。

对于 Skill、MCP、Workspace config 等，应区分：

- 发现 metadata；
- 读取完整内容；
- 允许内容作为 instruction；
- 执行 script / hook / local server。

本地文件也不天然可信，因为它可能来自 git clone、下载文件、同步目录或附件。

## 对 Agent Platform 的影响

Trust Boundary 应覆盖 Discovery、Parse、Load、Interpret、Execute 全生命周期。

## 核心结论

> **Locality ≠ Trust。对于 Agent，读取本身可能影响行为，因此要做到 Trust before privileged interpretation。**