# Skill 是可执行供应链资产

## 文章中的关键观点

Skill 可以包含说明、脚本和资源，因此安装第三方 Skill 不只是“读一份文档”，还可能引入代码和行为指导。

## 我们的架构分析

Skill 的风险至少包括：

```text
Instruction Risk
→ 恶意 / 错误指导

Code / Dependency Risk
→ Script 或依赖执行风险

Capability Escalation Risk
→ Skill 诱导 Agent 使用超出任务所需的能力
```

因此必须区分：

```text
Install
≠ Activate
≠ Execute Script
≠ Grant Capability
```

Skill 可以声明自己需要哪些能力，但不能自行扩大权限：

```text
Effective Permission
≈ Skill Requirement
  ∩ Agent Policy
  ∩ User Permission
  ∩ Task Need
```

Skill Revision 也需要固定版本，保证 Recovery、Audit 和 Eval 能知道当时使用的是哪一版程序性知识。

## 对 Agent Platform 的影响

Skill Registry 必须支持来源、版本、信任、审核、权限需求和发布生命周期，而不只是文件上传。

## 核心结论

> **Skill 是可执行供应链资产；安装、激活、执行和能力授权必须是不同安全阶段。**