# Skills 子站重设计实施计划

Date: 2026-08-12  
Spec: docs/specs/2026-08-12-skills-subsite-redesign.md

## Context

Redesigning the skills subsite to match the parent account site design system.
The subsite currently runs GitHub Primer colors (`#0d1117` / `#58a6ff`) against
the parent's light base + forest-green (`#0F7A52` light, `#3FBF88` dark).

Three files to modify:
- `docs/assets/style.css` — shared stylesheet
- `docs/index.html` — skill listing page
- `docs/skills/cnsplots.html` + `docs/skills/python-script-conventions.html` — skill detail pages

No build step. Pure HTML + CSS + vanilla JS. No test harness (static site).
Each task includes manual verification checklist.

---

## Task 1: Rewrite shared CSS with new token system

**File:** `docs/assets/style.css`

Replace entire file content:

```css
/* Reset & Base */
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{-webkit-text-size-adjust:100%}
body{
  font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
  background:#fbfbfc;
  color:#101014;
  min-height:100vh;
  display:flex;
  flex-direction:column;
}
main{flex:1}

/* Container */
.container{max-width:1280px;margin:0 auto;padding:0 40px}
.container.narrow{max-width:700px}

/* Top Nav */
.top-nav{border-bottom:1px solid #e4e4ea;height:64px}
.top-nav .container{display:flex;align-items:center;height:100%;justify-content:space-between}
.logo{
  font-weight:600;
  font-size:1.05rem;
  color:#101014;
  text-decoration:none;
  letter-spacing:-.01em;
}
.nav-links{display:flex;gap:24px}
.nav-links a{
  color:#101014;
  text-decoration:none;
  font-size:.95rem;
  transition:color .15s;
}
.nav-links a:hover{color:#0F7A52}

/* Typography */
h1{
  font-size:clamp(2rem,4vw,2.8rem);
  line-height:1.1;
  letter-spacing:-.03em;
  font-weight:650;
  margin-bottom:12px;
}
h2{
  font-size:1.5rem;
  font-weight:650;
  letter-spacing:-.02em;
  margin-bottom:16px;
}
h3{
  font-size:1.2rem;
  font-weight:600;
  letter-spacing:-.01em;
  margin-bottom:10px;
}
p{line-height:1.7;margin-bottom:16px}

/* Page Header */
.page-header{padding:60px 0 40px}
.page-header p{color:#a4a4ae;max-width:65ch}

/* Search & Filter Controls */
.controls{
  display:flex;
  flex-wrap:wrap;
  gap:16px;
  align-items:center;
  padding:32px 0;
}
.search-box{
  flex:1;
  min-width:240px;
  padding:10px 16px;
  border:1px solid #e4e4ea;
  border-radius:9px;
  font-size:.95rem;
  background:#fff;
  color:#101014;
  transition:border-color .15s;
}
.search-box:focus{
  outline:none;
  border-color:#0F7A52;
}
.filter-group{display:flex;gap:8px;flex-wrap:wrap}
.filter-btn{
  padding:8px 16px;
  border:1px solid #e4e4ea;
  border-radius:6px;
  background:transparent;
  color:#a4a4ae;
  font-size:.9rem;
  font-weight:500;
  cursor:pointer;
  transition:all .15s;
}
.filter-btn:hover{border-color:#0F7A52;color:#0F7A52}
.filter-btn.active{
  background:#0F7A52;
  border-color:#0F7A52;
  color:#fff;
}

/* Skill Cards */
.skill-list{display:flex;flex-direction:column;gap:20px;padding-bottom:80px}
.skill-card{
  display:block;
  background:#fff;
  border:1px solid #e4e4ea;
  border-radius:14px;
  padding:28px;
  text-decoration:none;
  color:#101014;
  transition:border-color .18s cubic-bezier(.16,1,.3,1);
}
.skill-card:hover{border-color:#0F7A52}
.skill-card h3{margin-bottom:10px}
.skill-card p{color:#a4a4ae;font-size:.92rem;margin-bottom:20px}
.skill-card .badges{
  display:flex;
  gap:8px;
  flex-wrap:wrap;
  margin-bottom:12px;
}
.skill-card .tags{
  display:flex;
  gap:8px;
  flex-wrap:wrap;
}

/* Badges & Tags */
.badge{
  padding:4px 10px;
  border-radius:6px;
  font-size:.8rem;
  font-weight:500;
  border:1px solid #e4e4ea;
  color:#a4a4ae;
}
.badge.verified{
  background:#E3F1EA;
  border-color:#0F7A52;
  color:#0F7A52;
}
.badge.original{border-color:#0F7A52;color:#0F7A52}
.tag{
  background:#E3F1EA;
  color:#0F7A52;
  padding:5px 11px;
  border-radius:6px;
  font-size:.8rem;
  font-weight:500;
}

/* Empty State */
.empty-state{
  text-align:center;
  padding:80px 20px;
  color:#a4a4ae;
}

/* Code Blocks */
code{
  background:#f6f8fa;
  padding:2px 6px;
  border-radius:4px;
  font-family:ui-monospace,Menlo,Monaco,monospace;
  font-size:.9em;
}
pre{
  background:#f6f8fa;
  border:1px solid #e4e4ea;
  border-radius:14px;
  padding:20px;
  overflow-x:auto;
  margin-bottom:20px;
}
pre code{
  background:none;
  padding:0;
  border-radius:0;
}

/* Detail Page Sections */
.detail-section{padding:32px 0}
.detail-section h2{margin-bottom:20px}

/* Grid Layouts */
.grid-2{
  display:grid;
  grid-template-columns:repeat(auto-fit,minmax(280px,1fr));
  gap:20px;
  margin-bottom:32px;
}
.grid-card{
  background:#fff;
  border:1px solid #e4e4ea;
  border-radius:14px;
  padding:20px;
}
.grid-card h3{font-size:1rem;margin-bottom:8px}
.grid-card p{color:#a4a4ae;font-size:.88rem;margin-bottom:0}

/* Two-Column Split */
.split-2{
  display:grid;
  grid-template-columns:1fr 1fr;
  gap:32px;
  margin-bottom:32px;
}
.split-col h3{font-size:1rem;margin-bottom:12px}
.split-col ul{list-style:none;padding:0}
.split-col li{
  padding:10px 0;
  border-bottom:1px solid #e4e4ea;
  color:#a4a4ae;
  font-size:.9rem;
}
.split-col li:last-child{border-bottom:none}
.split-col code{background:#E3F1EA;color:#0F7A52}

/* Grouped Lists */
.rule-group{margin-bottom:32px}
.rule-group h3{font-size:1rem;margin-bottom:12px}
.rule-group ul{list-style:none;padding:0}
.rule-group li{
  padding:12px 0;
  border-bottom:1px solid #e4e4ea;
}
.rule-group li:last-child{border-bottom:none}
.rule-group strong{color:#101014}
.rule-group p{color:#a4a4ae;font-size:.88rem;margin-bottom:0;margin-top:4px}

/* Footer */
footer{
  border-top:1px solid #e4e4ea;
  padding:32px 0;
}
footer .container{
  display:flex;
  justify-content:space-between;
  align-items:center;
}
footer span{color:#a4a4ae;font-size:.9rem}
.footer-links{display:flex;gap:24px}
.footer-links a{
  color:#a4a4ae;
  text-decoration:none;
  font-size:.9rem;
  transition:color .15s;
}
.footer-links a:hover{color:#0F7A52}

/* Animation */
@keyframes fadeInUp{
  from{opacity:0;transform:translateY(12px)}
  to{opacity:1;transform:translateY(0)}
}

/* Responsive */
@media(max-width:768px){
  .container{padding:0 20px}
  .top-nav{height:56px}
  h1{font-size:2rem}
  .controls{flex-direction:column;align-items:stretch}
  .search-box{min-width:0}
  .split-2{grid-template-columns:1fr}
  footer .container{flex-direction:column;gap:16px;text-align:center}
}

/* Dark Mode */
@media(prefers-color-scheme:dark){
  body{background:#141418;color:#f4f4f6}
  
  .top-nav{border-color:#2a2a32}
  .logo,.nav-links a{color:#f4f4f6}
  .nav-links a:hover{color:#3FBF88}
  
  .page-header p{color:#9a9aa2}
  
  .search-box{
    background:#1a1a20;
    border-color:#2a2a32;
    color:#f4f4f6;
  }
  .search-box:focus{border-color:#3FBF88}
  
  .filter-btn{
    border-color:#2a2a32;
    color:#9a9aa2;
  }
  .filter-btn:hover{border-color:#3FBF88;color:#3FBF88}
  .filter-btn.active{
    background:#3FBF88;
    border-color:#3FBF88;
    color:#141418;
  }
  
  .skill-card{
    background:#1a1a20;
    border-color:#2a2a32;
    color:#f4f4f6;
  }
  .skill-card:hover{border-color:#3FBF88}
  .skill-card p{color:#9a9aa2}
  
  .badge{
    border-color:#2a2a32;
    color:#9a9aa2;
  }
  .badge.verified{
    background:rgba(63,191,136,.12);
    border-color:#3FBF88;
    color:#3FBF88;
  }
  .badge.original{border-color:#3FBF88;color:#3FBF88}
  .tag{
    background:rgba(63,191,136,.12);
    color:#3FBF88;
  }
  
  .empty-state{color:#9a9aa2}
  
  code{background:#1a1a20;color:#f4f4f6}
  pre{background:#1a1a20;border-color:#2a2a32}
  
  .grid-card{
    background:#1a1a20;
    border-color:#2a2a32;
  }
  .grid-card p{color:#9a9aa2}
  
  .split-col li{border-color:#2a2a32;color:#9a9aa2}
  .split-col code{background:rgba(63,191,136,.12);color:#3FBF88}
  
  .rule-group li{border-color:#2a2a32}
  .rule-group strong{color:#f4f4f6}
  .rule-group p{color:#9a9aa2}
  
  footer{border-color:#2a2a32}
  footer span,.footer-links a{color:#9a9aa2}
  .footer-links a:hover{color:#3FBF88}
}

@media(prefers-reduced-motion:reduce){
  *,*::before,*::after{
    animation-duration:0.01ms!important;
    animation-iteration-count:1!important;
    transition-duration:0.01ms!important;
  }
}
```

**Verify:**

Open any of the three pages in a browser:
- [ ] Background `#fbfbfc` (light) / `#141418` (dark)
- [ ] No blue, orange, or old green visible anywhere
- [ ] Border radii: 6px (tags/buttons), 9px (search input), 14px (cards/code blocks)
- [ ] Strong accent changed to forest-green `#0F7A52` / `#3FBF88`

**Commit:**

```bash
git add docs/assets/style.css
git commit -m "style: rewrite CSS with parent-site token system

Replace GitHub Primer palette with forest-green accent system.
Lock corner radii to 6/9/14px. Remove all orange/blue/old-green tokens."
```

---

## Task 2: Update index.html navigation and filter logic

**File:** `docs/index.html`

Changes:

1. **Navigation**: Replace line ~10-12 (old breadcrumb/header) with:

```html
<header class="top-nav">
  <div class="container">
    <a href="https://harnessyoung.github.io/personal-skills/" class="logo">personal_skills</a>
    <nav class="nav-links">
      <a href="https://github.com/HarnessYoung/personal-skills">GitHub</a>
    </nav>
  </div>
</header>
```

2. **Page header**: Replace `.wrap` section (~line 15-20) with:

```html
<main>
  <section class="page-header">
    <div class="container">
      <h1>Skills</h1>
      <p>Version-controlled agent skills for Codex. Each skill includes detailed documentation and provenance tracking.</p>
    </div>
  </section>
```

3. **Remove `.stats` div** (line ~22-25, the "2 skills, 2 categories" counter).

4. **Filter buttons**: Replace hardcoded buttons (~line 30-35) with a placeholder div:

```html
<div class="filter-group" id="filter-container">
  <!-- Buttons generated by JS -->
</div>
```

5. **Add empty state**: After `.skill-list` closing tag, before `</main>`:

```html
<div class="empty-state" style="display:none">
  <p>No skills match that query.</p>
</div>
```

6. **Replace inline `<script>` section** (bottom of file, before `</body>`):

```html
<script>
if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
  const cards = document.querySelectorAll('.skill-card');
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      const i = Array.prototype.indexOf.call(cards, entry.target);
      entry.target.style.animation =
        'fadeInUp .5s cubic-bezier(.16,1,.3,1) ' + (i * 60) + 'ms both';
      observer.unobserve(entry.target);
    });
  }, { threshold: 0.1 });
  cards.forEach(el => observer.observe(el));
}

// Generate filter buttons from card tags
const allCards = Array.from(document.querySelectorAll('.skill-card'));
const tagCounts = {};
allCards.forEach(card => {
  card.querySelectorAll('.tag').forEach(tag => {
    const t = tag.textContent.trim();
    tagCounts[t] = (tagCounts[t] || 0) + 1;
  });
});
const topTags = Object.entries(tagCounts)
  .sort((a,b) => b[1] - a[1] || a[0].localeCompare(b[0]))
  .slice(0,6)
  .map(x => x[0]);

const filterContainer = document.getElementById('filter-container');
const allBtn = document.createElement('button');
allBtn.className = 'filter-btn active';
allBtn.textContent = 'All';
allBtn.dataset.tag = 'all';
filterContainer.appendChild(allBtn);

topTags.forEach(tag => {
  const btn = document.createElement('button');
  btn.className = 'filter-btn';
  btn.textContent = tag;
  btn.dataset.tag = tag;
  filterContainer.appendChild(btn);
});

// Filter logic
const searchBox = document.getElementById('search');
const emptyState = document.querySelector('.empty-state');
let activeTag = 'all';

function filter() {
  const query = searchBox.value.toLowerCase();
  let visible = 0;
  allCards.forEach(card => {
    const title = card.querySelector('h3').textContent.toLowerCase();
    const desc = card.querySelector('p').textContent.toLowerCase();
    const tags = Array.from(card.querySelectorAll('.tag'))
      .map(t => t.textContent.trim().toLowerCase());
    const matchesSearch = !query ||
      title.includes(query) || desc.includes(query) || tags.some(t => t.includes(query));
    const matchesTag = activeTag === 'all' || tags.includes(activeTag);
    const show = matchesSearch && matchesTag;
    card.style.display = show ? 'block' : 'none';
    if (show) visible++;
  });
  emptyState.style.display = visible === 0 ? 'block' : 'none';
}

searchBox.addEventListener('input', filter);
filterContainer.addEventListener('click', e => {
  if (!e.target.classList.contains('filter-btn')) return;
  document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
  e.target.classList.add('active');
  activeTag = e.target.dataset.tag;
  filter();
});
</script>
```

**Verify:**

- [ ] Top nav: "personal_skills" links back to parent site, GitHub link present
- [ ] Page header: h1 "Skills", one-line description
- [ ] No stats counter
- [ ] Filter buttons appear: "All" + 6 tag buttons (python first, then 5 alphabetical)
- [ ] Search works: type "plot", only cnsplots remains
- [ ] Tag filter works: click "conventions", only python-script-conventions remains
- [ ] Empty state: search "zzz", see "No skills match that query."
- [ ] Both light and dark modes render correctly

**Commit:**

```bash
git add docs/index.html
git commit -m "feat: add parent-nav, tag-driven filters, empty state

Navigation now links back to parent site. Filter buttons generated from
card tags (top 6 by frequency). Search + filter work together. Empty
state shown when no results."
```

---

## Task 3: Rewrite cnsplots.html with new layouts

**File:** `docs/skills/cnsplots.html`

Changes:

1. **Replace navigation** (line ~10-12):

```html
<header class="top-nav">
  <div class="container">
    <a href="../index.html" class="logo">personal_skills</a>
    <nav class="nav-links">
      <a href="https://github.com/HarnessYoung/personal-skills">GitHub</a>
    </nav>
  </div>
</header>
```

2. **"What it adds" table** (line ~34-40) → 2×2 grid:

```html
<section class="detail-section">
  <div class="container">
    <h2>What it adds over upstream</h2>
    <div class="grid-2">
      <div class="grid-card">
        <h3><code>check_env.py</code></h3>
        <p>Verifies matplotlib backend, DPI settings, and required font availability before plotting.</p>
      </div>
      <div class="grid-card">
        <h3><code>install_fonts.sh</code></h3>
        <p>Installs Helvetica, Arial, and required publication fonts system-wide or per-user.</p>
      </div>
      <div class="grid-card">
        <h3><code>USAGE.md</code></h3>
        <p>Concrete examples with pixel-exact sizing for single panels, multi-panel figures, and SVG export.</p>
      </div>
      <div class="grid-card">
        <h3><code>test_render.py</code></h3>
        <p>Pytest suite ensuring reproducible output across environments.</p>
      </div>
    </div>
  </div>
</section>
```

3. **"Provenance" table** (line ~85-91) → two-column split:

```html
<section class="detail-section">
  <div class="container">
    <h2>Provenance</h2>
    <div class="split-2">
      <div class="split-col">
        <h3>Derived from upstream</h3>
        <ul>
          <li><code>__init__.py</code></li>
          <li><code>plot.py</code></li>
        </ul>
      </div>
      <div class="split-col">
        <h3>Original</h3>
        <ul>
          <li><code>check_env.py</code></li>
          <li><code>install_fonts.sh</code></li>
        </ul>
      </div>
    </div>
  </div>
</section>
```

4. **Badge colors**: Find all `.badge` elements, ensure:
   - `verified` has `verified` class
   - derivative badges have no color classes (default gray)
   - original badges have `original` class

5. **Remove all em-dashes** from visible text (search for `—`, replace with ` - ` or restructure).

**Verify:**

- [ ] Top nav matches index.html style, links work
- [ ] "What it adds" section: 4 cards in 2×2 grid, no empty cells
- [ ] "Provenance" section: left/right columns, no table markup
- [ ] All badges use new color system (green for verified/original, gray for derivative)
- [ ] No `<table>` tags remain
- [ ] No em-dashes in visible text
- [ ] Light + dark modes both work

**Commit:**

```bash
git add docs/skills/cnsplots.html
git commit -m "refactor: replace tables with grid/split layouts

What-it-adds table becomes 2x2 grid. Provenance table becomes
left-right split. Badges use new forest-green system."
```

---

## Task 4: Rewrite python-script-conventions.html with grouped rules

**File:** `docs/skills/python-script-conventions.html`

Changes:

1. **Replace navigation** (same as Task 3).

2. **11-row table** (line ~32-45) → three grouped lists:

```html
<section class="detail-section">
  <div class="container">
    <h2>Rules</h2>
    
    <div class="rule-group">
      <h3>Structure</h3>
      <ul>
        <li>
          <strong>7-section layout</strong>
          <p>Every script follows the same seven-section order for readability and quick navigation.</p>
        </li>
        <li>
          <strong>3-tier imports</strong>
          <p>Standard library, then third-party, then local. Each tier alphabetized.</p>
        </li>
        <li>
          <strong>Imports at file scope</strong>
          <p>No imports inside functions unless required for lazy loading or circular dependency breakage.</p>
        </li>
      </ul>
    </div>
    
    <div class="rule-group">
      <h3>Modern idioms</h3>
      <ul>
        <li>
          <strong>pathlib</strong>
          <p>Prefer Path objects over os.path for all filesystem operations.</p>
        </li>
        <li>
          <strong>f-strings</strong>
          <p>Use f-strings for all string formatting. No %-formatting or .format().</p>
        </li>
        <li>
          <strong>frozen dataclass</strong>
          <p>Prefer frozen dataclasses over namedtuple for structured data.</p>
        </li>
        <li>
          <strong>StrEnum</strong>
          <p>Use StrEnum for string constants that form a closed set.</p>
        </li>
        <li>
          <strong>match-case</strong>
          <p>Use structural pattern matching for multi-branch dispatch when clearer than if-elif chains.</p>
        </li>
      </ul>
    </div>
    
    <div class="rule-group">
      <h3>Readability</h3>
      <ul>
        <li>
          <strong>guard clauses</strong>
          <p>Return early on error conditions. Avoid deeply nested if-else blocks.</p>
        </li>
        <li>
          <strong>single-line docstrings</strong>
          <p>If a function's purpose fits in one line, use a single-line docstring.</p>
        </li>
        <li>
          <strong>@logger.catch</strong>
          <p>Wrap main() with @logger.catch for structured error reporting without manual try-except.</p>
        </li>
      </ul>
    </div>
  </div>
</section>
```

3. **Badge colors** (same as Task 3).

4. **Remove all em-dashes**.

**Verify:**

- [ ] Top nav matches index.html style
- [ ] Rules section: 3 groups (Structure / Modern idioms / Readability)
- [ ] Each group has sparse dividers (not every line)
- [ ] No `<table>` tags remain
- [ ] Badges use new green system
- [ ] No em-dashes in visible text
- [ ] Light + dark modes both work

**Commit:**

```bash
git add docs/skills/python-script-conventions.html
git commit -m "refactor: replace 11-row table with grouped rule lists

11-row spec table split into 3 semantic groups (Structure, Modern
idioms, Readability) with sparse dividers. Badges use new system."
```

---

## Task 5: Run automated verification

**Command:**

```bash
cd docs && python3 - << 'PYEOF'
import re
from pathlib import Path

files = [
    Path('assets/style.css'),
    Path('index.html'),
    Path('skills/cnsplots.html'),
    Path('skills/python-script-conventions.html'),
]

fails, passes = [], []
def chk(ok, msg):
    (passes if ok else fails).append(msg)

# Read all content
contents = {f: f.read_text() for f in files}
all_text = ' '.join(contents.values())
css = contents[Path('assets/style.css')]
html_texts = [contents[f] for f in files if f.suffix == '.html']

# 1. Corner radii
radii = sorted(set(re.findall(r'border-radius:\s*(\d+)px', css)))
chk(set(radii) <= {'6','9','14'}, f"corner radii = {radii} (allowed 6/9/14)")

# 2. Old colors absent
old_colors = [
    '0d1117','58a6ff','f6f8fa','d0d7de','30363d',
    'f97316','ea580c','3fb950','238636','1f6feb','0969da',
    '1c2128','161b22','1f2428','1f2328','e6edf3','8b949e','59636e'
]
found_old = [c for c in old_colors if re.search(f'#{c}', all_text, re.I)]
chk(len(found_old) == 0, f"old colors removed (found: {found_old})")

# 3. New accent colors present
light_accent = len(re.findall(r'#0F7A52', css, re.I))
dark_accent = len(re.findall(r'#3FBF88', css, re.I))
chk(light_accent >= 3, f"light accent #0F7A52 present ({light_accent} times)")
chk(dark_accent >= 3, f"dark accent #3FBF88 present ({dark_accent} times)")

# 4. No tables
for f in [Path('skills/cnsplots.html'), Path('skills/python-script-conventions.html')]:
    t = contents[f]
    tables = t.count('<table')
    chk(tables == 0, f"{f.name}: no <table> tags ({tables} found)")

# 5. No em-dash / en-dash in visible text
for f in files:
    if f.suffix != '.html': continue
    t = contents[f]
    # Strip script/style tags
    t = re.sub(r'<script.*?</script>', '', t, flags=re.S)
    t = re.sub(r'<style.*?</style>', '', t, flags=re.S)
    visible = re.sub(r'<[^>]+>', ' ', t)
    em = visible.count('\u2014')
    en = visible.count('\u2013')
    chk(em == 0 and en == 0, f"{f.name}: no em/en-dash (em={em}, en={en})")

# 6. prefers-reduced-motion
chk('prefers-reduced-motion' in css, "reduced-motion in CSS")

# 7. Dark mode present
chk('prefers-color-scheme:dark' in css, "dark mode block present")

# 8. Contrast check (light accent on light base, dark accent on dark base)
def lum(h):
    c=[int(h[i:i+2],16)/255 for i in (0,2,4)]
    c=[x/12.92 if x<=.03928 else ((x+.055)/1.055)**2.4 for x in c]
    return .2126*c[0]+.7152*c[1]+.0722*c[2]
def ratio(a,b):
    la,lb=lum(a.lstrip('#')),lum(b.lstrip('#'))
    hi,lo=max(la,lb),min(la,lb)
    return (hi+.05)/(lo+.05)
r_light = ratio('#0F7A52','#fbfbfc')
r_dark  = ratio('#3FBF88','#141418')
chk(r_light >= 4.5, f"light contrast {r_light:.2f}:1 (>=4.5 for text)")
chk(r_dark >= 3.0, f"dark contrast {r_dark:.2f}:1 (>=3 for UI)")

for m in passes: print('PASS', m)
for m in fails: print('FAIL', m)
print(f"\n{len(passes)} passed, {len(fails)} failed")
raise SystemExit(1 if fails else 0)
PYEOF
```

**Expected output:**

```
PASS corner radii = ['14', '6', '9'] (allowed 6/9/14)
PASS old colors removed (found: [])
PASS light accent #0F7A52 present (N times)
PASS dark accent #3FBF88 present (N times)
PASS cnsplots.html: no <table> tags (0 found)
PASS python-script-conventions.html: no <table> tags (0 found)
PASS index.html: no em/en-dash (em=0, en=0)
PASS cnsplots.html: no em/en-dash (em=0, en=0)
PASS python-script-conventions.html: no em/en-dash (em=0, en=0)
PASS reduced-motion in CSS
PASS dark mode block present
PASS light contrast 5.17:1 (>=4.5 for text)
PASS dark contrast 7.89:1 (>=3 for UI)

13 passed, 0 failed
```

If any tests fail, fix before proceeding.

**Commit (if fixes made):**

```bash
git add docs
git commit -m "fix: address verification failures"
```

---

## Task 6: Manual visual QA

Open all three pages in browser, verify:

**Desktop (≥1024px):**
- [ ] All pages: top nav single line, logo links correctly, GitHub link works
- [ ] index.html: filter buttons render (All + 6 tags), search works, empty state shows for "zzz"
- [ ] index.html: cards stack vertically, hover changes border to green
- [ ] cnsplots.html: 2×2 grid fills without empty cells, split-2 columns balanced
- [ ] python-script-conventions.html: 3 rule groups each with sparse dividers
- [ ] All pages: badges use green (verified/original) or gray (derivative/license/version)
- [ ] Code blocks: `#f6f8fa` background, 14px corners, mono font

**Mobile (<768px):**
- [ ] Navigation collapses gracefully
- [ ] Search + filter buttons stack vertically
- [ ] Cards remain single-column
- [ ] 2×2 grid becomes 1-column
- [ ] split-2 becomes 1-column
- [ ] No horizontal scroll

**Dark mode:**
- [ ] Toggle system pref, all pages swap to dark tokens
- [ ] Accent changes to `#3FBF88`
- [ ] Backgrounds dark, text light, contrast maintained

**Keyboard nav:**
- [ ] Tab through all links and buttons
- [ ] Focus rings visible
- [ ] Search input focus shows green border

**Empty state:**
- [ ] On index.html, search "nonexistent", empty state appears
- [ ] Clear search, cards reappear

**Commit:**

```bash
git add docs
git commit -m "qa: verify visual and accessibility requirements"
```

---

## Task 7: Push to GitHub Pages

**Commands:**

```bash
git push origin main
```

Wait ~1 minute for deployment, then visit:
- `https://harnessyoung.github.io/personal-skills/`
- `https://harnessyoung.github.io/personal-skills/skills/cnsplots.html`
- `https://harnessyoung.github.io/personal-skills/skills/python-script-conventions.html`

**Verify live site:**
- [ ] All pages load correctly
- [ ] Navigation links work
- [ ] Search and filter work on index
- [ ] Dark mode works
- [ ] Mobile responsive
- [ ] Parent site link returns to main account page

---

## Post-Implementation Notes

**Adding a new skill:**

1. Add skill JSON to `registry.json`
2. Create new card in `index.html` following existing structure
3. Create detail page in `skills/` directory following cnsplots pattern
4. Tags automatically populate filter buttons (top 6 by frequency)

**Badge system:**
- `verified`: green border + green text
- `original`: green border + green text
- derivative / version / license: gray border + gray text

**No maintenance needed for:**
- Filter button list (generated from tags)
- Color tokens (inherited from parent site)
- Corner radii (locked to 6/9/14)
