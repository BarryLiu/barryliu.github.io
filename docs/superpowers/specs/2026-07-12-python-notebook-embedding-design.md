# Python 代码与 Notebook 引用设计

## 目标

在现有 Astro 博客中增加一个由 uv 管理的 Python 程序区，并允许 MDX 文章引用仓库内的 `.py` 和 `.ipynb` 文件。博客构建不执行 Notebook，只渲染其中已经保存的 Markdown、代码和文本/图片输出。

## 目录

- `app/`：可运行、可复用的 Python 程序。
- `notebooks/`：Jupyter Notebook 源文件。
- `scripts/render_python_content.py`：把允许公开的 Python 内容转换为 Astro 可读取的 JSON。
- `src/generated/python-content/`：生成的结构化内容，随源文件一同提交。
- `public/python-content/`：Notebook 提取出的图片。
- `src/components/python/`：MDX 引用组件。

## 引用接口

文章使用 MDX，并通过稳定的仓库相对路径引用：

```mdx
<PythonSource src="app/demo.py" />
<Notebook src="notebooks/demo.ipynb" />
```

组件只读取生成目录，不允许读取任意绝对路径。找不到对应生成内容时构建失败，从而避免发布过期或失效引用。

## 构建链路

本地执行 `uv run python scripts/render_python_content.py` 更新生成物。`npm run python:check` 使用 `--check` 校验生成物是否同步；`npm run build` 在 Astro 构建前执行该检查。Cloudflare Pages 因为使用已提交的生成物，不需要安装 Python 或 uv。

## 渲染范围与安全

第一版支持 Notebook 的 Markdown、Python 代码、纯文本输出和 PNG/JPEG 图片。Notebook 不会被执行；HTML、JavaScript、widgets 和未知 MIME 输出不会直接注入页面。带 `hide-cell` 或 `blog-ignore` tag 的单元格不进入生成内容。

