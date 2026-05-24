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
3. clone 到本地，在 `src/content/posts` 创建正式文章，在 `src/content/drafts` 保存草稿
4. 修改 CNAME 或删掉使用默认域名
5. 修改 `src/data/site.ts` 配置项
6. 如需启用 GitHub OAuth 收藏功能，配置环境变量（见下方"GitHub OAuth 收藏功能"章节）

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

#### 环境变量（Cloudflare Pages Settings）

在 Cloudflare Pages → Settings → Environment Variables 中配置：

| Variable | 说明 | 获取方式 |
|----------|------|----------|
| `AUTH_COOKIE_SECRET` | Cookie 签名密钥 | `openssl rand -base64 32` 生成 |
| `GITHUB_OAUTH_CLIENT_ID` | GitHub OAuth App Client ID | GitHub Developer Settings → 你的 OAuth App |
| `GITHUB_OAUTH_CLIENT_SECRET` | GitHub OAuth App Client Secret | GitHub Developer Settings → 你的 OAuth App → 生成 Client Secret |

**GitHub OAuth App 创建**：
1. https://github.com/settings/developers → New OAuth App
2. 填写：
   - Application name：任意
   - Homepage URL：`https://你的域名`
   - Authorization callback URL：`https://你的域名/api/auth/github/callback`
3. 创建后复制 Client ID 和 Client Secret 到 Cloudflare Pages

#### GitHub Secrets（CI/CD 部署用）

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

### 3. 功能开关

编辑 `src/data/site.ts` 中的 `features` 节点：

```ts
features: {
  githubOAuth: true,  // GitHub OAuth 收藏功能（默认 false）
},
```

| 开关 | 说明 | 依赖 |
|------|------|------|
| `githubOAuth` | 开启后显示收藏/查看收藏按钮，依赖 GitHub OAuth 环境变量 | 需配置 `AUTH_COOKIE_SECRET` + `GITHUB_OAUTH_CLIENT_ID` + `GITHUB_OAUTH_CLIENT_SECRET` |

---

## 链接

- GitHub博客：[http://barryliu.github.io](http://barryliu.github.io)
- GitHub网站：[https://github.com/barryLiu](https://github.com/barryLiu)
- Coding：[https://coding.net/u/BarryLiu](https://coding.net/u/BarryLiu)
- CSDN：[http://blog.csdn.net/github_33764133](http://blog.csdn.net/github_33764133)
