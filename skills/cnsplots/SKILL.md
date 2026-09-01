---
name: cnsplots
description: Generate, revise, and debug publication-quality scientific figures in Python with the cnsplots package (Cell/Nature/Science styling, pixel-exact sizing, built-in statistical annotations, editable SVG/PDF export). Also covers applying the cnsplots style to plain matplotlib, seaborn, or scanpy axes, repeated grid panels, heterogeneous multi-panel layouts, and the rcParams contract for custom artists. Use when a user asks for cnsplots code, journal-style plots, multi-panel or grid figures, survival/volcano/GSEA/ROC/heatmap plots, or Illustrator-editable vector figure output.
---

# cnsplots

Produce a runnable script that plots the user's real data with `cnsplots` and
saves a verified artifact. Never hand back untested plotting code.

Docs: <https://cnsplots.farid.one/latest/api.html> · Gallery:
<https://cnsplots.farid.one/latest/examples/index.html>

## Bundled scripts

The helper scripts live next to this file. Invoke them with paths relative
to this skill's directory (written as `$SKILL_DIR` below), not the user's
project root:

- `$SKILL_DIR/scripts/check_env.py` — environment and dependency probe
- `$SKILL_DIR/scripts/inspect_api.py` — installed signatures and docstrings
- `$SKILL_DIR/scripts/dump_style.py` — measured rcParams, settings, palettes, colors
- `$SKILL_DIR/scripts/validate_output.py` — post-save artifact validation

## Bundled templates

Each runs unmodified on a built-in dataset, then adapts via its `CONFIGURE`
block. Start from one instead of writing a layout from scratch:

- `$SKILL_DIR/templates/mpl_grid_repeat.py` — uniform grid, one plot type
- `$SKILL_DIR/templates/multipanel_heterogeneous.py` — labeled A/B/C figure
- `$SKILL_DIR/templates/mixed_grid_in_panel.py` — aligned grid inside a labeled figure
- `$SKILL_DIR/templates/dense_figure.py` — showcase-style dense figure: per-panel
  palettes, negative offsets, embedded image, composite plotters, embedded upsetplot

## Hard rules

- `import cnsplots as cns` and use only public `cns.*` names. Never import
  `cnsplots._utils`, `cnsplots.plots._distribution`, or any other private module.
- Verify every function signature against the *installed* version before writing
  final code (step 2). The API changes between releases; do not trust memory.
- Sizes in `cns.figure()` / `mp.panel()` are **pixels at 72 per inch**, not
  inches. Rendering happens at 144 dpi, so a 200-px figure rasterizes to 400 px.
- Never invent data, labels, units, group orders, thresholds, or statistical
  tests. If a choice changes scientific meaning and cannot be inferred, ask.
- Never hardcode a style value the package already sets. Inherit it, or read it
  from `mpl.rcParams` / `cns.settings`. See
  [references/rcparams.md](references/rcparams.md).
- Do not build a visual grid by calling `mp.panel()` per cell; multipanel does
  not align panel edges. See
  [references/composition-patterns.md](references/composition-patterns.md).
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

### 3. Choose the layout before writing code

Four cases. Getting this wrong costs a rewrite, because the layout engines are
not interchangeable.

| Figure | Approach | Start from |
| --- | --- | --- |
| One panel | `cns.figure(width=, height=)` | baseline below |
| Same plot repeated, uniform cells | `cns.figure()` + `fig.subplots()` | `templates/mpl_grid_repeat.py` |
| Different sizes/types, A/B/C labels | `cns.multipanel()` + `mp.panel()` | `templates/multipanel_heterogeneous.py` |
| Heterogeneous **and** a repeated block | one host `mp.panel()` + `fig.add_gridspec()` | `templates/mixed_grid_in_panel.py` |
| Full journal figure: many panels, images, composite plotters | `cns.multipanel()` + hand-tuned offsets | `templates/dense_figure.py` |

`multipanel` sizes each panel from its *rendered* axis decorations, so panels
whose y tick labels differ in width get different axes left edges. Measured:
three `below=`-stacked panels at y magnitudes 1, 1e5, 10 landed at
`x0 = 0.065 / 0.114 / 0.075`. `below=` groups panels vertically; it does not
align them. Forcing it with `ax.set_position()` is reverted on save by
multipanel's draw handler. When edges must line up, use the host-panel plus
`GridSpec` pattern. Full reasoning and measurements:
[references/composition-patterns.md](references/composition-patterns.md).

### 4. Build the figure

```python
import matplotlib

matplotlib.use("Agg")  # required for headless runs

import cnsplots as cns

cns.figure(width=180, height=150, color_cycle="Ecotyper1")
ax = cns.boxplot(data=df, x="group", y="value", pairs=[("A", "B")])
ax.set(xlabel="Group", ylabel="Value (a.u.)")
cns.savefig("outputs/figure.svg")
```

- `cns.figure()` applies the full style **and** creates the figure; it returns
  `None`, so reach the figure with `plt.gcf()`. Do not also call
  `setup_matplotlib()`.
- Creating the figure yourself, or drawing with plain matplotlib, seaborn, or
  scanpy? Use `cns.setup_matplotlib()` first, or `cns.setup_ax(ax)` to retrofit
  existing axes. Patterns: [references/style-bridge.md](references/style-bridge.md).
- Titles and labels go through the returned matplotlib `Axes`. Pass no
  `fontsize`, `linewidth`, or `frameon`; every value you supply overrides the
  journal style.
- Temporary style changes: `with cns.settings.context(...):` — do not mutate
  global settings permanently.
- `cns.take_legend_out(ax=ax)` — `ax` is **keyword-only**. Written positionally
  it silently sets the legend *title* to the axes repr string.
- `heatmapplot` / `dotplot` return backend plotter objects, `vennplot` returns a
  matplotlib-venn object, `upsetplot` returns panel axes — not a plain `Axes`.
  Guard `.set(...)` calls accordingly.

### 5. Save and validate

```bash
python3 $SKILL_DIR/scripts/validate_output.py outputs/figure.svg
```

Prefer SVG or PDF for submission, PNG for preview. A clean script exit is not
evidence the figure is correct: every layout defect found while building this
skill (a silently wrapped multipanel row, tick labels crashing into the panel
below, an unrequested p-value annotation) exited zero and produced a valid file.

Render a PNG and look at it. `savefig_transparent` is `True` by default, so set
`cns.settings.savefig_transparent = False` for the preview or the figure may
look blank on a dark background. Check: text clipping, overlapping tick labels,
legend collisions, misleading or truncated axes, indistinguishable colors, panel
misalignment, and annotations you did not ask for.

For multipanel, confirm the row structure is what you intended. `max_width` must
exceed the sum of axes widths **plus** each panel's decoration reserve and
margins; otherwise a panel wraps to the next row with no warning. Measured: two
panels of 150 and 300 px needed `max_width=520`, not 500. Compare `y0` values to
verify which panels share a row.

### 6. Report

Return the full runnable script, the absolute output path, the palette/size
choices made, and every scientific assumption (tests, comparison direction,
event coding, transformations).

## Statistical integrity

- `pairs`, event codes, reference groups, transforms, and thresholds are
  analysis decisions. Surface them explicitly; never add them for decoration.
- Name the test actually used by the installed function's docstring (e.g.
  two-sided Mann-Whitney U for `boxplot`, Welch's t-test for `barplot`,
  Fisher's exact for `stackplot`), not an assumed one.
- **Some functions annotate a test you did not request.** `cns.kdeplot` with a
  two-level `hue` runs a two-sample Kolmogorov-Smirnov test and prints
  `P = ...` on the axes; `add_mode=False` does not suppress it, and with three
  or more levels no annotation appears. Always inspect `ax.texts` after
  plotting. Either report that test by name in the caption, or remove the
  annotation deliberately:

  ```python
  for text in list(ax.texts):
      if text.get_text().startswith("$P"):
          text.remove()
  ```
- Keep raw observations when requested; do not silently swap distributions for
  summary bars.
- Do not imply causality or significance beyond what the data and test support.

## Reference index

Load these on demand; do not read them all up front.

- [references/plot-catalog.md](references/plot-catalog.md) — pick a plot function
- [references/composition-patterns.md](references/composition-patterns.md) — grid
  vs multipanel, panel alignment, mixed layouts
- [references/dense-figures.md](references/dense-figures.md) — full journal
  figures: negative offsets, embedded images, composite plotter internals,
  reworking generated annotations
- [references/style-bridge.md](references/style-bridge.md) — matplotlib, seaborn,
  scanpy, and plotnine integration
- [references/rcparams.md](references/rcparams.md) — the rcParams contract; read
  before writing custom artists or hardcoding any style value
- [references/settings-catalog.md](references/settings-catalog.md) — every
  `cns.settings` field
- [references/troubleshooting.md](references/troubleshooting.md) — backend errors,
  blank figures, clipped labels, palette misuse, SVG font issues
