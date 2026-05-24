# Barry's Blog

个人学习博客文章记录页面，欢迎评论交流。

## 技术栈

- **评论系统**：GitHub Discussions + Giscus
- **框架**：Astro
- **托管平台**：Cloudflare Pages（免费：500分钟构建/月，付费：$20/月 = 5000分钟）
- **数据存储**：Cloudflare KV（免费：10万次读取/天 + 1000次写入/天，付费：$5/百万写入）

---

## 安装说明

### 1. 基础配置

1. fork 仓库到自己的 GitHub
2. 修改仓库名字为：`username.github.io`
3. clone 到本地，参考 `_posts` 目录结构创建文章
4. 修改 CNAME 或删掉使用默认域名
5. 修改 `_config.yml` 配置项
6. 修改 `src/data/site.ts` 配置项
7. fork 后将 `_posts/barry` 目录删除（博主生活吐槽）

### 2. Cloudflare Pages 部署

#### wrangler.toml 配置

```toml
name = "your-project-name"        # 修改为你的项目名，对应 CLOUDFLARE_PROJECT_NAME
pages_build_output_dir = "dist"   # 构建输出目录，一般不改
compatibility_date = "2026-05-18"

[[kv_namespaces]]
binding = "POST_STATS"            # KV 命名空间标识，代码中引用
# id = "xxxxxxxx"                 # 部署后自动生成，需更新
# preview_id = "xxxxxxxx"         # 预览环境 ID，部署后自动生成
```

> KV 命名空间的 `id` 和 `preview_id` 在首次部署后由 Cloudflare 自动生成，部署后会自动写入文件。

#### 获取 Cloudflare 凭证

| 凭证 | 获取方式 |
|------|----------|
| Account ID | Cloudflare Dashboard 右侧边栏底部 |
| API Token | [Dashboard API Tokens](https://dash.cloudflare.com/profile/api-tokens) → 创建 "Edit Cloudflare Workers" 模板 |

#### 配置 GitHub Secrets

仓库 Settings → Secrets and variables → Actions 中添加：

| Secret Name | 说明 |
|-------------|------|
| `CLOUDFLARE_API_TOKEN` | API Token |
| `CLOUDFLARE_ACCOUNT_ID` | Account ID |
| `CLOUDFLARE_PROJECT_NAME` | wrangler.toml 中的 name |

#### 自动部署

push 到 `master` 分支后自动触发：
```
npm ci → npm run build → Deploy to Cloudflare Pages
```

手动触发：GitHub → Actions → "Deploy Astro site to Cloudflare Pages" → Run workflow

### 3. 分支说明

---

## 链接

- GitHub博客：[http://barryliu.github.io](http://barryliu.github.io)
- GitHub网站：[https://github.com/barryLiu](https://github.com/barryLiu)
- Coding：[https://coding.net/u/BarryLiu](https://coding.net/u/BarryLiu)
- CSDN：[http://blog.csdn.net/github_33764133](http://blog.csdn.net/github_33764133)