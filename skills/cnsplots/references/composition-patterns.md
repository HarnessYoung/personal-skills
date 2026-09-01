# Composition patterns

Three layout engines, three jobs. Picking the wrong one produces misaligned
panels that no amount of parameter tuning will fix.

| | matplotlib grid | `cns.multipanel` | grid inside a host panel |
| --- | --- | --- | --- |
| Panel sizes | uniform | per-panel | uniform within the grid |
| Cross-row/column alignment | guaranteed | **not guaranteed** | guaranteed |
| A/B/C labels | manual | automatic | automatic for the host |
| Layout flow | fixed rows x columns | wraps at `max_width` | fixed inside the host rect |
| Vertical stacking | rows | `below="A"` | rows |
| Per-panel palette | global only | `color_cycle=` | global only |
| Use for | one repeated plot | heterogeneous figure | heterogeneous + a repeated block |

## Decision rule

1. Every panel same size and same plot type, no other panels? **Pattern A**,
   matplotlib grid.
2. Panels differ in size or type, and you do not need them edge-aligned?
   **Pattern B**, `cns.multipanel`.
3. Both: a heterogeneous figure that contains a block of repeated panels?
   **Pattern C**, one host panel subdivided with `GridSpec`.

Never build a visual grid by calling `mp.panel()` once per cell. Read the next
section for why.

## Why multipanel does not align panels

`multipanel` sizes each panel as
`margin_left + left_reserve + width + margin_right`
(`_multipanels.py:440`), where `left_reserve` comes from
`_get_left_reserve_px()` (`:395`) and is derived from that panel's **actually
rendered** y-axis decoration width. Your `width=` constrains the axes only; the
panel's outer width is discovered at draw time.

Consequence: two panels whose y tick labels differ in width get different axes
left edges. Measured with three `below=`-stacked panels at y magnitudes 1, 1e5,
and 10, all `width=150`:

```
A: x0=0.06547
B: x0=0.11391
C: x0=0.07531
```

With identical magnitudes they agree exactly (`0.06547` for both). The same
applies to flow layout: six `140x100` panels forming a visual 3x2 grid gave
column-two left edges of `0.4622`, `0.4784`, `0.4461` across the three rows.

So `below=` stacks panels **vertically in the same column slot**, but does not
align their axes edges. Use it for semantic grouping where a few pixels do not
matter, or where the panels genuinely share tick formatting (a KM curve with its
risk table underneath).

Three fixes were tested; two do not work:

- Unify tick formatting with a shared `FuncFormatter`: gets to
  `0.11484 / 0.11484 / 0.115`. Close but not exact, and it forces one tick
  format on every panel.
- Hand-tune `pad_left`: `pad_left` is **added on top of** the measured reserve,
  not substituted for it, so the panels stay unequal.
- `ax.set_position()` after all panels exist: aligns correctly, then **reverts on
  save**. `multipanel.__init__` registers a `draw_event` handler (`:483` to
  `_on_draw` `:684`) that recomputes layout on every draw, and `savefig` draws.
  Measured before save `0.11391` for all three, after save
  `0.07141 / 0.12687 / 0.08266`.

Do not attempt to force alignment on multipanel axes. Use Pattern C.

## Pattern A: repeated grid, matplotlib

Uniform panels, one plot type, no heterogeneous neighbours.

```python
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import cnsplots as cns

groups = ["BRCA1", "TP53", "EGFR", "MYC", "KRAS", "PTEN"]
ncols = 3
nrows = -(-len(groups) // ncols)
panel_w, panel_h = 120, 100

cns.figure(width=ncols * panel_w, height=nrows * panel_h)
fig = plt.gcf()                       # cns.figure() returns None
axes = fig.subplots(nrows, ncols, squeeze=False)

for idx, name in enumerate(groups):
    ax = axes[idx // ncols][idx % ncols]
    cns.kdeplot(data=expr, x=name, hue="condition", ax=ax)
    ax.set_title(name)
    ax.set_xlabel("")

for idx in range(len(groups), nrows * ncols):
    axes[idx // ncols][idx % ncols].set_visible(False)

fig.tight_layout()
cns.savefig("grid.svg")
```

`cns.figure()` already applies the full style, so every subplot inherits it; do
not also call `setup_matplotlib()`. Panel letters, if needed, come from
`cns.add_panel_label("A")`, which labels the **current** axes and takes no `ax`
argument, so select the axes first with `plt.sca(ax)`.

`GridSpec` allots equal cells regardless of tick label width, so columns and rows
align exactly.

## Pattern B: heterogeneous figure, multipanel

Different sizes and plot types, automatic labels, alignment not required.

```python
import matplotlib

matplotlib.use("Agg")

import cnsplots as cns

mp = cns.multipanel(max_width=420, title="Cohort summary", loc="left")

ax_a = mp.panel("A", width=110, height=130)
cns.violinplot(data=iris, x="species", y="sepal_length", ax=ax_a)
ax_a.set_ylabel("Sepal length (cm)")

ax_b = mp.panel("B", width=180, height=130)
cns.scatterplot(data=iris, x="sepal_length", y="petal_length", hue="species", ax=ax_b)
cns.take_legend_out(title="Species", ax=ax_b)      # ax is keyword-only

ax_c = mp.panel("C", width=110, height=80, below="A")
cns.barplot(data=tips, x="day", y="total_bill", ax=ax_c)

cns.savefig("figure.svg")
```

- Panels flow left to right and wrap when the row exceeds `max_width`.
- `mp.newline()` forces a break by inserting a spacer that consumes the rest of
  the row.
- `below="A"` stacks under panel A instead of flowing.
- `mp.get_axes("A")` retrieves a panel's axes later; `mp.fig` is the figure.
- `panel_margin_bottom` and `panel_margin_right` default to `10`, so panels are
  not flush unless you pass `margin_*=0`.

## Pattern C: repeated grid inside a heterogeneous figure

One `mp.panel()` acts as a positioned, empty **host rectangle**. Its coordinates
become the bounds of a `GridSpec`, so matplotlib lays out the cells and
alignment is exact, while multipanel still draws the host's panel letter.

```python
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import cnsplots as cns

mp = cns.multipanel(max_width=520)

ax_a = mp.panel("A", width=150, height=110)
cns.boxplot(data=df, x="group", y="value", ax=ax_a)

host = mp.panel("B", width=300, height=110)          # grid host, stays empty

ax_c = mp.panel("C", width=150, height=90, below="A")
cns.barplot(data=df, x="group", y="value", ax=ax_c)

# All panels exist. Only now subdivide the host.
fig = mp.fig
fig.canvas.draw()                                     # let the layout settle
box = host.get_position()
host.set_axis_off()                                   # hide the empty frame

gs = fig.add_gridspec(2, 3, left=box.x0, right=box.x1,
                      bottom=box.y0, top=box.y1,
                      wspace=0.5, hspace=0.6)

for idx, name in enumerate(genes):
    ax = fig.add_subplot(gs[idx // 3, idx % 3])
    cns.boxplot(data=frames[name], x="group", y="value", ax=ax)
    cns.setup_ax(ax)
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_title(name)

cns.savefig("mixed.svg")
```

Measured with cell y magnitudes spanning 1 to 1e5: each column has a single
`x0`, each row a single `y0`, and the bounds are bit-identical before and after
`savefig`. The grid cells are not multipanel panels, so `_on_draw` never
repositions them.

Two ordering constraints, both load-bearing:

1. **Subdivide after every `mp.panel()` call.** Adding a panel afterwards
   re-flows the host; the already-placed grid stays put and ends up outside the
   host rectangle. Reproduced: adding panel C after subdividing moved host B to
   `y0=0.025` while the cells kept their old coordinates.
2. **Call `fig.canvas.draw()` before reading `host.get_position()`.** Before the
   first draw, the reserve is unmeasured and the rectangle is a provisional
   value.

`cns.setup_ax(ax)` on each cell is belt-and-braces: cells created with
`add_subplot` already inherit the active rcParams. Call it when the axes came
from a library that overrode them, and pass `colorbar_label=` explicitly if a
colorbar is present, since the default is `'FDR q-val'`.

### Do not use `inset_axes` for this

The `mpl_toolkits.axes_grid1.inset_locator.inset_axes` approach with a tuple
`loc` constructs without error and then **crashes at draw time**:

```
TypeError: list indices must be integers or slices, not tuple
```

`loc` must be an int or a recognized string. Even with a valid `loc`, insets are
anchored relative to the host axes with `borderpad` padding, which does not
produce a regular grid. `GridSpec` is the correct tool.

## Returned objects

Most plot functions return the target `Axes`. `heatmapplot` and `dotplot` return
backend plotter objects, `vennplot` a matplotlib-venn object, and `upsetplot`
panel axes. In grid loops, do not assume the return value is an `Axes`; pass
`ax=` and keep using your own reference. These composite plotters also manage
their own internal axes, so they cooperate poorly with a `GridSpec` cell.
