# 把脑和手解耦

## 文章中的关键观点

文章标题强调“Decoupling the brain from the hands”：模型和 Harness 所组成的控制侧，不应该与执行代码、文件操作和环境管理强绑定。

## 我们的架构分析

可以把 Agent 系统拆成两侧：

```text
Brain / Control
模型 + Harness
    │
    │ Action Request
    ▼
Hands / Execution
工具 + 环境 + 资源
```

控制侧可以频繁演进，执行侧则需要提供稳定、受治理的动作接口。一个 Harness 不应该直接把自己和某台机器、某个文件系统或某套工具实现绑定。

这与传统控制面 / 数据面分离类似，但此时首先强调的是**决策逻辑与执行载体的解耦**。

## 对 Agent Platform 的影响

统一平台应通过 Action / Result 之类的稳定协议连接 Harness 与执行环境，使 Harness 可以换模型、换策略、换实现，而不重建整个执行基础设施。

## 核心结论

> **Agent 的“脑”和“手”应该通过稳定执行接口解耦；Harness 不直接等同于执行环境。**