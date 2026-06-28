import { defineConfig } from 'vitepress'

// https://vitepress.dev/reference/site-config
export default defineConfig({
  // GitHub 项目页：https://cbl315.github.io/ai-roadmap/
  // 若未来改用自定义域名（如 roadmap.woshicai.tech），把 base 改回 '/' 即可
  site: 'https://cbl315.github.io',
  base: '/ai-roadmap/',

  lang: 'zh-CN',
  title: 'AI 学习路线',
  description: 'Backend Developer → AI-Powered One Person Company',

  // claude-rules/ 是开发规范，不纳入公开站点
  srcExclude: ['**/claude-rules/**'],

  // 站点最后更新时间（基于 git commit）
  lastUpdated: true,

  // 本地搜索（无需第三方服务）
  search: {
    provider: 'local',
    options: {
      translations: {
        button: {
          buttonText: '搜索文档',
          buttonAriaLabel: '搜索文档'
        },
        modal: {
          noResultsText: '无法找到相关结果',
          resetButtonTitle: '清除查询条件',
          footer: {
            selectText: '选择',
            navigateText: '切换'
          }
        }
      }
    }
  },

  themeConfig: {
    // 站点头部的标题（留空，靠 logo 即可，logo 后用 title 文案）
    siteTitle: 'AI 学习路线',

    // 社交链接（导航栏右侧图标）
    socialLinks: [
      { icon: 'github', link: 'https://github.com/cbl315/ai-roadmap' }
    ],

    // 顶部导航
    nav: [
      { text: '首页', link: '/' },
      { text: '学习路线', link: '/guide/roadmap' },
      { text: '调研笔记', link: '/notes/rag' },
      {
        text: '学习成果',
        link: '/references/phase2-web-chat'
      }
    ],

    // 左侧导航栏：按目录分组
    sidebar: {
      '/guide/': [
        {
          text: '学习路线',
          items: [
            { text: '总览', link: '/guide/roadmap' }
          ]
        }
      ],
      '/notes/': [
        {
          text: '调研笔记',
          items: [
            { text: 'RAG 检索增强生成', link: '/notes/rag' }
          ]
        }
      ],
      '/references/': [
        {
          text: '学习成果',
          items: [
            { text: 'Web AI NPC 聊天实现', link: '/references/phase2-web-chat' }
          ]
        }
      ]
    },

    // 右侧大纲栏
    outline: {
      level: [2, 3],
      label: '本页导航'
    },

    docFooter: {
      prev: '上一篇',
      next: '下一篇'
    },

    lastUpdatedText: '最后更新',

    returnToTopLabel: '回到顶部',

    sidebarMenuLabel: '菜单',

    darkModeSwitchLabel: '主题',

    lightModeSwitchTitle: '切换到浅色模式',
    darkModeSwitchTitle: '切换到深色模式'
  }
})
