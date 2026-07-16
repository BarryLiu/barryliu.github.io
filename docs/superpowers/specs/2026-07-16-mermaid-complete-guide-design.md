# Mermaid 完整图表指南与站内渲染设计

日期：2026-07-16

## 目标

为博客新增一篇中文 Mermaid 完整指南，覆盖 Mermaid Live Editor 当前展示的图表类型，并补充 Mermaid 官方文档中已提供但截图未完全展示的类型。文章中的 Mermaid 示例需要在站内直接渲染为 SVG，同时保留可查看、可复制的源代码。

本次改动还要提供可复用的 Mermaid 文章渲染能力，使后续任意 Markdown 或 MDX 文章都能通过 `mermaid` 代码围栏展示图表。

## 变更范围

### 文章

新增 `content/posts/tool/mermaid-complete-guide.md`，frontmatter 遵循现有 Astro Content Collections schema，文章路由为 `/posts/tool/mermaid-complete-guide/`。

文章覆盖以下图表：

- 流程与交互：Flowchart、Swimlanes、Sequence、State、User Journey、Timeline。
- 软件与系统设计：Class、Entity Relationship、Architecture、Block、C4、Requirement、Event Modeling。
- 项目与研发管理：Gantt、Git Graph、Kanban、Mindmap、TreeView。
- 数据分析：Pie、Quadrant、XY Chart、Radar、Sankey、Treemap、Venn。
- 网络、协议与语法：Packet、Railroad ABNF、Railroad EBNF、Railroad IR、Railroad PEG。
- 分析与战略：Cynefin Framework、Ishikawa、Wardley Map。
- 其他：ZenUML，以及 Mermaid 官方目录或 Live Editor 中适合补充说明的新增、测试或实验类型。

每种图表包含：

1. 用途和适用场景。
2. 一段能够在目标 Mermaid 版本中解析的中文示例。
3. 站内渲染结果和可展开的原始代码。
4. 关键语法、限制与常见错误。
5. 对应的 Mermaid 官方文档或 Mermaid Live Editor 链接。

文章还包含 Mermaid Live Editor 操作、初始化配置、frontmatter 配置、主题变量、样式与 class、布局方向、无障碍信息、安全级别、导出方法、版本兼容、错误排查，以及“需求到图表类型”的速查表。

### 渲染能力

新增一个 Astro Mermaid 渲染组件，并在文章布局中统一加载。组件查找文章正文中的 `pre > code.language-mermaid`，保存源码后调用本地安装的 Mermaid npm 包进行浏览器端 SVG 渲染。

渲染行为：

- Mermaid 依赖固定在支持本篇示例语法的 11.x 版本，并提交 lockfile 变化。
- 页面没有 Mermaid 代码块时不执行渲染逻辑，并通过动态导入避免无关文章加载 Mermaid 主模块。
- 每个图表生成独立 ID，按顺序渲染，避免同页多图 ID 冲突。
- 默认使用严格安全级别，禁止图表定义注入任意脚本。
- 图表采用与站点深色赛博水族馆主题协调的基础主题和青色、品红、荧光绿变量。
- 图表容器允许横向滚动，SVG 保持清晰，并适配窄屏。
- 渲染后保留一个可展开的源码区，继续使用现有 Shiki 代码样式，并提供复制按钮。
- 单图渲染失败时保留源码并显示该图的错误提示，不中断其他图表。
- C4、TreeView、Wardley、Railroad 等有实验性、beta 或版本要求的类型在文章中明确标识。

## 内容组织

文章先用速查表帮助读者按需求选择图表，再按用途分组深入讲解。图表章节采用一致模板，避免三十多个章节变成无层次的语法罗列。

文章目录大纲：

1. Mermaid 是什么以及为什么适合文档即代码。
2. Mermaid Live Editor 入门。
3. 最小语法、配置、主题和安全说明。
4. 图表选择速查表。
5. 按用途分组的完整图表教程。
6. 站点、Markdown 和 GitHub 等环境中的兼容差异。
7. 常见错误与调试方法。
8. 综合示例与继续学习链接。

## 错误处理与兼容性

所有文章示例必须通过目标 Mermaid 版本的 `parse` 或等价 API 验证。对于仅在特定版本、beta 语法或实验状态下可用的图表，文章显式写明前置条件，不能把 Mermaid Live Editor 的示例菜单等同于所有旧版渲染器都支持。

浏览器端渲染失败时，页面仍然展示原始 Mermaid 代码，保证文章内容可读。JavaScript 被禁用时同样保留源码作为降级结果。

## 验证

至少完成以下验证：

1. 为 Mermaid 代码块识别、渲染组件接入或文章结构补充必要的自动化测试。
2. 使用目标 Mermaid 版本批量解析文章中的全部 Mermaid 代码块。
3. 运行 `npm run test`。
4. 运行 `npm run build`。
5. 本地打开 `/posts/tool/mermaid-complete-guide/`，确认全部示例渲染、源码展开、复制、宽图滚动和移动端布局。
6. 抽查 `/`、`/ai-notes/`、`/knowledge/`、`/about/`、`/archive/`、另一篇普通文章和 `rss.xml`，确认通用文章布局没有回归。

若完整构建被当前工作树中与本次任务无关的既有问题阻塞，需要记录准确错误，并继续完成可独立执行的 Mermaid 定向验证；不得为绕过错误而修改无关文件。

## 非目标

- 不修改现有文章内容。
- 不提交 `dist/`、`.astro/`、`node_modules/` 或生成的静态资源目录。
- 不实现可视化拖拽编辑器。
- 不替代 Mermaid Live Editor，也不在站内保存用户图表。
- 不修改 Cloudflare Pages 项目、生产分支或部署绑定。

## 完成标准

文章完整覆盖设计范围内的图表类型；每种类型都有可运行示例、使用场景、语法提示和来源链接。文章页直接显示 SVG 图表并保留源码，单图失败能够安全降级。测试、构建和关键页面检查的结果在最终交付中如实说明。
