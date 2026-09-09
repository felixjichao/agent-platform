import { defineConfig } from 'vitepress'

export default defineConfig({
  lang: 'zh-CN',
  title: 'Agent Platform',
  description: '从一手工程实践持续推导 Agent Platform 的架构研究与演进。',
  base: '/agent-platform/',
  cleanUrls: true,
  rewrites(id) {
    return id.replace(/^(articles\/[^/]+)\/README\.md$/, '$1/index.md')
  },
  themeConfig: {
    nav: [
      { text: '首页', link: '/' },
      { text: '总体架构', link: '/architecture/agent-platform' },
      { text: '架构研究', link: '/articles/01-building-effective-agents/' },
      { text: 'GitHub', link: 'https://github.com/felixjichao/agent-platform' }
    ]
  }
})
