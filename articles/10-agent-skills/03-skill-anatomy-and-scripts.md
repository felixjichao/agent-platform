# Skill Anatomy 与 Skill-local Script

## 文章中的关键观点

一个 Skill 目录可以包含 `SKILL.md`、脚本、参考资料和资源。说明文件指导 Agent，脚本负责稳定可重复的具体操作。

## 我们的架构分析

可以把 Skill 内部拆成：

```text
Skill
├── Instructions
├── Scripts
├── References
└── Resources
```

其中 Skill-local Script 与 Tool 不完全相同。

### Skill-local Script

- 为某个 Skill 服务；
- 通常在本地 Execution Environment 中运行；
- 封装稳定的 deterministic mechanics；
- 不一定值得成为平台全局 Capability。

### Tool

- 平台级行动能力；
- 面向多个 Agent / Skill 复用；
- 有独立 Permission、Audit、Contract 和治理。

因此 Skill 可以通过 Script 减少 Tool Explosion：不是每个稳定小操作都要注册成全局 Tool。

## 对 Agent Platform 的影响

Skill Runtime 需要允许安全读取资源和执行本地脚本，但脚本执行权限仍然受 Execution Environment Policy 约束。

## 核心结论

> **Skill 既能承载知识，也能携带局部 deterministic implementation；Skill Script 不自动等于平台 Tool。**