# Skills 子站重设计方案

日期：2026-08-12
状态：已确认，待实施
关联：docs/specs/2026-08-12-account-site-design.md（父站设计，token 来源）

## Design Read

Redesign-preserve 的开发者子站，面向浏览可安装 skill 的开发者，
沿用父站已锁定的「浅底 + 单一深绿」语言，原生 CSS 实现。

三个尺度与父站一致（redesign-preserve 规则：匹配现有 dial）：
- DESIGN_VARIANCE: 6
- MOTION_INTENSITY: 3
- VISUAL_DENSITY: 4

## 审计：改前的三个实质问题

**1. 两套设计系统并存。** 子站用 GitHub Primer 配色（`#0d1117` / `#58a6ff` /
`#f6f8fa`），父站是浅底 + `#0F7A52`。从主站点进子站像换了个网站。

**2. 圆角系统失控。** 子站出现 6 种圆角：`4px / 5px / 6px / 8px / 999px /
0 6px 6px 0`。父站锁定 `6/9/14` 三档。违反 Shape Consistency Lock。

**3. 长列表用了最差布局。** `cnsplots.html` 两个表格共 10 行，
`python-script-conventions.html` 一个 11 行表格，均为逐行 `border-b`。
这是明确点名的最差默认布局。

另：三个页面均含 em-dash，零容忍。

## 设计 token（全部继承父站）

| 用途 | 浅色 | 深色 |
| --- | --- | --- |
| 页面底 | `#fbfbfc` | `#141418` |
| 卡片底 | `#ffffff` | `#1a1a20` |
| 边框 | `#e4e4ea` | `#2a2a32` |
| 主文字 | `#101014` | `#f4f4f6` |
| 次文字 | `#a4a4ae` | `#9a9aa2` |
| 强调色 | `#0F7A52` | `#3FBF88` |
| tag 底 | `#E3F1EA` | `rgba(63,191,136,.12)` |
| 代码块底 | `#f6f8fa` | `#1a1a20` |

圆角三档：**6px**（tag / 按钮）、**9px**（输入框）、**14px**（卡片 / 代码块）。
改前的 6 种圆角全部作废。

字体：系统字体栈，不引 Google Fonts。代码用 `ui-monospace` 栈。

**颜色一致性锁：** 全站仅一个强调色。改前的橙 `#f97316` / `#ea580c`、
蓝 `#1f6feb` / `#58a6ff` / `#0969da`、绿 `#3fb950` / `#238636` 全部移除。

## 首页结构（index.html）

```
顶部导航（单行 64px）
├─ 左：personal_skills（链回 harnessyoung.github.io）
└─ 右：GitHub

标题区
├─ h1: Skills
└─ 说明句（≤20 词）

筛选条
├─ 搜索框（9px 圆角，focus 转深绿边框）
└─ tag 按钮组（6px 圆角，选中态深绿底白字）

卡片列表（单列纵向堆叠）
└─ 每张：标题 / 描述 / badges / tags

页脚（单行，1px 上边框）
```

### 决定与理由

- **卡片单列，不做网格。** 父站首屏右栏即单列卡片，保持一致；且 skill 卡片
  含四个 badge（版本 / origin / license / 验证状态），双列会挤。
- **移除 `.stats`（「2 skills, 2 categories」）。** 计数会过期，且卡片就在下方，
  可直接数。与父站移除 skill 计数是同一决定。
- **顶部导航左侧链回父站。** 改前子站是孤岛，进来无法返回。
- **tag 按钮由 JS 从卡片 DOM 生成，不硬编码。** 按出现频次降序取前 6。
  当前结果：`python`(2) 打头，随后频次 1 者按字母序
  （`bioinformatics` / `code-quality` / `conventions` / `matplotlib` / `publication`）。
  其余靠搜索覆盖。

### 为何弃用改前的硬编码分类

改前按钮为 `All / Python / Visualization`，与数据不匹配：两个 skill 都带
`python` tag，点「Python」等于不筛选。改为 tag 驱动后，分类永远与数据一致，
新增 skill 无需维护分类列表。

## 子页面重构

### cnsplots.html

- **「What it adds over upstream」4 行表格** → 2×2 卡片网格。每格：脚本名
  `<code>` 作标题 + 一句说明。4 项填满网格，无空格。
- **「Provenance」4 行表格** → 两栏分组。左栏「Derived from upstream」2 项，
  右栏「Original」2 项。该内容本质是来源二分，分栏比表格更直接。

### python-script-conventions.html

**11 行表格** → 按语义分 3 组，每组一个小标题 + 组内规则列表，组内用稀疏
`divide-y`（3-5 条），不再 11 条平铺加线：

- **Structure**: 7-section layout, 3-tier imports, imports at file scope
- **Modern idioms**: pathlib, f-strings, frozen dataclass, StrEnum, match-case
- **Readability**: guard clauses, single-line docstrings, `@logger.catch`

### 两个子页面共同改动

- **导航条替换面包屑。** 改前为 `personal_skills / cnsplots` 纯文字面包屑，
  改为与首页一致的导航条。导航条已承担返回功能，面包屑冗余。
- **badge 换色。** `origin` badge 的橙、蓝全部去掉：derivative 用中性灰边框，
  original 用深绿边框。verified badge 的 `#3fb950` 换成 `#0F7A52`。
- **清除全部 em-dash。**
- **新增代码块样式**（父站无此组件）：底色见 token 表，14px 圆角，
  `ui-monospace` 字体栈。

### 眼罩计数

首页 3 个 h2，子页各 7 个 h2，全站零 uppercase 眼罩。本次不新增任何眼罩，
`Skills` / `About` 等均为普通 h2。满足「≤ ceil(sections/3)」。

## 交互与动效

仅三处，均有功能理由：

**1. 搜索框**
- 实时过滤，匹配标题 + 描述 + tag（不匹配 badge，搜版本号无意义）
- Focus：边框转 `#0F7A52`，无 outline glow
- **空结果态**：显示「No skills match that query.」。改前无此态，搜不到即空白。

**2. tag 按钮**
- 单选切换。选中态深绿底白字，未选中透明底灰边框
- 由 JS 从卡片 DOM 生成；无 JS 时降级为显示全部卡片（渐进增强）

**3. 卡片 hover**
- 边框转深绿，`180ms cubic-bezier(.16,1,.3,1)`
- 不做位移。理由同父站：卡片是点击目标，位移会移动光标目标。

**动效**：仅卡片进场淡入上移，`60ms` 错开，一次性。
`prefers-reduced-motion` 全部降级。动效预算与父站一致。

**明确不做**：筛选切换的 FLIP 重排动画。2-6 张卡片重排肉眼几乎无感，
实现成本与出错概率都高。直接切换 `display`。

## 技术实现

原生 CSS + 一段 vanilla JS（tag 生成 / 过滤 / IntersectionObserver）。不引库。

三页共享 `assets/style.css`。筛选 JS 内联于 `index.html`（仅首页需要）。

## 验证

自动检查（Python 脚本，扩展至多文件）：

- 圆角仅出现 `6/9/14`
- 强调色语义槽位各一次，无橙蓝绿残留
- 三个文件零 em-dash / en-dash
- 无 `<table>` 残留
- `prefers-reduced-motion` 存在
- 深浅两色强调色对比度实测
- 每张卡片的 tag 均可在按钮组中找到（数据一致性）

人工检查：两种颜色模式、移动端塌陷、键盘 tab 遍历、搜索空结果态。

## 不改动的部分

- URL 结构与文件名（`index.html` / `skills/cnsplots.html` /
  `skills/python-script-conventions.html`）
- 所有正文文案与技术内容
- `registry.json` 与各 `skill.json`
- 页面信息架构（首页列表 + 每 skill 一子页）
