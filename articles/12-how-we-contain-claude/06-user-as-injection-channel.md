# 用户也可能成为 Prompt Injection 通道

## 文章中的关键观点

文章讨论了攻击者诱导用户把恶意 Prompt 直接复制给 Claude Code 的红队案例。对模型而言内容来自用户，但真正 Intent Origin 可能来自攻击者。

## 我们的架构分析

传统信任模型容易认为：

```text
User Instruction → high trust
External Content → low trust
```

但 phishing / copy-paste attack 形成：

```text
Attacker
   ↓
Email / Slack / Issue
   ↓
User copies prompt
   ↓
Agent
```

因此：

> **Instruction Source != Intent Origin。**

“Ask the user”也不是万能安全边界，因为攻击链本身可能就是诱导用户授权。

需要区分：

### Intent Authorization

用户定义：我想完成什么。

### Capability Authorization

系统决定：为了这个 Work，Agent 实际获得什么能力。

```text
User Intent
≠ Effective Capability Grant
```

用户要求也不能自动突破 Secret、Filesystem、Egress 等系统硬边界。

## 对 Agent Platform 的影响

Human Approval 主要用于用户有能力做出的业务语义判断，不能承担 Credential Isolation、Network Egress 等基础设施安全职责。

## 核心结论

> **来自 User 并不等于来自 User 的真实意图；User Intent 可以定义目标，但不能自动扩大 Capability Boundary。**