---
name: cnsplots
description: Generate, revise, and debug publication-quality scientific figures in Python with the cnsplots package (Cell/Nature/Science styling, pixel-exact sizing, built-in statistical annotations, editable SVG/PDF export). Use when a user asks for cnsplots code, journal-style plots, multi-panel figures, survival/volcano/GSEA/ROC/heatmap plots, or Illustrator-editable vector figure output.
---

# cnsplots

Produce a runnable script that plots the user's real data with `cnsplots` and
saves a verified artifact. Never hand back untested plotting code.

Docs: <https://cnsplots.farid.one/latest/api.html> · Gallery:
<https://cnsplots.farid.one/latest/examples/index.html>

## Bundled scripts

The three helper scripts live next to this file. Invoke them with paths relative
to this skill's directory (written as `$SKILL_DIR` below), not the user's
project root:

- `$SKILL_DIR/scripts/check_env.py` — environment and dependency probe
- `$SKILL_DIR/scripts/inspect_api.py` — installed signatures and docstrings
- `$SKILL_DIR/scripts/validate_output.py` — post-save artifact validation

## Hard rules

- `import cnsplots as cns` and use only public `cns.*` names. Never import
  `cnsplots._utils`, `cnsplots.plots._distribution`, or any other private module.
- Verify every function signature against the *installed* version before writing
  final code (step 2). The API changes between releases; do not trust memory.
- Sizes in `cns.figure()` / `mp.panel()` are **pixels**, not inches.
- Never invent data, labels, units, group orders, thresholds, or statistical
  tests. If a choice changes scientific meaning and cannot be inferred, ask.
- Always run the script and confirm the output file exists and is non-empty
  before reporting success.

## Workflow

### 1. Bootstrap the environment

```bash
python3 $SKILL_DIR/scripts/check_env.py
```

Reports the interpreter, `cnsplots` version, backend availability, and whether
`mutool` is present. If `cnsplots` is missing, ask before installing, then:

```bash
python3 -m pip install cnsplots     # or: uv pip install cnsplots
```

Without MuPDF's `mutool`, `cns.savefig("f.svg")` still works but falls back to
plain matplotlib SVG with a warning (no Illustrator post-processing).

### 2. Inspect the data, then the API

Print columns, dtypes, null counts, category levels, and event coding for the
real input. Then confirm the signature of each function you plan to call:

```bash
python3 $SKILL_DIR/scripts/inspect_api.py boxplot survivalplot multipanel
```

Pick the narrowest suitable function from
[references/plot-catalog.md](references/plot-catalog.md).

### 3. Build the figure

```python
import matplotlib

matplotlib.use("Agg")  # required for headless runs

import cnsplots as cns

cns.figure(width=180, height=150, color_cycle="Ecotyper1")
ax = cns.boxplot(data=df, x="group", y="value", pairs=[("A", "B")])
ax.set(xlabel="Group", ylabel="Value (a.u.)")
cns.savefig("outputs/figure.svg")
```

- Single panel: `cns.figure(width=..., height=...)`.
- Multi-panel: `mp = cns.multipanel(max_width=540)`, then
  `ax = mp.panel("A", width=150, height=150)` and pass `ax=ax` to each plot.
- Titles/labels go through the returned matplotlib `Axes`.
- Temporary style changes: `with cns.settings.context(...):` — do not mutate
  global settings permanently.
- `heatmapplot` / `dotplot` return backend plotter objects, `vennplot` returns a
  matplotlib-venn object, `upsetplot` returns panel axes — not a plain `Axes`.
  Guard `.set(...)` calls accordingly.

### 4. Save and validate

```bash
python3 $SKILL_DIR/scripts/validate_output.py outputs/figure.svg
```

Prefer SVG or PDF for submission, PNG for preview. Then visually check: text
clipping, overlapping tick labels, legend collisions, misleading or truncated
axes, indistinguishable colors, panel misalignment. Render the PNG and look at
it when image display is available.

### 5. Report

Return the full runnable script, the absolute output path, the palette/size
choices made, and every scientific assumption (tests, comparison direction,
event coding, transformations).

## Statistical integrity

- `pairs`, event codes, reference groups, transforms, and thresholds are
  analysis decisions. Surface them explicitly; never add them for decoration.
- Name the test actually used by the installed function's docstring (e.g.
  two-sided Mann-Whitney U for `boxplot`, Welch's t-test for `barplot`,
  Fisher's exact for `stackplot`), not an assumed one.
- Keep raw observations when requested; do not silently swap distributions for
  summary bars.
- Do not imply causality or significance beyond what the data and test support.

## Common failures

See [references/troubleshooting.md](references/troubleshooting.md) for backend
errors, blank figures, clipped labels, palette misuse, and SVG font issues.
