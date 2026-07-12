# Header Motion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为全站 Header 增加克制流光、水族呼吸、共享导航高亮和滚动紧凑状态，同时保留现有主题、语言、搜索和移动菜单行为。

**Architecture:** 主要在 `CyberNav.astro` 内完成结构、样式和渐进增强脚本，滚动脚本只负责切换 `data-compact` 状态，共享高亮脚本负责测量当前链接并写入 CSS 自定义属性。测试使用现有 Node 静态契约测试先锁定结构、可访问性、减少动态效果和性能约束，再实现最小代码。

**Tech Stack:** Astro、TypeScript 浏览器脚本、CSS transitions/keyframes、Node `node:test`

---

## 文件职责

- `tests/interactive-features.test.mjs`：增加 Header 动效的静态行为契约，防止后续移除滚动状态、共享高亮、减少动态效果或移动菜单过渡。
- `src/components/CyberNav.astro`：维护 Header 标记、动效样式、滚动状态和共享高亮交互。
- `src/styles/tokens.css`：仅在深浅主题确实需要不同动效色值时增加 Header 专用变量。

### Task 1: 锁定 Header 动效行为契约

**Files:**
- Modify: `tests/interactive-features.test.mjs`
- Test: `tests/interactive-features.test.mjs`

- [ ] **Step 1: 写入失败测试**

在 `interactive site features` suite 中增加两个测试：

```js
it('adds a compact scroll state and shared desktop navigation highlight', () => {
  const nav = read('src/components/CyberNav.astro');

  assert.match(nav, /data-nav-shell/);
  assert.match(nav, /data-nav-links/);
  assert.match(nav, /data-nav-highlight/);
  assert.match(nav, /data-compact/);
  assert.match(nav, /window\.scrollY\s*>\s*40/);
  assert.match(nav, /requestAnimationFrame/);
  assert.match(nav, /--nav-highlight-x/);
  assert.match(nav, /--nav-highlight-width/);
});

it('keeps header motion accessible and mobile navigation progressively enhanced', () => {
  const nav = read('src/components/CyberNav.astro');

  assert.match(nav, /:focus-visible/);
  assert.match(nav, /prefers-reduced-motion:\s*reduce/);
  assert.match(nav, /details\[open\]/);
  assert.match(nav, /aria-current/);
  assert.match(nav, /passive:\s*true/);
});
```

- [ ] **Step 2: 运行定向测试并确认失败**

Run: `node --test tests/interactive-features.test.mjs`

Expected: FAIL，失败原因是 `CyberNav.astro` 尚未包含 `data-nav-shell`、共享高亮层和紧凑滚动脚本。

- [ ] **Step 3: 提交测试基线**

```bash
git add tests/interactive-features.test.mjs
git commit -m "测试 Header 动效行为"
```

### Task 2: 实现桌面 Header 结构和视觉动效

**Files:**
- Modify: `src/components/CyberNav.astro`
- Modify when required: `src/styles/tokens.css`
- Test: `tests/interactive-features.test.mjs`

- [ ] **Step 1: 增加渐进增强标记**

为 Header、导航链接容器和链接增加稳定标记，并插入共享高亮层：

```astro
<header class="site-header" data-nav-shell>
  <nav class="nav nav-panel container" ...>
    <CyberLogo />
    <div class="desktop-links" data-nav-links>
      <span class="nav-highlight" data-nav-highlight aria-hidden="true"></span>
      {site.nav.map((item) => (
        <a
          href={item.href}
          data-nav-link
          data-i18n-zh={item.label}
          data-i18n-en={item.labelEn}
        >
          {item.label}
        </a>
      ))}
    </div>
```

构建时根据 `Astro.url.pathname` 为当前页面对应链接输出 `aria-current="page"`。首页仅匹配 `/`，其他导航按路径前缀匹配，避免首页链接错误匹配全部页面。

- [ ] **Step 2: 增加首次进入、流光、呼吸和共享高亮 CSS**

CSS 使用以下边界：

```css
.site-header {
  animation: nav-enter 500ms cubic-bezier(0.22, 1, 0.36, 1) both;
}

.nav-panel::before {
  pointer-events: none;
  background: linear-gradient(90deg, transparent, rgb(40 247 255 / 70%), transparent);
  animation: nav-border-scan 8s ease-in-out infinite;
}

.desktop-links {
  position: relative;
}

.nav-highlight {
  position: absolute;
  width: var(--nav-highlight-width, 0px);
  transform: translateX(var(--nav-highlight-x, 0px));
  opacity: var(--nav-highlight-opacity, 0);
  transition: transform 220ms ease, width 220ms ease, opacity 160ms ease;
}

.desktop-links a,
.desktop-actions :global(button),
.desktop-actions .icon-link,
.desktop-actions .contact {
  position: relative;
  z-index: 1;
}
```

面板只做光晕透明度呼吸，不给整个导航持续上下位移。操作控件在 `:hover` 和 `:focus-visible` 时最多上移 2px。

- [ ] **Step 3: 增加滚动紧凑状态 CSS**

```css
.site-header[data-compact='true'] {
  padding-top: 8px;
}

.site-header[data-compact='true'] .nav {
  min-height: 62px;
}

.site-header[data-compact='true'] .nav-panel {
  border-radius: 16px;
  padding-block: 7px;
  background: var(--nav-background-compact, var(--nav-background));
  box-shadow: var(--nav-shadow-compact, var(--nav-shadow)), var(--shadow-glow);
}
```

- [ ] **Step 4: 运行定向测试确认结构仍有脚本项失败**

Run: `node --test tests/interactive-features.test.mjs`

Expected: 共享高亮和紧凑状态的结构断言通过；滚动脚本相关断言仍失败。

### Task 3: 实现滚动状态和共享高亮脚本

**Files:**
- Modify: `src/components/CyberNav.astro`
- Test: `tests/interactive-features.test.mjs`

- [ ] **Step 1: 添加可重复初始化的 Header 脚本**

脚本实现以下最小行为：

```js
const setupCyberNav = () => {
  document.querySelectorAll('[data-nav-shell]').forEach((shell) => {
    if (!(shell instanceof HTMLElement) || shell.dataset.navReady === 'true') return;
    shell.dataset.navReady = 'true';

    let scrollFrame = 0;
    const updateCompactState = () => {
      scrollFrame = 0;
      shell.dataset.compact = String(window.scrollY > 40);
    };
    const requestCompactUpdate = () => {
      if (scrollFrame) return;
      scrollFrame = requestAnimationFrame(updateCompactState);
    };

    updateCompactState();
    window.addEventListener('scroll', requestCompactUpdate, { passive: true });
  });
};

setupCyberNav();
document.addEventListener('astro:page-load', setupCyberNav);
```

- [ ] **Step 2: 在同一初始化边界内实现高亮测量**

高亮测量使用容器和链接的 `getBoundingClientRect()`，写入：

```js
links.style.setProperty('--nav-highlight-x', `${linkRect.left - linksRect.left}px`);
links.style.setProperty('--nav-highlight-width', `${linkRect.width}px`);
links.style.setProperty('--nav-highlight-opacity', '1');
```

监听 `pointerenter`、`focusin`、`pointerleave`、`focusout` 和 `resize`。离开时恢复到 `[aria-current="page"]`；没有当前链接时把透明度设为 `0`。语言切换会改变链接宽度，因此同时监听站点已有的语言变更事件；如果没有可靠事件，则使用一次 `MutationObserver` 观察链接文本变化并重新测量。

- [ ] **Step 3: 运行定向测试确认通过**

Run: `node --test tests/interactive-features.test.mjs`

Expected: PASS，Header 新增契约全部通过，原有交互功能测试不回归。

- [ ] **Step 4: 提交 Header 桌面动效**

```bash
git add src/components/CyberNav.astro src/styles/tokens.css tests/interactive-features.test.mjs
git commit -m "优化 Header 悬浮动效"
```

仅在 `tokens.css` 实际发生变化时暂存该文件。

### Task 4: 完成移动端和减少动态效果支持

**Files:**
- Modify: `src/components/CyberNav.astro`
- Test: `tests/interactive-features.test.mjs`

- [ ] **Step 1: 实现移动菜单过渡**

保留 `details` / `summary`，增加展开状态样式：

```css
.mobile-panel {
  transform: translateY(-8px) scale(0.98);
  transform-origin: top right;
  opacity: 0;
  transition: opacity 180ms ease, transform 220ms ease;
}

.mobile-menu[open] .mobile-panel {
  transform: translateY(0) scale(1);
  opacity: 1;
}

.mobile-menu[open] summary span:nth-child(1) {
  transform: translateY(4px) rotate(45deg);
}

.mobile-menu[open] summary span:nth-child(2) {
  opacity: 0;
}

.mobile-menu[open] summary span:nth-child(3) {
  transform: translateY(-4px) rotate(-45deg);
}
```

- [ ] **Step 2: 实现减少动态效果覆盖**

```css
@media (prefers-reduced-motion: reduce) {
  .site-header,
  .nav-panel::before,
  .nav-panel::after {
    animation: none !important;
  }

  .site-header,
  .nav,
  .nav-panel,
  .nav-highlight,
  .desktop-links a,
  .desktop-actions :global(*),
  .mobile-panel,
  summary span {
    scroll-behavior: auto;
    transition-duration: 0.01ms !important;
  }
}
```

- [ ] **Step 3: 运行完整自动化验证**

Run: `npm run test`

Expected: PASS，所有 Node 测试通过。

Run: `npm run build`

Expected: PASS，Astro 构建成功且无新增错误。

### Task 5: 浏览器视觉与交互验证

**Files:**
- Verify: `src/components/CyberNav.astro`
- Verify: `src/styles/tokens.css`

- [ ] **Step 1: 启动或复用本地 Astro 服务**

先检查 `http://localhost:4321` 是否已响应；未运行时执行：

Run: `npm run dev`

Expected: Astro dev server 在 `http://localhost:4321` 可访问。

- [ ] **Step 2: 验证桌面端关键页面**

依次查看 `/`、`/ai-notes/`、`/knowledge/`、`/about/`、`/archive/` 和任意 `/posts/.../` 页面，确认：

- Header 首次进入自然淡入。
- 滚动超过 40px 后紧凑，上滚回顶部后恢复。
- 导航共享高亮跟随鼠标和键盘焦点，并回到当前页面链接。
- 深色和浅色主题下边框、文字及光晕对比正常。
- 搜索、主题、语言、RSS、GitHub 和联系入口仍可操作。

- [ ] **Step 3: 验证移动端与减少动态效果**

在窄屏下确认桌面导航隐藏、菜单按钮变形、菜单面板平滑展开，且链接可以正常访问。在模拟 `prefers-reduced-motion: reduce` 后确认流光、呼吸和位移动画停止。

- [ ] **Step 4: 检查最终 diff 和工作区边界**

Run: `git diff --check`

Expected: 无空白错误。

Run: `git status --short`

Expected: Header 相关改动可与工作区既有未提交改动清晰区分；不包含 `dist/`、`.astro/`、`.superpowers/` 或复制生成的静态资源。

- [ ] **Step 5: 提交移动端与无障碍完善**

```bash
git add src/components/CyberNav.astro tests/interactive-features.test.mjs
git commit -m "完善 Header 移动端动效"
```
