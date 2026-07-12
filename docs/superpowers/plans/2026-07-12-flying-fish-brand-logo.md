# Flying Fish Brand Logo Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 制作一套胸鳍从鱼身侧面展开、跃出海面的飞鱼 SVG 品牌资源，并替换网站导航、页脚和 favicon 中的旧标志。

**Architecture:** `public/assets/brand/` 保存独立图形、完整横版和 favicon 三份静态 SVG；`CyberLogo.astro` 内联同源矢量路径，保留现有多语言文字和可访问性。新增品牌资源契约测试，锁定资源存在、透明背景、侧胸鳍语义、小尺寸简化和站点引用关系。

**Tech Stack:** Astro 5、TypeScript、SVG、scoped CSS、Node.js 内置测试。

---

### Task 1: 用失败测试锁定品牌资源契约

**Files:**
- Create: `tests/brand-assets.test.mjs`
- Test: `tests/brand-assets.test.mjs`

- [ ] **Step 1: 写入品牌资源失败测试**

```js
import assert from 'node:assert/strict';
import { existsSync, readFileSync } from 'node:fs';
import { describe, it } from 'node:test';

function read(path) {
  const url = new URL(`../${path}`, import.meta.url);
  assert.ok(existsSync(url), `${path} should exist`);
  return readFileSync(url, 'utf8');
}

describe('flying fish brand assets', () => {
  it('ships a consistent transparent SVG logo family', () => {
    const mark = read('public/assets/brand/logo-mark.svg');
    const lockup = read('public/assets/brand/logo.svg');
    const favicon = read('public/assets/brand/favicon.svg');

    assert.match(mark, /viewBox="0 0 120 84"/);
    assert.match(mark, /id="fish-body-gradient"/);
    assert.match(mark, /data-part="pectoral-fin"/);
    assert.match(mark, /data-part="water-arc"/);
    assert.doesNotMatch(mark, /<rect[^>]+(?:width="120"|width="100%")/);

    assert.match(lockup, /viewBox="0 0 360 96"/);
    assert.match(lockup, /想飞的鱼/);
    assert.match(lockup, /Flying Fish Lab/);
    assert.match(lockup, /data-part="pectoral-fin"/);
    assert.doesNotMatch(lockup, /<rect[^>]+(?:width="360"|width="100%")/);

    assert.match(favicon, /viewBox="0 0 64 64"/);
    assert.match(favicon, /data-part="pectoral-fin"/);
    assert.match(favicon, /data-part="water-arc"/);
    assert.doesNotMatch(favicon, /data-part="fin-ray"/);
  });

  it('uses the new mark in the reusable site logo and favicon link', () => {
    const logo = read('src/components/CyberLogo.astro');
    const layout = read('src/layouts/BaseLayout.astro');

    assert.match(logo, /viewBox="0 0 120 84"/);
    assert.match(logo, /class="pectoral-fin"/);
    assert.match(logo, /class="water-arc"/);
    assert.match(logo, /data-i18n-zh="想飞的鱼"/);
    assert.match(layout, /href="\/assets\/brand\/favicon\.svg"/);
  });
});
```

- [ ] **Step 2: 运行定向测试并确认失败**

Run: `node --test tests/brand-assets.test.mjs`

Expected: FAIL，首个失败项为旧 `logo-mark.svg` 的 `viewBox="0 0 88 56"` 与新契约不匹配。

- [ ] **Step 3: 提交失败测试**

```bash
git add tests/brand-assets.test.mjs
git commit -m "补充飞鱼品牌资源测试"
```

### Task 2: 创建三份飞鱼品牌 SVG 资源

**Files:**
- Modify: `public/assets/brand/logo-mark.svg`
- Modify: `public/assets/brand/logo.svg`
- Modify: `public/assets/brand/favicon.svg`
- Test: `tests/brand-assets.test.mjs`

- [ ] **Step 1: 重绘透明背景独立图形**

在 `logo-mark.svg` 使用 `120 × 84` viewBox。鱼体沿右上方向倾斜，深青轮廓包住青蓝渐变身体；胸鳍路径从靠近头部后方的鱼身侧面起始，向左后方展开为浅扇形，并标记 `data-part="pectoral-fin"`。添加三条细鳍条、分叉尾鳍、眼睛、海面弧线和两个水滴，不添加背景矩形。

核心结构：

```svg
<g transform="rotate(-12 62 43)">
  <path data-part="tail" d="M31 44 12 29l5 19-10 14 24-7Z" />
  <path data-part="fish-body" d="M24 47C42 27 77 24 105 39c-13 19-50 31-81 17-4-2-4-6 0-9Z" />
  <path data-part="pectoral-fin" d="M67 42C53 25 33 18 19 22c10 8 20 18 27 33 8 1 16-4 21-13Z" />
  <path data-part="pectoral-fin-lower" d="M62 52C50 64 38 70 26 69c8-7 15-13 20-22Z" />
</g>
<path data-part="water-arc" d="M12 72C39 61 76 60 108 72" />
```

- [ ] **Step 2: 创建横向完整标志**

`logo.svg` 使用 `360 × 96` viewBox，在左侧以约 104 × 76 的尺寸复用独立图形结构，右侧保留两行文字。背景透明，中文标题使用深青色，英文副标题使用青蓝色，并在深色主题外部使用时仍保持轮廓清晰。

- [ ] **Step 3: 创建 favicon 简化版本**

`favicon.svg` 使用 `64 × 64` viewBox，只保留鱼体、分叉尾鳍、一个侧胸鳍、眼睛和一条海面弧线。删除鳍条、水滴与细小高光，主要轮廓宽度不小于 2.6px。

- [ ] **Step 4: 运行品牌资源测试**

Run: `node --test tests/brand-assets.test.mjs`

Expected: 资源契约测试中的 SVG 资源用例 PASS；组件用例仍因 `CyberLogo.astro` 使用旧 viewBox 而 FAIL。

### Task 3: 替换导航和页脚复用 Logo

**Files:**
- Modify: `src/components/CyberLogo.astro`
- Test: `tests/brand-assets.test.mjs`

- [ ] **Step 1: 用新标志替换旧内联 SVG**

将 `CyberLogo.astro` 的 SVG 改为 `viewBox="0 0 120 84"`，内联与 `logo-mark.svg` 对应的鱼体、侧胸鳍、尾鳍、眼睛、海面弧线和水滴。渐变 ID 添加组件专用前缀，避免页面中导航和页脚重复渲染时发生冲突。

```astro
<svg viewBox="0 0 120 84" role="img" aria-hidden="true">
  <defs>
    <linearGradient id="nav-fish-body-gradient" x1="20" y1="60" x2="104" y2="30" gradientUnits="userSpaceOnUse">
      <stop stop-color="#21c7dc" />
      <stop offset="1" stop-color="#5479e8" />
    </linearGradient>
    <linearGradient id="nav-fin-gradient" x1="24" y1="18" x2="67" y2="55" gradientUnits="userSpaceOnUse">
      <stop stop-color="#8a78ee" stop-opacity=".9" />
      <stop offset="1" stop-color="#36dbe7" stop-opacity=".42" />
    </linearGradient>
  </defs>
  <path class="water-arc" d="M12 72C39 61 76 60 108 72" />
  <circle class="water-drop" cx="29" cy="66" r="2" />
  <circle class="water-drop water-drop-small" cx="96" cy="65" r="1.4" />
  <g transform="rotate(-12 62 43)">
    <path class="tail" d="M31 46 12 30l5 18-10 14 25-7Z" />
    <path class="fish-body" d="M25 46C42 28 72 24 104 38c-10 12-30 23-51 26-12 2-23 0-31-4-5-3-5-9 3-14Z" />
    <path class="pectoral-fin" d="M68 43C57 29 39 19 20 22c12 8 21 19 27 34 9 0 17-5 21-13Z" />
    <path class="pectoral-fin lower-fin" d="M61 54C50 64 39 69 27 68c8-7 15-14 20-22 6 2 11 5 14 8Z" />
    <path class="fin-ray" d="M61 42C48 34 37 29 26 26M58 47C45 40 36 35 29 30M54 51C43 46 36 41 32 36" />
    <path class="body-highlight" d="M40 56c18 2 39-5 54-15" />
    <circle class="eye-ring" cx="91" cy="39" r="4" />
    <circle class="eye" cx="92" cy="38" r="1.7" />
  </g>
</svg>
```

- [ ] **Step 2: 调整小尺寸样式**

保持导航布局不变，将图形显示尺寸调整为 `52px × 36px`，轮廓使用 SVG 自带颜色；只保留柔和青色 drop-shadow。紧凑页脚继续隐藏英文副标题。

```css
svg {
  width: 52px;
  height: 36px;
  overflow: visible;
  filter: drop-shadow(0 4px 10px rgb(21 183 207 / 24%));
}
```

- [ ] **Step 3: 运行定向测试并确认通过**

Run: `node --test tests/brand-assets.test.mjs`

Expected: 2 tests PASS，0 FAIL。

- [ ] **Step 4: 提交 Logo 资源和组件**

```bash
git add public/assets/brand/logo-mark.svg public/assets/brand/logo.svg public/assets/brand/favicon.svg src/components/CyberLogo.astro
git commit -m "替换跃水飞鱼品牌标志"
```

### Task 4: 全量验证和页面检查

**Files:**
- Verify: `tests/brand-assets.test.mjs`
- Verify: `src/components/CyberLogo.astro`
- Verify: `public/assets/brand/*.svg`

- [ ] **Step 1: 运行全部自动测试**

Run: `npm run test`

Expected: 所有 Node.js 测试通过，0 FAIL。

- [ ] **Step 2: 运行生产构建**

Run: `npm run build`

Expected: Astro 构建成功，命令退出码为 0。

- [ ] **Step 3: 验证关键路由可访问**

请求 `/`、`/ai-notes/`、`/knowledge/`、`/about/`、`/archive/`、一篇 `/posts/.../` 和 `/rss.xml`，每个请求都应返回 200。

- [ ] **Step 4: 浏览器检查实际效果**

在桌面宽度下检查首页导航和页脚，在浅色、深色主题各截图一次；确认鱼头朝右上，胸鳍从鱼身侧面展开，海面元素简洁，没有竖直船帆感。缩小视口后确认 Logo 不挤压移动菜单，并确认浏览器标签使用新 favicon。

- [ ] **Step 5: 检查最终变更范围**

Run: `git status --short && git diff --check`

Expected: 本次范围仅包含品牌测试、三份品牌 SVG 和 `CyberLogo.astro`；仓库原有的其他未提交修改保持不变。
