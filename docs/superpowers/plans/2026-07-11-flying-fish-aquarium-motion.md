# Flying Fish Aquarium Motion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将首页右侧水族馆重做为无网格、无圆形节点的动态飞鱼场景，并通过完整循环表现“深海蓄力、展翼跃升、滑翔回游”。

**Architecture:** 保持 Hero 左侧和现有两栏布局不变，只替换 `CyberHero.astro` 中水族馆内部结构与 scoped CSS。场景由分层 SVG 飞鱼、CSS 渐变光雾、气泡、尾迹粒子和短暂出现的技术文字组成；所有连续动画使用 CSS keyframes，并为移动端和 `prefers-reduced-motion` 提供明确降级。

**Tech Stack:** Astro 5、TypeScript 项目结构、HTML/SVG、scoped CSS、Node.js 内置测试。

---

## 文件结构

- `src/components/CyberHero.astro`：水族馆语义结构、SVG 飞鱼、粒子和全部 scoped 动画样式。
- `tests/interactive-features.test.mjs`：静态契约测试，确保旧圆形节点/轨道被移除、关键动画和 reduced-motion 降级持续存在。

不新增动画依赖，不修改左侧 Hero 文案，不把本次视觉逻辑拆到全局样式或运行时脚本中。

### Task 1: 用失败测试锁定动态水族馆结构

**Files:**
- Modify: `tests/interactive-features.test.mjs`
- Test: `tests/interactive-features.test.mjs`

- [ ] **Step 1: 在首页结构测试之后添加动态水族馆契约测试**

```js
  it('renders a narrative flying-fish motion scene without radar ornaments', () => {
    const hero = read('src/components/CyberHero.astro');

    assert.match(hero, /class="aquarium-scene"/);
    assert.match(hero, /class="flying-fish"/);
    assert.match(hero, /class="fish-wing/);
    assert.match(hero, /class="trail-particle/);
    assert.match(hero, /class="tech-signal/);
    assert.match(hero, /@keyframes fish-flight/);
    assert.match(hero, /@keyframes wing-glide/);
    assert.match(hero, /@keyframes trail-drift/);
    assert.match(hero, /prefers-reduced-motion:\s*reduce/);
    assert.doesNotMatch(hero, /class="ring/);
    assert.doesNotMatch(hero, /class="node/);
    assert.doesNotMatch(hero, /class="hud"/);
    assert.doesNotMatch(hero, /var\(--color-lime\)/);
  });
```

- [ ] **Step 2: 运行定向测试并确认失败**

Run: `node --test --test-name-pattern="narrative flying-fish" tests/interactive-features.test.mjs`

Expected: FAIL，首个失败信息包含 `class="aquarium-scene"` 未匹配。

- [ ] **Step 3: 提交失败测试**

```bash
git add tests/interactive-features.test.mjs
git commit -m "测试动态飞鱼水族馆结构"
```

### Task 2: 替换旧水族馆为分层动态场景

**Files:**
- Modify: `src/components/CyberHero.astro:39-58`
- Modify: `src/components/CyberHero.astro:167-348`
- Test: `tests/interactive-features.test.mjs`

- [ ] **Step 1: 用无轨道、无节点结构替换 `.aquarium` 内部标记**

水族馆根节点保留现有可访问名称，在内部使用下面的明确分层。装饰节点必须带 `aria-hidden="true"`，飞鱼 SVG 保留可访问标题：

```astro
    <div class="aquarium" aria-label="Flying fish holographic aquarium">
      <div class="aquarium-scene" aria-hidden="true">
        <span class="water-light water-light-a"></span>
        <span class="water-light water-light-b"></span>
        <span class="bubble bubble-a"></span>
        <span class="bubble bubble-b"></span>
        <span class="bubble bubble-c"></span>

        <div class="fish-flight-path">
          <svg class="flying-fish" viewBox="0 0 420 260" role="img" aria-labelledby="flying-fish-title">
            <title id="flying-fish-title">一条展开鱼翼、从深海飞向天空的鱼</title>
            <defs>
              <linearGradient id="fish-body-gradient" x1="0" y1="0" x2="1" y2="1">
                <stop offset="0" stop-color="#d9fbff" />
                <stop offset="0.52" stop-color="#55d9ee" />
                <stop offset="1" stop-color="#6677dc" />
              </linearGradient>
              <linearGradient id="fish-wing-gradient" x1="0" y1="1" x2="1" y2="0">
                <stop offset="0" stop-color="#47dce9" stop-opacity=".2" />
                <stop offset=".58" stop-color="#8c78e8" stop-opacity=".72" />
                <stop offset="1" stop-color="#ef78c9" stop-opacity=".9" />
              </linearGradient>
            </defs>
            <g class="fish-wing fish-wing-back">
              <path d="M143 145C181 49 286 25 361 62C290 76 245 117 214 187C190 165 169 151 143 145Z" />
            </g>
            <g class="fish-tail">
              <path d="M309 153L389 96L365 152L395 203L306 178Z" />
            </g>
            <path class="fish-body" d="M49 158C111 103 218 101 320 157C241 218 121 219 49 158Z" />
            <path class="fish-belly" d="M75 170C143 198 227 197 289 169" />
            <g class="fish-wing fish-wing-front">
              <path d="M139 157C187 89 278 79 340 109C282 119 235 151 196 210C181 185 162 169 139 157Z" />
            </g>
            <circle class="fish-eye" cx="119" cy="146" r="7" />
            <circle class="fish-eye-glint" cx="121" cy="143" r="2" />
          </svg>
        </div>

        <span class="trail-particle trail-particle-a"></span>
        <span class="trail-particle trail-particle-b"></span>
        <span class="trail-particle trail-particle-c"></span>
        <span class="trail-particle trail-particle-d"></span>
        <span class="tech-signal tech-signal-rag">RAG CORE</span>
        <span class="tech-signal tech-signal-agent">AGENT OPS</span>
        <span class="tech-signal tech-signal-mlops">MLOPS</span>
        <span class="tech-signal tech-signal-code">CODE TOOLS</span>
      </div>
    </div>
```

- [ ] **Step 2: 替换水族馆样式，建立无框深海背景和 12 秒主循环**

实现以下关键规则；不要保留 `.ring`、`.node`、`.hud` 或 `background-size: 44px 44px`：

```css
  .aquarium {
    position: relative;
    min-height: 650px;
    overflow: hidden;
    border: 1px solid rgb(69 212 235 / 18%);
    border-radius: 30px;
    background:
      radial-gradient(circle at 68% 18%, rgb(141 92 226 / 28%), transparent 34%),
      radial-gradient(circle at 24% 76%, rgb(37 190 218 / 24%), transparent 38%),
      linear-gradient(155deg, #06162a 0%, #092b45 48%, #211b46 100%);
    box-shadow: inset 0 -80px 120px rgb(2 10 24 / 35%), 0 24px 70px rgb(13 64 94 / 22%);
    isolation: isolate;
  }

  .aquarium-scene {
    position: absolute;
    inset: 0;
    overflow: hidden;
  }

  .fish-flight-path {
    position: absolute;
    left: 5%;
    bottom: 4%;
    width: 76%;
    animation: fish-flight 12s cubic-bezier(.42, 0, .2, 1) infinite;
    will-change: transform, opacity;
  }

  .flying-fish {
    display: block;
    width: 100%;
    overflow: visible;
    filter: drop-shadow(0 18px 20px rgb(1 12 27 / 32%)) drop-shadow(0 0 22px rgb(69 218 236 / 26%));
  }

  .fish-body {
    fill: url(#fish-body-gradient);
    stroke: rgb(220 251 255 / 84%);
    stroke-width: 3;
  }

  .fish-wing {
    transform-box: fill-box;
    transform-origin: 18% 72%;
    animation: wing-glide 2.4s ease-in-out infinite;
  }

  .fish-wing path,
  .fish-tail path {
    fill: url(#fish-wing-gradient);
    stroke: rgb(159 229 244 / 70%);
    stroke-width: 3;
  }

  .fish-tail {
    transform-box: fill-box;
    transform-origin: left center;
    animation: tail-swim 1.1s ease-in-out infinite;
  }

  @keyframes fish-flight {
    0% { opacity: 0; transform: translate(-22%, 18%) rotate(-8deg) scale(.72); }
    8% { opacity: 1; }
    26% { transform: translate(2%, 5%) rotate(-3deg) scale(.82); }
    34% { transform: translate(-1%, 8%) rotate(-7deg) scale(.84); }
    58% { opacity: 1; transform: translate(30%, -43%) rotate(-19deg) scale(1.02); }
    78% { opacity: 1; transform: translate(48%, -58%) rotate(-6deg) scale(.96); }
    92%, 100% { opacity: 0; transform: translate(74%, -48%) rotate(4deg) scale(.82); }
  }

  @keyframes wing-glide {
    0%, 100% { transform: rotate(-3deg) scaleY(.92); }
    50% { transform: rotate(5deg) scaleY(1.06); }
  }

  @keyframes tail-swim {
    0%, 100% { transform: rotate(-5deg); }
    50% { transform: rotate(7deg); }
  }
```

- [ ] **Step 3: 添加异步环境运动、粒子尾迹和技术文字淡入淡出**

```css
  .water-light {
    position: absolute;
    width: 72%;
    height: 54%;
    border-radius: 50%;
    background: radial-gradient(ellipse, rgb(76 218 235 / 18%), transparent 68%);
    filter: blur(22px);
    animation: current-drift 9s ease-in-out infinite alternate;
  }

  .water-light-a { left: -18%; bottom: -8%; }
  .water-light-b { top: -16%; right: -24%; animation-duration: 13s; animation-delay: -4s; }

  .bubble,
  .trail-particle {
    position: absolute;
    width: 5px;
    height: 5px;
    border-radius: 50%;
    background: rgb(174 242 255 / 72%);
    box-shadow: 0 0 12px rgb(83 220 239 / 68%);
  }

  .trail-particle { animation: trail-drift 12s ease-out infinite; }

  .tech-signal {
    position: absolute;
    color: rgb(193 239 248 / 64%);
    font-size: .68rem;
    font-weight: 800;
    letter-spacing: .16em;
    opacity: 0;
    text-shadow: 0 0 14px rgb(87 218 239 / 42%);
    animation: signal-rise 12s ease-out infinite;
  }

  @keyframes current-drift {
    from { transform: translate3d(-4%, 2%, 0) scale(.92); opacity: .55; }
    to { transform: translate3d(9%, -6%, 0) scale(1.12); opacity: .9; }
  }

  @keyframes trail-drift {
    0%, 35% { opacity: 0; transform: translate3d(0, 0, 0) scale(.4); }
    48% { opacity: .9; }
    72%, 100% { opacity: 0; transform: translate3d(-90px, 48px, 0) scale(1.5); }
  }

  @keyframes signal-rise {
    0%, 45% { opacity: 0; transform: translate3d(0, 16px, 0); }
    55%, 68% { opacity: .72; }
    82%, 100% { opacity: 0; transform: translate3d(18px, -20px, 0); }
  }
```

为各气泡、粒子和技术文字设置不同的 `left`、`top`、`animation-delay`，四个技术文字至少相差 `0.7s`，避免同时出现。

- [ ] **Step 4: 运行动态场景定向测试并确认通过**

Run: `node --test --test-name-pattern="narrative flying-fish" tests/interactive-features.test.mjs`

Expected: PASS，1 个匹配测试通过，其余测试因 name pattern 跳过。

- [ ] **Step 5: 提交桌面端动态场景**

```bash
git add src/components/CyberHero.astro tests/interactive-features.test.mjs
git commit -m "重做首页动态飞鱼水族馆"
```

### Task 3: 完成响应式和减少动态降级

**Files:**
- Modify: `src/components/CyberHero.astro`
- Test: `tests/interactive-features.test.mjs`

- [ ] **Step 1: 添加移动端尺寸和信息降级**

```css
  @media (max-width: 980px) {
    .aquarium { min-height: 500px; }
    .fish-flight-path { width: 68%; }
  }

  @media (max-width: 560px) {
    .aquarium { min-height: 360px; }
    .fish-flight-path { left: 0; bottom: 0; width: 82%; }
    .tech-signal-mlops,
    .tech-signal-code,
    .bubble-c,
    .trail-particle-d { display: none; }
  }
```

- [ ] **Step 2: 添加 `prefers-reduced-motion` 静态终态**

```css
  @media (prefers-reduced-motion: reduce) {
    .fish-flight-path {
      opacity: 1;
      transform: translate(18%, -18%) rotate(-10deg) scale(.92);
    }

    .fish-flight-path,
    .fish-wing,
    .fish-tail,
    .water-light,
    .bubble,
    .trail-particle,
    .tech-signal {
      animation: none !important;
    }

    .trail-particle,
    .tech-signal { display: none; }
  }
```

- [ ] **Step 3: 运行完整测试**

Run: `npm run test`

Expected: 所有 Node 内置测试通过，无失败或未处理异常。

- [ ] **Step 4: 提交响应式和无障碍降级**

```bash
git add src/components/CyberHero.astro tests/interactive-features.test.mjs
git commit -m "完善飞鱼动画响应式降级"
```

### Task 4: 构建和浏览器视觉验证

**Files:**
- Verify: `src/components/CyberHero.astro`

- [ ] **Step 1: 运行生产构建**

Run: `npm run build`

Expected: Astro 构建成功，`dist/` 生成完成，无 Content Collections 或 CSS 编译错误。

- [ ] **Step 2: 在现有本地站点刷新首页并观察完整循环**

Browser URL: `http://localhost:4321/`

检查至少 14 秒，确认飞鱼从左下游入、蓄力、展翼向右上跃升、滑翔淡出并回到起点；不能只检查单帧截图。

- [ ] **Step 3: 检查桌面端视觉约束**

在约 `1625 × 1224` 视口确认：没有绿色圆球、同心轨道、网格、HUD 和密集边框；技术文字从尾迹中错峰出现；飞鱼始终是第一视觉焦点且不被裁切。

- [ ] **Step 4: 检查移动端布局**

将视口调整为约 `390 × 844`，确认水族馆没有横向溢出，鱼的主要运动轨迹可见，次要技术文字和粒子已减少。

- [ ] **Step 5: 检查减少动态模式**

在浏览器模拟 `prefers-reduced-motion: reduce`，确认主位移、鱼翼、鱼尾、光雾、气泡和粒子动画停止，飞鱼以清晰静态终态展示。

- [ ] **Step 6: 检查最终差异范围**

Run: `git diff --check && git status --short`

Expected: `git diff --check` 无输出；本任务只新增或修改计划中列出的文件，现有其他未提交文件保持不变。
