# 从 Sandbox 泛化到 Execution Environment

## 文章中的关键观点

Managed Agents 的执行侧需要为 Agent 提供代码、文件和外部系统操作能力。Sandbox 是重要实现，但不是唯一形态。

## 我们的架构分析

如果平台把执行侧直接定义为 Sandbox，会无法覆盖很多真实场景：

- SaaS API；
- MCP Server；
- 数据库；
- 浏览器；
- 远程计算机；
- 企业内部服务；
- 机器人或其他设备。

因此更稳定的抽象是**执行环境（Execution Environment）**：它描述 Agent 实际可以观察和操作的世界，Sandbox 只是其中一种隔离实现。

```text
Execution Environment
├── Sandbox / VM
├── API / MCP
├── DB
├── Browser
├── Filesystem
└── Remote Computer / Device
```

## 对 Agent Platform 的影响

统一运行时通过动作协议访问执行环境，而不同环境负责自己的连接、隔离和资源实现。后续安全、权限和观测也应围绕执行环境统一治理。

## 核心结论

> **Sandbox 是实现手段，Execution Environment 才是平台层稳定抽象。**