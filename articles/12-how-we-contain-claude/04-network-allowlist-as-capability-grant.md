# Network Allowlist 本质是 Capability Grant

## 文章中的关键观点

Anthropic 在实际安全测试中发现，仅仅 allowlist 一个看起来可信的域名，并不能阻止数据被发送到攻击者控制的同一 SaaS / API 租户。域名可信不等于该域名下所有行为都安全。

## 我们的架构分析

传统规则：

```text
allow api.example.com
```

真正授予的却可能是一组远程能力：

- upload；
- remote fetch；
- create resource；
- call model；
- write to tenant。

因此：

> **Allowed Domain = Capability Grant，而不仅是 Destination Filter。**

权限判断需要升级成：

```text
Who are you acting as?
+ What capability are you invoking?
+ Which resource / tenant?
+ Where is the data going?
```

核心授权单元逐渐接近：

```text
Principal
× Capability
× Resource
× Scope
× Duration
```

Data Flow 也不能只看域名：同一个 SaaS 域名下，公司 Tenant 与攻击者 Tenant 是完全不同的目的地。

## 对 Agent Platform 的影响

Egress Governance 应同时考虑 Destination、Capability、Credential、Tenant / Principal、Data Classification 和 Provenance。

## 核心结论

> **Network Destination 是地址，不是安全语义；Agent Authorization 应围绕 Principal、Capability、Resource 和 Scope 建模。**