# 根目录内容目录迁移设计

## 目标

将博客内容从 `src/content/` 移到仓库根目录 `content/`，降低文章目录层级，同时保持现有文章路由、内容集合名称、草稿行为、静态资源路径和构建流程不变。

## 目录结构

迁移后的内容目录为：

```text
content/
├── posts/
├── drafts/
└── diary/
```

`src/content/config.ts` 继续作为 Astro 内容集合配置入口。`posts` 和 `drafts` 改用 `astro/loaders` 提供的 `glob()`，分别显式加载 `content/posts` 和 `content/drafts` 下的 Markdown/MDX 文件。匹配规则排除文章内的 `assets` 目录，entry ID 保持相对于各 collection 根目录生成。

`diary` 当前不属于已注册的 Astro collection，本次只移动目录，不新增 collection、页面或公开路由。

## 配套路径调整

- 迁移脚本默认输出改为 `content/posts` 和 `content/drafts`。
- 静态资源复制脚本默认从 `content/posts` 搜索文章资源。
- Python 内容示例和测试中的文章路径改为 `content/posts`。
- README、AGENTS.md 和与本次功能直接相关的计划文档更新为新目录。

## 兼容性要求

- 页面仍通过 `getCollection('posts')` 和 `getCollection('drafts')` 获取内容。
- `/posts/.../` URL 和 frontmatter 中的 `postSlug` 不变。
- `public/posts-assets/` 兼容资源路径不变。
- 不提交构建生成的 `dist/`、`.astro/`、`public/posts-assets/`。
- 不修改现有页面、组件、主题或 Cloudflare 接口行为。

## 验证

- 先增加配置和默认路径断言，确认它们在旧结构下失败。
- 迁移目录并调整实现后运行 `npm run test` 和 `npm run build`。
- 检查 `/`、`/ai-notes/`、`/knowledge/`、`/about/`、`/archive/`、一篇文章页和 `/rss.xml` 的构建产物。
