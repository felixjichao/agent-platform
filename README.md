# Agent Platform

本仓库用于沉淀智能体平台（Agent Platform）的架构研究与演进过程。

## 文档入口

- [智能体平台总体架构](architecture/agent-platform.md)：当前规范性架构文档，记录经过研究后已经稳定下来的平台架构。
- [文档写作规范](docs-style-guide.md)：中文优先、术语使用、文章来源与架构推导分离等规则。
- `articles/`：按研究文章保存逐节讨论和架构推导。

## 研究文章

1. [Building effective agents](articles/01-building-effective-agents/README.md)
2. [Scaling Managed Agents: Decoupling the brain from the hands](articles/02-scaling-managed-agents/README.md)
3. [Effective context engineering for AI agents](articles/03-effective-context-engineering/README.md)
4. [Effective harnesses for long-running agents](articles/04-effective-harnesses-for-long-running-agents/README.md)
5. [Harness design for long-running application development](articles/05-harness-design-for-long-running-apps/README.md)
6. [How we built our multi-agent research system](articles/06-multi-agent-research-system/README.md)
7. [Building a C compiler with a team of parallel Claudes](articles/07-building-c-compiler/README.md)
8. [Demystifying evals for AI agents](articles/08-demystifying-evals-for-ai-agents/README.md)
9. [Writing effective tools for agents — with agents](articles/09-writing-effective-tools-for-agents/README.md)
10. [Equipping agents for the real world with Agent Skills](articles/10-agent-skills/README.md)
11. [Code execution with MCP: Building more efficient agents](articles/11-code-execution-with-mcp/README.md)
12. [How we contain Claude across products](articles/12-how-we-contain-claude/README.md)

## 组织方式

每篇文章一个目录，每次讨论的核心问题拆成一个独立 Markdown 小节：

```text
articles/<article>/
├── README.md
├── 01-<topic>.md
├── 02-<topic>.md
└── ...
```

文章目录保留三类信息：

1. **文章观点**：原文实际支持的内容。
2. **架构分析**：结合讨论形成的抽象、修正和推导。
3. **平台影响**：这些结论如何改变 Agent Platform。

`architecture/agent-platform.md` 不按文章组织，而是按平台架构组织，是当前架构的事实入口。

## 架构演进方式

每完成一篇文章，都采用两阶段提交：

```text
文章研究提交
  ↓
架构吸收 / 修正
  ↓
架构演进提交
```

因此可以直接查看：

```bash
git log -- architecture/agent-platform.md
```

回溯从执行控制、Managed Agents、上下文工程、长任务、多智能体、Eval、能力工程、PTC 到安全治理的完整架构演进。

## 写作原则

- 正文尽可能使用中文。
- 重要英文术语首次出现时保留原词，之后优先使用中文。
- 目录名、文件名、接口、事件类型和代码标识符保持英文。
- 不把我们的架构推导伪装成文章来源。
- 一节只处理一个核心问题。
