# Repository Guidelines（仓库指南）

## 项目结构

本仓库是一个 Jekyll / GitHub Pages 博客。`_config.yml` 是站点配置；`index.html`、`feed.xml` 和 `page/` 是首页、订阅和归档等入口页面。已发布文章放在 `_posts/`，文件名使用 `YYYY-MM-DD-title.md` 格式，可按主题放入 `_posts/skill/`、`_posts/work/`、`_posts/ailearn/` 等目录。未发布草稿放在 `_drafts/`。页面模板在 `_layouts/`，可复用片段在 `_includes/`。样式入口是 `css/main.scss`，样式片段在 `_sass/`。脚本放在 `js/`，图片和附件放在 `images/`、`assets/` 或文章所属目录的 `assets/` 中。`_site/` 是构建产物，不要手动修改，也不要提交。

## 文件结构规范

新增页面优先放在 `page/`，新增文章放在 `_posts/<topic>/`，新增草稿放在 `_drafts/<topic>/`。布局级改动放在 `_layouts/`，通用导航、页脚、评论、标签、分类等片段放在 `_includes/`。不要把页面结构、样式和脚本混在同一个文件里；只在当前页面专用逻辑很少时允许内联。新增图片优先放在对应主题目录的 `assets/` 中，例如 `_posts/work/assets/`，全站通用图片才放到根目录 `assets/` 或 `images/`。

## 构建、测试和本地运行

- `docker compose up -d`：启动 Jekyll 3.8，本地访问 `http://localhost:4000`。
- `docker compose logs -f jekyll`：查看 Jekyll 构建和运行日志。
- `docker compose run --rm jekyll jekyll build`：执行一次完整构建，用于检查 Markdown、Liquid、Sass 和链接生成错误。
- `docker compose down`：停止本地容器。

仓库没有提交 `Gemfile`，优先使用 `docker-compose.yml` 中定义的 Docker 环境。

## 编码和命名规范

Markdown、HTML、Liquid、YAML、SCSS 都使用 UTF-8。保持和周围文件一致的格式；YAML、HTML、Liquid、SCSS 默认使用两个空格缩进。文章文件名必须带日期前缀，并使用短横线连接英文或拼音关键词，例如 `_posts/skill/2025-04-07-pyqt6-learn.md`。新增分类时，优先复用现有目录结构。图片应放在内容附近，并使用稳定的相对路径引用。

## 主题设计规范

修改主题、页面布局或组件样式时，优先使用 Tailwind CSS 的 utility class 表达间距、字号、颜色、布局和响应式规则，避免新增大段手写 CSS。若当前构建链尚未接入 Tailwind CSS，需要先说明方案并补齐必要配置；只做小范围兼容旧页面时，才沿用现有 `css/main.scss` 和 `_sass/`。主题风格保持博客阅读优先：正文清晰、导航稳定、颜色克制、移动端可读。不要为了装饰添加复杂动画、过度渐变或影响阅读的背景效果。

## 验证要求

本仓库没有自动化测试套件。修改文章、模板、样式或配置后，至少运行 `docker compose run --rm jekyll jekyll build`。涉及页面展示时，还要本地打开相关页面检查 front matter、标题、代码块、图片、分页、分类和标签是否正常。不要提交 `_site/`、`.sass-cache/`、日志、临时文件、IDE 配置或本机私有配置文件。

## 提交和 PR 规范

提交信息使用简短中文动作描述，参考历史记录：`添加设计文档`、`同步整理文档`、`整理格式`。PR 内容需要说明：本次改了哪些文章或页面、为什么改、是否改动 `_config.yml` / `CNAME` / Docker 配置、是否已完成本地构建。视觉变化需要附截图或说明影响页面。

## 给 AI Agent 的特别说明

收到“总结需要提交 PR 的内容”这类请求时，必须同时参考当前 Git 未提交变更和本次 session 的聊天上下文。总结应包含：变更范围、主要文件、用户可见影响、验证结果、风险或未验证项。不要凭空补充没有在 diff 或聊天中出现的内容。
