# Flying Fish Surface Flight Motion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将首页飞鱼动画升级为从深海冲破海面、镜头随鱼上升、以浅色赛博天空为主视觉，并让四个技术关键词持续围绕飞鱼旋转的完整循环。

**Architecture:** 在 `CyberHero.astro` 内把当前单层深海背景拆成可独立移动的天空、云层、海面和深海舞台；鱼、环绕关键词和局部光效放入同一个飞行容器。主循环使用统一的 14 秒时间轴，镜头舞台、飞鱼、水花和关键词使用匹配的关键帧时间点，但通过独立缓动形成跟随感。

**Tech Stack:** Astro 5、HTML/SVG、scoped CSS keyframes、Node.js 内置测试、浏览器 computed-style 动态采样。

---

### Task 1: 用失败测试锁定破水飞行和环绕关键词

**Files:**
- Modify: `tests/interactive-features.test.mjs`
- Test: `tests/interactive-features.test.mjs`

- [ ] **Step 1: 扩展动态水族馆测试契约**

在现有 `renders a narrative flying-fish motion scene without radar ornaments` 测试中加入：

```js
    assert.match(hero, /class="sky-stage"/);
    assert.match(hero, /class="ocean-stage"/);
    assert.match(hero, /class="sea-surface"/);
    assert.match(hero, /class="splash-burst/);
    assert.match(hero, /class="orbit-system"/);
    assert.match(hero, /class="orbit-keyword/);
    assert.match(hero, /@keyframes camera-rise/);
    assert.match(hero, /@keyframes surface-wave/);
    assert.match(hero, /@keyframes splash-break/);
    assert.match(hero, /@keyframes keyword-orbit/);
```

- [ ] **Step 2: 运行定向测试并确认失败**

Run: `node --test --test-name-pattern="narrative flying-fish" tests/interactive-features.test.mjs`

Expected: FAIL，首个失败项为 `class="sky-stage"` 未匹配。

### Task 2: 将背景拆成天空、海面和深海镜头舞台

**Files:**
- Modify: `src/components/CyberHero.astro`
- Test: `tests/interactive-features.test.mjs`

- [ ] **Step 1: 添加分层场景结构**

在 `.aquarium-scene` 中建立以下层级，原有气泡和水流移动到 `.ocean-stage`，新云层和扫描光放到 `.sky-stage`：

```astro
<div class="camera-stage" aria-hidden="true">
  <div class="sky-stage">
    <span class="cyber-sun"></span>
    <span class="cloud cloud-a"></span>
    <span class="cloud cloud-b"></span>
    <span class="cloud cloud-c"></span>
    <span class="sky-scan"></span>
  </div>
  <div class="sea-surface">
    <span class="surface-glow"></span>
    <span class="surface-wave surface-wave-a"></span>
    <span class="surface-wave surface-wave-b"></span>
    <span class="splash-burst splash-out"></span>
    <span class="splash-burst splash-in"></span>
    <span class="water-drop water-drop-a"></span>
    <span class="water-drop water-drop-b"></span>
    <span class="water-drop water-drop-c"></span>
  </div>
  <div class="ocean-stage"><!-- existing water lights, currents and bubbles --></div>
</div>
```

- [ ] **Step 2: 建立初始 58% 天空、42% 深海的画面**

```css
.camera-stage { position: absolute; inset: -44% 0 0; height: 144%; animation: camera-rise 14s ease-in-out infinite; }
.sky-stage { position: absolute; inset: 0 0 42%; background: linear-gradient(180deg, #f8fcff 0%, #dff5fb 58%, #9edceb 100%); }
.sea-surface { position: absolute; top: 58%; right: 0; left: 0; height: 9%; z-index: 3; }
.ocean-stage { position: absolute; top: 62%; right: 0; bottom: 0; left: 0; background: linear-gradient(180deg, #1684a5 0%, #073752 34%, #06162a 100%); }
```

- [ ] **Step 3: 添加镜头跟随关键帧**

```css
@keyframes camera-rise {
  0%, 28% { transform: translateY(30%); }
  42% { transform: translateY(12%); }
  58%, 74% { transform: translateY(0); }
  88% { transform: translateY(18%); }
  100% { transform: translateY(30%); }
}
```

飞鱼破水后海面必须随 `.camera-stage` 向下离开画面中部；天空飞翔阶段海面位于容器底部约 10% 至 20% 区域。

### Task 3: 实现破水、滑翔和回海主循环

**Files:**
- Modify: `src/components/CyberHero.astro`
- Test: `tests/interactive-features.test.mjs`

- [ ] **Step 1: 将飞鱼主时间轴调整为 14 秒抛物线**

```css
.fish-flight-path { animation: fish-surface-flight 14s cubic-bezier(.42, 0, .2, 1) infinite; }

@keyframes fish-surface-flight {
  0% { opacity: 0; transform: translate(-28%, 58%) rotate(-5deg) scale(.66); }
  10% { opacity: 1; }
  28% { transform: translate(2%, 35%) rotate(-13deg) scale(.78); }
  40% { transform: translate(16%, -2%) rotate(-24deg) scale(.92); }
  56% { transform: translate(32%, -28%) rotate(-8deg) scale(1.02); }
  70% { transform: translate(48%, -36%) rotate(3deg) scale(.98); }
  84% { opacity: 1; transform: translate(60%, 2%) rotate(22deg) scale(.86); }
  94%, 100% { opacity: 0; transform: translate(70%, 42%) rotate(12deg) scale(.72); }
}
```

- [ ] **Step 2: 添加短促出水和入水效果**

`.splash-out` 仅在 34% 至 46% 时间窗显示，`.splash-in` 仅在 82% 至 91% 显示；水滴从海面向上抛出后下落，不能整轮持续出现。

```css
@keyframes splash-break {
  0%, 33%, 47%, 100% { opacity: 0; transform: scale(.3,.1); }
  38% { opacity: .95; transform: scale(1,.9); }
  45% { opacity: 0; transform: scale(1.5,.35); }
}
```

- [ ] **Step 3: 让鱼翼在破水后展开**

鱼翼动画周期改为 14 秒：水下阶段 `scaleY(.5)`，破水时快速展开至 `scaleY(1.12)`，天空滑翔阶段缓慢呼吸，俯冲前收拢至 `.72`。

### Task 4: 将技术关键词改为跟随鱼的不可见轨道

**Files:**
- Modify: `src/components/CyberHero.astro`
- Test: `tests/interactive-features.test.mjs`

- [ ] **Step 1: 把关键词移入飞鱼局部容器**

```astro
<div class="orbit-system" aria-hidden="true">
  <span class="orbit-keyword orbit-rag"><span>RAG CORE</span></span>
  <span class="orbit-keyword orbit-agent"><span>AGENT OPS</span></span>
  <span class="orbit-keyword orbit-mlops"><span>MLOPS</span></span>
  <span class="orbit-keyword orbit-code"><span>CODE TOOLS</span></span>
</div>
```

- [ ] **Step 2: 使用不可见椭圆轨道旋转**

```css
.orbit-system { position: absolute; inset: -12% -20% -18%; pointer-events: none; }
.orbit-keyword { position: absolute; inset: 0; animation: keyword-orbit 8s linear infinite; }
.orbit-keyword span { position: absolute; top: 50%; right: -3%; transform: translateY(-50%); animation: keyword-counter-rotate 8s linear infinite; }
.orbit-agent { animation-delay: -2s; }
.orbit-mlops { animation-delay: -4s; }
.orbit-code { animation-delay: -6s; }
```

`keyword-counter-rotate` 使用与外层相反角度，让文字始终保持正向；轨道本身不绘制 border 或 outline。

- [ ] **Step 3: 根据飞行阶段控制关键词亮度**

水下阶段整体透明度约 `.32`，破水后提升到 `.78`，俯冲时回落；关键词经过后半圈时通过子元素关键帧降低到 `.35`，形成位于鱼身后方的感觉。

### Task 5: 响应式、减少动态和验证

**Files:**
- Modify: `src/components/CyberHero.astro`
- Modify: `tests/interactive-features.test.mjs`

- [ ] **Step 1: 更新移动端规则**

移动端保留四个关键词，但轨道缩小至桌面端约 72%，水花和水滴数量减少，飞鱼主路径限制在容器内部。

- [ ] **Step 2: 更新减少动态终态**

减少动态模式下停止镜头、海浪、云层、水花、飞鱼和关键词旋转；海面固定在画面底部约 18%，飞鱼完全展翼并位于天空中心，四个关键词静态均匀分布在鱼周围。

- [ ] **Step 3: 运行相关测试**

Run: `node --test tests/interactive-features.test.mjs`

Expected: 15 个交互测试全部通过。

- [ ] **Step 4: 运行生产构建**

Run: `npm run build`

Expected: Astro 构建成功并生成 464 个页面。

- [ ] **Step 5: 浏览器观察完整循环**

在 `http://localhost:4321/` 连续观察至少 15 秒，并采样 `.camera-stage`、`.fish-flight-path` 和 `.orbit-keyword` 的 computed transform。确认飞鱼破水后镜头上升、海面下降、天空成为主体，关键词位置持续绕鱼变化且随鱼一起移动。

### Task 6: 修正飞鱼朝向并添加破水翼影

**Files:**
- Modify: `src/components/CyberHero.astro`
- Modify: `tests/interactive-features.test.mjs`

- [ ] **Step 1: 添加鱼头朝右和翼影结构失败测试**

```js
assert.match(hero, /class="fish-artwork"/);
assert.match(hero, /class="wing-echo/);
assert.match(hero, /@keyframes wing-echo-flight/);
assert.match(hero, /\.fish-artwork[^}]*transform:\s*scaleX\(-1\)/s);
assert.match(hero, /\.orbit-system[^}]*transform:\s*none/s);
```

Run: `node --test --test-name-pattern="narrative flying-fish" tests/interactive-features.test.mjs`

Expected: FAIL，`class="fish-artwork"` 未匹配。

- [ ] **Step 2: 只翻转飞鱼图形，不翻转关键词系统**

用独立容器包裹飞鱼 SVG：

```astro
<div class="fish-artwork">
  <svg class="wing-echo wing-echo-a" viewBox="0 0 420 260" aria-hidden="true">...</svg>
  <svg class="wing-echo wing-echo-b" viewBox="0 0 420 260" aria-hidden="true">...</svg>
  <svg class="flying-fish" viewBox="0 0 420 260" role="img">...</svg>
</div>
```

```css
.fish-artwork { position: relative; transform: scaleX(-1); transform-origin: center; }
.orbit-system { transform: none; }
```

`.orbit-system` 保持为 `.fish-flight-path` 的兄弟子元素，因此文字不会随鱼镜像。

- [ ] **Step 3: 修正翻转后的尾部锚点**

SVG 内部坐标仍保持原始方向，因此 `.fish-tail` 继续使用原路径左边缘作为内部连接锚点；外层整体镜像后，视觉连接点自然落在鱼身左侧。通过浏览器检查尾部摆动时路径不脱离鱼身。

- [ ] **Step 4: 添加两层空中翼影**

翼影 SVG 只包含前后鱼翼路径，使用同一 `fish-wing-gradient`，不包含鱼身、眼睛、尾巴或关键词：

```css
.wing-echo { position: absolute; inset: 0; width: 100%; opacity: 0; filter: blur(2px) drop-shadow(0 0 18px rgb(132 109 232 / 28%)); animation: wing-echo-flight 14s ease-out infinite; }
.wing-echo-b { animation-delay: .16s; }

@keyframes wing-echo-flight {
  0%, 34%, 82%, 100% { opacity: 0; transform: translate3d(0, 0, 0) scale(.9); }
  42% { opacity: .24; transform: translate3d(-9px, -7px, 0) scale(1.04); }
  58% { opacity: .14; transform: translate3d(-18px, -11px, 0) scale(1.11); }
  76% { opacity: 0; transform: translate3d(-28px, -14px, 0) scale(1.18); }
}
```

- [ ] **Step 5: 验证三个阶段**

浏览器分别检查约 `t=2s` 水下阶段、`t=6s` 破水阶段和 `t=8s` 天空阶段：鱼头均位于右侧；水下翼影透明度为 `0`；破水及天空阶段翼影透明度大于 `0`；环绕关键词文字方向正常。

### Task 7: 将环绕内容替换为五组个人技术栈

**Files:**
- Modify: `src/components/CyberHero.astro`
- Modify: `tests/interactive-features.test.mjs`

- [ ] **Step 1: 添加五组技术栈失败测试**

```js
assert.match(hero, /JAVA · SPRING/);
assert.match(hero, /TYPESCRIPT · VUE/);
assert.match(hero, /PYTHON · FASTAPI/);
assert.match(hero, /AGENT · RAG/);
assert.match(hero, /DOCKER · LINUX/);
assert.match(hero, /class="orbit-keyword orbit-python"/);
assert.doesNotMatch(hero, />RAG CORE</);
assert.doesNotMatch(hero, />AGENT OPS</);
assert.doesNotMatch(hero, />MLOPS</);
assert.doesNotMatch(hero, />CODE TOOLS</);
```

Run: `node --test --test-name-pattern="narrative flying-fish" tests/interactive-features.test.mjs`

Expected: FAIL，`JAVA · SPRING` 未匹配。

- [ ] **Step 2: 替换标签并增加 Python 外层轨道项**

```astro
<span class="orbit-keyword orbit-java"><span>JAVA · SPRING</span></span>
<span class="orbit-keyword orbit-typescript"><span>TYPESCRIPT · VUE</span></span>
<span class="orbit-keyword orbit-python"><span>PYTHON · FASTAPI</span></span>
<span class="orbit-keyword orbit-agent"><span>AGENT · RAG</span></span>
<span class="orbit-keyword orbit-docker"><span>DOCKER · LINUX</span></span>
```

- [ ] **Step 3: 调整双层轨道相位**

外层 Java、TypeScript、Python 使用 9 秒周期，起始相位分别为 `0s`、`-3s`、`-6s`；内层 Agent、Docker 使用 7 秒周期，起始相位分别为 `-1.75s`、`-5.25s`。对应的反向旋转必须使用相同周期和延迟，保证文字正向。

- [ ] **Step 4: 更新减少动态静态分布**

在 `prefers-reduced-motion` 中将 Java、TypeScript、Python 分布在外层约 `0deg / 120deg / 240deg`，Agent、Docker 分布在内层约 `60deg / 240deg`，五个标签均不能隐藏。

- [ ] **Step 5: 浏览器验证**

桌面端和 390px 移动端分别确认 `.orbit-keyword` 数量为 5、五组文字均存在、没有左右裁切、没有两个标签中心距离小于 24px，并确认 `.fish-artwork` 仍保持 `scaleX(-1)`。
