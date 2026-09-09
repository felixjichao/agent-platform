# 恢复必须回到 Ground Truth

## 文章中的关键观点

文章强调新的 coding session 应先检查已有文件、Git 历史、测试状态和进度，再继续工作。

## 我们的架构分析

恢复不能只做：

```text
read progress.md
→ believe everything
→ continue
```

更可靠的是：

```text
读取 Handoff
    ↓
恢复环境
    ↓
检查 Ground Truth
    ├── Git / files
    ├── tests
    ├── artifacts
    └── runtime events
    ↓
reconcile
    ↓
继续执行
```

原因很简单：Notes 和 Progress 是 Agent 的主观投影，可能遗漏、过时甚至错误；代码、测试、外部资源和 Runtime Event 才是更接近真实事实的证据。

## 对 Agent Platform 的影响

Recovery 应被视为运行时能力：重新建立执行环境、恢复持久资源、重放或加载状态，并允许 Harness 做 Reconciliation。

## 核心结论

> **Recovery 不是重新加载一段摘要，而是用持久事实和真实环境重新建立一致状态。**