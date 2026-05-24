# Repository Guidelines（仓库指南）

## 项目结构

本仓库当前主站是一个 **Astro + TypeScript + Content Collections** 静态博客，部署目标是 **Cloudflare Pages**。旧 Jekyll 文章和草稿已迁移到 Astro Content Collections，旧 Jekyll 目录结构不再作为内容来源。

Astro 入口在 `src/`：页面放在 `src/pages/`，布局放在 `src/layouts/`，组件放在 `src/components/`，站点数据放在 `src/data/`，通用样式放在 `src/styles/`，工具函数放在 `src/utils/`。正式文章位于 `src/content/posts/`，草稿位于 `src/content/drafts/`，内容集合 schema 在 `src/content/config.ts`。迁移脚本是 `scripts/migrate-posts.mjs`，静态资源复制脚本是 `scripts/copy-static-assets.mjs`。构建产物是 `dist/`，Astro 缓存是 `.astro/`，不要提交。

## 文件结构规范

新增页面优先放在 `src/pages/`，新增组件放在 `src/components/`，新增布局放在 `src/layouts/`。新增站点级数据优先放在 `src/data/`，不要把导航、项目列表、社交链接硬编码散落到多个页面里。新增正式文章写入 `src/content/posts/<topic>/title.md`，新增草稿写入 `src/content/drafts/<topic>/title.md` 并保留 `draft: true`。全站品牌图标放在 `public/assets/brand/`，构建前复制出来的 `public/images/`、`public/posts-assets/` 不要手动维护。

## 构建、测试和本地运行

- `npm install`：安装 Astro 和构建依赖。
- `npm run migrate`：兼容旧迁移入口；旧 Jekyll 目录不存在时返回 0，不覆盖现有 Astro 内容。
- `npm run assets`：从 `src/content/posts/**/assets` 复制文章静态资源到 `public/posts-assets/` 兼容路径，并复制根 `favicon.ico`。
- `npm run dev`：启动 Astro，本地访问 `http://localhost:4321`。
- `npm run build`：执行迁移、复制资源并构建 `dist/`。
- `npm run preview`：预览 `dist/`。
- `npm run dev:cloudflare`：先构建 `dist/`，再用 Wrangler Pages 本地预览 Cloudflare Functions 和 KV 绑定。
- `npm run test`：运行 Node 内置测试，覆盖迁移和项目配置。
- `docker compose up`：用 Node 22 容器启动 Astro dev server。
- `docker compose run --rm astro npm run build`：在容器中执行完整构建。

Cloudflare Pages 配置：Build command 使用 `npm run build`，Build output directory 使用 `dist`，Node 版本建议 `22`。如使用 GitHub Actions 发布，需要配置 `CLOUDFLARE_API_TOKEN`、`CLOUDFLARE_ACCOUNT_ID` 和 `CLOUDFLARE_PROJECT_NAME`。文章访问量和赞/踩统计使用 Pages Function `functions/api/post-stats.ts` 与 KV 绑定 `POST_STATS`；Cloudflare 后台需要创建同名 KV namespace，并让 Pages 项目绑定为 `POST_STATS`。本地调试统计接口使用 `npm run dev:cloudflare`，接口路径是 `/api/post-stats`。

## 编码和命名规范

TypeScript、Astro、Markdown、YAML、CSS 都使用 UTF-8。保持两个空格缩进。组件文件使用 PascalCase，例如 `CyberHero.astro`；工具函数使用 camelCase；数据文件使用小写复数名，例如 `projects.ts`。文章文件名使用短横线关键词，例如 `src/content/posts/skill/pyqt6-learn.md`。迁移脚本会把旧 Jekyll frontmatter 统一为 Astro Content Collections 可读格式。

## 主题设计规范

当前主题来源是 `design.pen` 的“想飞的鱼 / 赛博水族馆”设计系统。修改首页、导航、项目卡、文章卡、分类/标签、关于页、AI 笔记和知识库页面时，优先贴合设计稿中的深色网格背景、青色/品红/荧光绿高光、矩形全息鱼缸、项目雷达、文章列表和紧凑卡片结构。样式主入口是 `src/styles/global.css` 和 `src/styles/tokens.css`，组件内部可使用 scoped CSS。不要再新增 Jekyll Sass，也不要依赖 `_sass/`。

## 验证要求

修改迁移脚本、内容模型、页面、样式或部署配置后，至少运行 `npm run test` 和 `npm run build`。涉及页面展示时，还要本地打开或请求关键页面：`/`、`/ai-notes/`、`/knowledge/`、`/about/`、`/archive/`、任意一篇 `/posts/.../` 文章，以及 `rss.xml`。当前正式文章目标是 `src/content/posts/` 下 185 篇，草稿在 `src/content/drafts/` 下且不生成公开文章路由。不要提交 `dist/`、`.astro/`、`node_modules/`、复制生成的 `public/images/`、`public/posts-assets/`、日志、临时文件、IDE 配置或本机私有配置。

## 提交和 PR 规范

提交信息使用简短中文动作描述，例如：`迁移 Astro 博客`、`同步 Cloudflare 部署配置`、`优化赛博水族馆首页`。PR 内容需要说明：本次改了哪些页面/组件/脚本、是否改动部署配置、是否影响内容集合或迁移逻辑、是否已运行 `npm run test` 和 `npm run build`。视觉变化需要附截图或说明影响页面。涉及 Cloudflare 发布时，说明 Pages 项目名、构建命令和输出目录。

## 给 AI Agent 的特别说明

收到“总结需要提交 PR 的内容”这类请求时，必须同时参考当前 Git 未提交变更和本次 session 的聊天上下文。总结应包含：变更范围、主要文件、用户可见影响、验证结果、风险或未验证项。不要凭空补充没有在 diff 或聊天中出现的内容。修改迁移逻辑时，优先补充 `tests/*.test.mjs`，先看到测试失败，再实现修复。
