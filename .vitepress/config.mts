import { existsSync, readdirSync, readFileSync } from 'node:fs'
import { resolve } from 'node:path'
import { fileURLToPath } from 'node:url'
import { defineConfig } from 'vitepress'

const repoRoot = fileURLToPath(new URL('..', import.meta.url))
const articlesRoot = resolve(repoRoot, 'articles')

function plainTextTitle(title: string) {
  return title
    .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1')
    .replace(/[`*_]/g, '')
    .trim()
}

function markdownTitle(filePath: string, fallback: string) {
  if (!existsSync(filePath)) return fallback

  const content = readFileSync(filePath, 'utf8')
  const heading = content.match(/^#\s+(.+)$/m)?.[1]
  return plainTextTitle(heading ?? fallback)
}

function fallbackTitle(fileName: string) {
  return fileName
    .replace(/\.md$/, '')
    .replace(/^\d+-/, '')
    .split('-')
    .filter(Boolean)
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ')
}

function buildArticleSidebar() {
  return readdirSync(articlesRoot, { withFileTypes: true })
    .filter((entry) => entry.isDirectory() && /^\d+-/.test(entry.name))
    .sort((a, b) => a.name.localeCompare(b.name, 'en', { numeric: true }))
    .map((entry) => {
      const articleDir = resolve(articlesRoot, entry.name)
      const articleNumber = entry.name.match(/^(\d+)-/)?.[1] ?? ''
      const articleTitle = markdownTitle(resolve(articleDir, 'README.md'), fallbackTitle(entry.name))
      const chapters = readdirSync(articleDir, { withFileTypes: true })
        .filter((file) => file.isFile() && /^\d+-.*\.md$/.test(file.name))
        .sort((a, b) => a.name.localeCompare(b.name, 'en', { numeric: true }))
        .map((file) => ({
          text: markdownTitle(resolve(articleDir, file.name), fallbackTitle(file.name)),
          link: `/articles/${entry.name}/${file.name.replace(/\.md$/, '')}`
        }))

      return {
        text: `${articleNumber} · ${articleTitle}`,
        collapsed: true,
        items: [
          { text: '概览', link: `/articles/${entry.name}/` },
          ...chapters
        ]
      }
    })
}

export default defineConfig({
  lang: 'zh-CN',
  title: 'Agent Platform',
  description: '从一手工程实践持续推导 Agent Platform 的架构研究与演进。',
  base: '/agent-platform/',
  cleanUrls: true,
  lastUpdated: true,
  rewrites(id) {
    return id.replace(/^(articles\/[^/]+)\/README\.md$/, '$1/index.md')
  },
  themeConfig: {
    nav: [
      { text: '首页', link: '/' },
      { text: '架构图谱', link: '/architecture/' },
      { text: '总体架构', link: '/architecture/agent-platform' },
      { text: '架构研究', link: '/articles/01-building-effective-agents/' },
      { text: '写作规范', link: '/docs-style-guide' }
    ],
    sidebar: {
      '/architecture/': [
        {
          text: 'Agent Platform 架构',
          items: [
            { text: '架构图谱', link: '/architecture/' },
            { text: '总体架构', link: '/architecture/agent-platform' },
            { text: 'L7 · 业务 / 产品', link: '/architecture/l7-business-product' },
            { text: 'L6 · 能力契约', link: '/architecture/l6-capability-contract' },
            { text: 'L5 · 能力工程', link: '/architecture/l5-capability-engineering' },
            { text: 'L4 · 执行策略 / Harness', link: '/architecture/l4-strategy-harness' },
            { text: 'L3 · 统一 Runtime', link: '/architecture/l3-runtime' },
            { text: 'L2 · Work Environment', link: '/architecture/l2-work-environment' },
            { text: 'L1 · 基础设施 / 真实世界', link: '/architecture/l1-infrastructure-real-world' },
            { text: '横切系统与治理', link: '/architecture/cross-cutting-governance' }
          ]
        }
      ],
      '/articles/': buildArticleSidebar()
    },
    search: {
      provider: 'local',
      options: {
        translations: {
          button: { buttonText: '搜索文档', buttonAriaLabel: '搜索文档' },
          modal: {
            noResultsText: '没有找到相关结果',
            resetButtonTitle: '清除查询',
            footer: { selectText: '选择', navigateText: '切换', closeText: '关闭' }
          }
        }
      }
    },
    outline: { level: [2, 3], label: '本页目录' },
    docFooter: { prev: '上一篇', next: '下一篇' },
    lastUpdated: { text: '最后更新于' },
    editLink: {
      pattern: 'https://github.com/felixjichao/agent-platform/edit/main/:path',
      text: '在 GitHub 上编辑'
    },
    socialLinks: [
      { icon: 'github', link: 'https://github.com/felixjichao/agent-platform' }
    ],
    footer: {
      message: '研究过程与当前架构分离沉淀，Markdown 与 Archify 图源共同表达当前架构。',
      copyright: 'Agent Platform'
    }
  }
})
