# 从 Isolated World 到 Shared-State Collaboration

## 文章中的关键观点

C 编译器实验中的多个 Claude 并不是各自在隔离世界里完成完整方案再汇总，而是并行修改同一大型代码库。它们需要面对真实冲突、测试失败、他人提交和不断变化的共享状态。

## 我们的架构分析

可以区分两类 Multi-Agent：

### Isolated-world

```text
Parent
 ├── Child A → 独立问题
 ├── Child B → 独立问题
 └── Child C → 独立问题
      ↓
   merge results
```

适合研究、信息搜集等高度独立任务。

### Shared-world

```text
        Shared Work State
       /       |        \
Agent A     Agent B     Agent C
 local       local       local
working     working     working
copy        copy        copy
```

它们共享同一个事实世界，却需要局部隔离来避免直接踩踏。

因此，共享状态至少需要：

- identity / version；
- ownership / lease；
- snapshot；
- change；
- conflict。

## 对 Agent Platform 的影响

Multi-Agent 不能只设计 Agent Message Bus，还要设计共享 Work State。很多协作应该通过环境和资源状态发生，而不是不断互发自然语言消息。

## 核心结论

> **多智能体协作既可能是消息协作，也可能是共享世界协作；真实工程任务更需要 Shared State + Local Isolation。**