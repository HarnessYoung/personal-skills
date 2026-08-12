# Account Site Implementation Plan

Date: 2026-08-12  
Spec: docs/specs/2026-08-12-account-site-design.md  
Target repo: HarnessYoung/HarnessYoung.github.io

## Context

Implementing a redesigned account site from the approved spec. The design uses:
- Left-right split layout
- Light base with single forest-green accent (#0F7A52 light, #3FBF88 dark)
- Project cards in the hero right column (not decorative placeholder)
- Native CSS only, no animation library
- Static HTML, no build step

The existing repo has one commit with a placeholder `index.html`. This plan replaces it entirely.

## Verification Strategy

No automated test harness (static HTML site, no build pipeline). Each task includes a manual verification checklist. Open `index.html` in a browser after each task and confirm the checks pass before committing.

---

## Task 1: Scaffold base HTML structure

**File:** `index.html`

Replace entire file content:

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="HarnessYoung — Bioinformatics researcher building agent skills and scientific tooling">
<title>HarnessYoung</title>
<style>
/* CSS added in next tasks */
</style>
</head>
<body>
<header class="top-nav">
  <div class="container">
    <a href="/" class="logo">HarnessYoung</a>
    <nav class="nav-links">
      <a href="https://github.com/HarnessYoung">GitHub</a>
      <a href="mailto:harness4young@outlook.com">Email</a>
    </nav>
  </div>
</header>

<main>
  <section class="hero">
    <div class="container split">
      <div class="hero-left">
        <div class="eyebrow">BIOINFORMATICS</div>
        <h1>Building agent skills and scientific tooling</h1>
        <p class="tagline">Reproducible workflows for bioinformatics research.</p>
        <div class="cta-group">
          <a href="https://harnessyoung.github.io/personal-skills/" class="btn btn-primary">View skills</a>
          <a href="https://github.com/HarnessYoung" class="btn btn-secondary">GitHub</a>
        </div>
      </div>
      <div class="hero-right">
        <a href="https://harnessyoung.github.io/personal-skills/" class="project-card">
          <h3>personal-skills</h3>
          <p class="card-desc">Version-controlled agent skills for Codex and Claude Code. Includes publication-quality scientific plotting and Python coding standards.</p>
          <div class="card-meta">
            <span>Python</span>
            <span>Updated Aug 2026</span>
          </div>
          <div class="card-tags">
            <span class="tag">agent-skills</span>
            <span class="tag">codex</span>
            <span class="tag">python</span>
          </div>
        </a>
      </div>
    </div>
  </section>

  <section class="about">
    <div class="container narrow">
      <h2>About</h2>
      <p>I'm a bioinformatics researcher working on S. pombe phenotype analysis and reproducible computational workflows.</p>
      <p>My focus is building tools and skills that help AI agents write better scientific code. Each project includes detailed documentation, version control, and provenance tracking.</p>
    </div>
  </section>
</main>

<footer>
  <div class="container">
    <span>© 2026 Yusheng Yang</span>
    <div class="footer-links">
      <a href="https://github.com/HarnessYoung">GitHub</a>
      <a href="mailto:harness4young@outlook.com">Email</a>
    </div>
  </div>
</footer>
</body>
</html>
```

**Verify:**

Open `index.html` in browser:
- [ ] Title bar reads "HarnessYoung"
- [ ] All text content visible (unstyled but readable)
- [ ] No JavaScript errors in console
- [ ] Heading says "Building agent skills and scientific tooling"
- [ ] Project card has title "personal-skills"

**Commit:**

```bash
git add index.html
git commit -m "feat: scaffold base HTML structure for account site"
```

---

## Task 2: Add base layout and typography CSS

**File:** `index.html`

Replace the empty `<style>` block with:

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
  font-size:clamp(2.5rem,5vw,4rem);
  line-height:1.1;
  letter-spacing:-.03em;
  font-weight:650;
  margin-bottom:16px;
}
h2{
  font-size:1.8rem;
  font-weight:650;
  letter-spacing:-.02em;
  margin-bottom:24px;
}
h3{
  font-size:1.3rem;
  font-weight:600;
  letter-spacing:-.01em;
  margin-bottom:12px;
}
p{line-height:1.7}

/* Responsive */
@media(max-width:768px){
  .container{padding:0 20px}
  .top-nav{height:56px}
  h1{font-size:2.2rem}
}
```

**Verify:**

Reload page:
- [ ] Top nav has bottom border, "HarnessYoung" on left, links on right
- [ ] Nav height ~64px desktop
- [ ] Hover nav links turns green `#0F7A52`
- [ ] h1 is large, tight letter-spacing
- [ ] Footer at bottom (flex layout working)
- [ ] Mobile (<768px): nav shorter, h1 smaller, padding tighter

**Commit:**

```bash
git add index.html
git commit -m "style: add base layout and typography"
```

---

## Task 3: Add hero section styles

**File:** `index.html`

Append to `<style>`:

```css
/* Hero */
.hero{padding:80px 0}
.hero .split{
  display:grid;
  grid-template-columns:1fr 1fr;
  gap:60px;
  align-items:center;
}
.eyebrow{
  font-size:.7rem;
  font-weight:700;
  text-transform:uppercase;
  letter-spacing:.15em;
  color:#0F7A52;
  margin-bottom:20px;
}
.tagline{
  font-size:1.1rem;
  color:#a4a4ae;
  margin-bottom:28px;
  max-width:90%;
}

/* Buttons */
.cta-group{display:flex;gap:12px;flex-wrap:wrap}
.btn{
  display:inline-block;
  padding:11px 24px;
  border-radius:9px;
  font-weight:500;
  font-size:.95rem;
  text-decoration:none;
  transition:all .12s;
}
.btn-primary{
  background:#0F7A52;
  color:#fff;
}
.btn-primary:hover{background:#0D6A48}
.btn-primary:active{transform:scale(.98)}
.btn-secondary{
  background:#fff;
  color:#101014;
  border:1px solid #e4e4ea;
}
.btn-secondary:hover{border-color:#0F7A52}
.btn-secondary:active{transform:scale(.98)}

@media(max-width:768px){
  .hero{padding:60px 0}
  .hero .split{
    grid-template-columns:1fr;
    gap:40px;
  }
}
```

**Verify:**

- [ ] Hero split: left column text, right column card, side-by-side desktop
- [ ] Eyebrow "BIOINFORMATICS" green, small uppercase
- [ ] Primary button green, white text
- [ ] Secondary button white, gray border
- [ ] Button hover: primary darkens, secondary border turns green
- [ ] Button active: scales down slightly
- [ ] Mobile: columns stack vertically

**Commit:**

```bash
git add index.html
git commit -m "style: add hero section and button styles"
```

---

## Task 4: Add project card styles

**File:** `index.html`

Append to `<style>`:

```css
/* Project Card */
.project-card{
  display:block;
  background:#fff;
  border:1px solid #e4e4ea;
  border-radius:14px;
  padding:28px;
  text-decoration:none;
  color:#101014;
  transition:border-color .18s cubic-bezier(.16,1,.3,1),background .18s;
}
.project-card:hover{
  border-color:#0F7A52;
  background:#fdfefd;
}
.project-card h3{margin-bottom:12px}
.card-desc{
  color:#a4a4ae;
  font-size:.92rem;
  line-height:1.65;
  margin-bottom:20px;
}
.card-meta{
  display:flex;
  gap:16px;
  flex-wrap:wrap;
  font-size:.85rem;
  color:#a4a4ae;
  margin-bottom:16px;
}
.card-tags{
  display:flex;
  gap:8px;
  flex-wrap:wrap;
}
.tag{
  background:#E3F1EA;
  color:#0F7A52;
  padding:5px 11px;
  border-radius:6px;
  font-size:.8rem;
  font-weight:500;
}
```

**Verify:**

- [ ] Card has white background, light gray border
- [ ] Hover: border turns green `#0F7A52`
- [ ] Card does NOT move vertically on hover (no translateY)
- [ ] Tags have light green background `#E3F1EA`
- [ ] Card meta (Python / Updated Aug 2026) gray, readable
- [ ] Border radius 14px (softer than typical 8px)

**Commit:**

```bash
git add index.html
git commit -m "style: add project card component"
```

---

## Task 5: Add About and Footer styles

**File:** `index.html`

Append to `<style>`:

```css
/* About */
.about{
  padding:120px 0 80px;
}
.about p{
  margin-bottom:20px;
  color:#a4a4ae;
  max-width:65ch;
}

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
footer span{
  color:#a4a4ae;
  font-size:.9rem;
}
.footer-links{display:flex;gap:24px}
.footer-links a{
  color:#a4a4ae;
  text-decoration:none;
  font-size:.9rem;
  transition:color .15s;
}
.footer-links a:hover{color:#0F7A52}

@media(max-width:768px){
  .about{padding:80px 0 60px}
  footer .container{flex-direction:column;gap:16px;text-align:center}
}
```

**Verify:**

- [ ] About section: "About" heading + two paragraphs
- [ ] About text max-width ~65ch, left-aligned
- [ ] Footer: copyright left, links right
- [ ] Footer links hover green
- [ ] Mobile: footer stacks vertically, centered

**Commit:**

```bash
git add index.html
git commit -m "style: add about section and footer"
```

---

## Task 6: Add dark mode support

**File:** `index.html`

Append to `<style>`:

```css
/* Dark Mode */
@media(prefers-color-scheme:dark){
  body{background:#141418;color:#f4f4f6}
  
  .top-nav{border-color:#2a2a32}
  .logo,.nav-links a{color:#f4f4f6}
  .nav-links a:hover{color:#3FBF88}
  
  .eyebrow{color:#3FBF88}
  .tagline{color:#9a9aa2}
  
  .btn-primary{background:#3FBF88;color:#141418}
  .btn-primary:hover{background:#50C998}
  .btn-secondary{
    background:#1a1a20;
    color:#f4f4f6;
    border-color:#2a2a32;
  }
  .btn-secondary:hover{border-color:#3FBF88}
  
  .project-card{
    background:#1a1a20;
    border-color:#2a2a32;
    color:#f4f4f6;
  }
  .project-card:hover{
    border-color:#3FBF88;
    background:#1c1c22;
  }
  .card-desc,.card-meta{color:#9a9aa2}
  .tag{
    background:rgba(63,191,136,.12);
    color:#3FBF88;
  }
  
  .about p{color:#9a9aa2}
  
  footer{border-color:#2a2a32}
  footer span,.footer-links a{color:#9a9aa2}
  .footer-links a:hover{color:#3FBF88}
}
```

**Verify:**

Toggle system dark mode (macOS: System Prefs → Appearance, or browser dev tools):

**Dark mode ON:**
- [ ] Body background dark `#141418`
- [ ] Text white `#f4f4f6`
- [ ] Accent color changed to lighter green `#3FBF88`
- [ ] Primary button: light green bg, dark text (reversed)
- [ ] Card dark background, light green border on hover
- [ ] Tag has semi-transparent green background

**Light mode ON:**
- [ ] Verify all previous light-mode checks still pass
- [ ] Strong contrast maintained (WCAG AA)

**Commit:**

```bash
git add index.html
git commit -m "style: add dark mode support"
```

---

## Task 7: Add entrance animation

**File:** `index.html`

Add before `</body>`:

```html
<script>
if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
  const observer = new IntersectionObserver(entries => {
    entries.forEach((entry, i) => {
      if (entry.isIntersecting) {
        entry.target.style.animation = `fadeInUp .5s cubic-bezier(.16,1,.3,1) ${i * 60}ms both`;
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });
  
  document.querySelectorAll('.hero-left > *, .project-card').forEach(el => {
    observer.observe(el);
  });
}
</script>
```

**File:** `index.html`

Append to `<style>`:

```css
/* Animation */
@keyframes fadeInUp{
  from{opacity:0;transform:translateY(12px)}
  to{opacity:1;transform:translateY(0)}
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

**Normal motion:**
- [ ] Hard-reload page (Cmd+Shift+R)
- [ ] Left column items fade in sequentially
- [ ] Card fades in after left items
- [ ] Total duration ~500ms

**Reduced motion:**
- [ ] Enable in system prefs or browser (macOS: Accessibility → Display → Reduce motion)
- [ ] Reload page
- [ ] All content appears instantly, no fade

**Commit:**

```bash
git add index.html
git commit -m "feat: add entrance animation with reduced-motion support"
```

---

## Task 8: Final visual QA

Open `index.html` and manually verify all requirements:

**Desktop (≥1024px width):**
- [ ] Hero split: left text / right card, vertically centered
- [ ] Card hover: border green `#0F7A52`, subtle bg change
- [ ] Button active: scale down
- [ ] Eyebrow green, uppercase, small
- [ ] About section max 65ch, left-aligned
- [ ] Footer: no version/build/weather strings
- [ ] Entrance animation works (if motion not reduced)

**Mobile (<768px width):**
- [ ] Hero single column: text top, card below
- [ ] Buttons wrap if needed
- [ ] Footer stacks vertically
- [ ] No horizontal scroll

**Dark mode (both desktop & mobile):**
- [ ] All colors swap correctly
- [ ] Accent changes to `#3FBF88`
- [ ] Readability maintained

**Accessibility:**
- [ ] Tab through all links (keyboard nav works)
- [ ] Focus rings visible
- [ ] Open browser dev tools → Lighthouse
- [ ] Run accessibility audit
- [ ] Contrast issues: 0 (or explain any exceptions)

**Spec compliance check:**
- [ ] Border-radius only uses 6px, 9px, 14px
- [ ] Accent color appears in exactly 3 contexts: eyebrow, primary button, tag background
- [ ] No animation library script tags
- [ ] No em-dash (—) anywhere in visible text
- [ ] No eyebrow on "About" section (it's a plain h2)

If any check fails, fix before committing.

**Commit (if fixes made):**

```bash
git add index.html
git commit -m "fix: address final QA issues"
```

---

## Task 9: Push to GitHub Pages

**Commands:**

```bash
git push origin main
```

Wait ~1 minute for GitHub Pages to deploy.

**Verify live site:**

Visit `https://harnessyoung.github.io/`

- [ ] Page loads
- [ ] Links work (personal-skills, GitHub, email)
- [ ] Dark mode works
- [ ] Mobile responsive
- [ ] No console errors

---

## Post-Implementation Notes

**Adding a second project:**

Duplicate the `.project-card` block inside `.hero-right`:

```html
<div class="hero-right">
  <a href="..." class="project-card"><!-- first project --></a>
  <a href="..." class="project-card" style="margin-top:20px"><!-- second project --></a>
</div>
```

Add this CSS:

```css
.hero-right{display:flex;flex-direction:column;gap:20px}
```

**When reaching 4+ projects:**

Add an `ALL PROJECTS` section between hero and about:

```html
<section class="all-projects">
  <div class="container">
    <h2>All Projects</h2>
    <div class="project-grid">
      <a href="..." class="project-card compact">
        <h3>Project Name</h3>
        <div class="card-meta"><!-- meta --></div>
        <div class="card-tags"><!-- tags --></div>
      </a>
      <!-- More cards -->
    </div>
  </div>
</section>
```

Add CSS:

```css
.all-projects{padding:80px 0}
.project-grid{
  display:grid;
  grid-template-columns:repeat(auto-fit,minmax(320px,1fr));
  gap:20px;
}
.project-card.compact .card-desc{display:none}
```

**Maintenance:**
- Update "Updated Aug 2026" dates manually when projects change
- No skill-count maintenance needed (per spec decision)
- Always check both light and dark modes after color changes
