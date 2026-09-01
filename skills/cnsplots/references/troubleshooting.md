# cnsplots troubleshooting

**`ModuleNotFoundError: No module named 'cnsplots'`** — not installed in the
active interpreter. Confirm with `python3 scripts/check_env.py`, then ask the
user before `python3 -m pip install cnsplots`. Watch for venv mismatch.

**Backend / display errors, or the process hangs** — set the backend before any
plotting import:

```python
import matplotlib
matplotlib.use("Agg")
import cnsplots as cns
```

or export `MPLBACKEND=Agg`.

**Figure is blank or tiny** — `width`/`height` are pixels. `cns.figure(6, 4)`
gives a 6x4 *pixel* canvas. Use realistic values like `cns.figure(180, 150)`.

**Figure looks blank in a dark viewer** — `settings.savefig_transparent` is
`True`, so there is no background. Set
`cns.settings.savefig_transparent = False` for previews, or open the file over
white.

**`AttributeError: 'NoneType' object has no attribute ...` after `cns.figure()`**
— `cns.figure()` returns `None`; it creates and styles the current figure. Use
`fig = plt.gcf()`. Same for `setup_matplotlib()`, `setup_ax()`, and
`take_legend_out()`, which all return `None`.

**Multipanel produced more rows than expected** — `max_width` is compared
against each panel's *total* width, which is
`margin_left + decoration reserve + width + margin_right`, not the `width=` you
passed. With `panel_margin_right` defaulting to `10`, panels of 150 and 300 px
needed `max_width=520`, not 500. Nothing warns. Compare panel `y0` values to see
which panels actually share a row.

**Row check reports panels on separate rows that clearly share one** — you
grouped by `y0` or `y1`. Panels of differing heights share a row while agreeing on
neither edge. Group by vertical overlap; see `report_bands()` in
`templates/dense_figure.py`.

**An `upsetplot` spills outside its panel** — it accepts `ax=` but does not
confine itself to it. Let it lay out with `fig=mp.fig`, then rescale its returned
axes into the host rectangle after all panels exist. Recipe in
[dense-figures.md](dense-figures.md). Its dict has a `totals` key that is `None`
when `totals_plot_elements=0`, so filter `None` before iterating.

**`heatmapplot` or `dotplot` legends overlap each other or the next panel** —
`legend_hpad`, `legend_vpad`, `legend_hgap`, `legend_vgap`, `legend_width` are
absolute nudges tuned for one figure size and font. They do not rescale. Re-tune
them after any geometry change and confirm visually; a value copied from another
figure will usually collide.

**Composite plotter title appears twice or in the wrong place** — `dotplot` and
`heatmapplot` expose several internal axes, and `hm_ax` is not the same object as
`ax_heatmap` even when they share a rectangle. Blank the built-in title with
`dp.ax_heatmap.set_title("")` and set your own on `dp.hm_ax`.

**Image panel has thick white margins** — the panel aspect ratio does not match
the image, so `imshow` letterboxes it. Size the panel to the image, and reclaim
the unused decoration space with a negative `pad_left` since an image axes has no
ticks or y-label.

**Panels in a visual grid have ragged left edges** — expected: multipanel derives
each panel's reserve from its rendered y tick label width, so differing
magnitudes shift the axes. Do not fix it with `pad_left` (it adds to the reserve)
or `ax.set_position()` (discarded by the next relayout). Use a single host panel subdivided
with `fig.add_gridspec()`; see
[composition-patterns.md](composition-patterns.md).

**`UserWarning: This figure includes Axes that are not compatible with
tight_layout`** — `tight_layout()` was called on a `multipanel` figure. Panel axes
are positioned explicitly and have no `SubplotSpec`, so `tight_layout` skips them
entirely: measured panel bounds are identical before and after. It is a harmless
no-op, but drop the call. `multipanel` already self-corrects through its
`draw_event` handler, and `tight_layout` belongs to the `plt.subplots` path. See
[composition-patterns.md](composition-patterns.md).

**Panel geometry looks wrong when read right after plotting** — the decoration
reserve is measured during a draw, so before the first draw it is `0.0` and the
axes sits at its uncorrected position. Call `mp.fig.canvas.draw()` before reading
`get_position()`. You do not need it before `cns.savefig()`, which draws
internally.

**`TypeError: list indices must be integers or slices, not tuple` when saving** —
`inset_axes(..., loc=(x, y))` was given a tuple; `loc` must be an int or a known
string. The error surfaces at draw time, not construction. Use `GridSpec` for
grid layouts instead of insets.

**`AttributeError` on the returned object** — `heatmapplot`, `dotplot`,
`vennplot`, and `upsetplot` do not return a plain `Axes`. Inspect with
`type(result)` and reach for the matplotlib axes through the returned object or
`plt.gca()`.

**`TypeError: unexpected keyword argument`** — the signature changed between
releases. Run `python3 scripts/inspect_api.py <function>` and match the
installed signature instead of copying older examples.

**Clipped labels or overlapping ticks** — increase panel width/height, rotate
tick labels via the returned axes (`ax.tick_params(axis="x", rotation=45)`),
shorten category names, or move the legend out with
`cns.take_legend_out(ax=ax)`.

**Legend overlaps the data** — `cns.take_legend_out(ax=ax)`, or widen the canvas
so the legend has dedicated space.

**Legend title became `Axes(0.125,0.11;0.775x0.77)`** — `take_legend_out(ax)` was
called positionally. The signature is `take_legend_out(title=None, *, ax=None)`,
so the axes bound to `title`. Nothing raises. Always write
`cns.take_legend_out(ax=ax)`.

**Rotated tick labels collide with the panel below** — a multipanel panel's
decoration reserve does not grow enough for steeply rotated labels. Add
`margin_bottom=` to the upper panel. Measured with 30-degree rotated species
names: `margin_bottom=15` still overlapped, `30` cleared it. Prefer shortening
category names over rotating them.

**An unrequested `P = ...` appeared on the figure** — some functions test
automatically. `cns.kdeplot` with a two-level `hue` runs a two-sample
Kolmogorov-Smirnov test and annotates it; `add_mode=False` does not disable it,
and three or more levels produce no annotation. Inspect `ax.texts`, then either
report that test by name in the caption or remove it deliberately:

```python
for text in list(ax.texts):
    if text.get_text().startswith("$P"):
        text.remove()
```

**Missing statistical annotations** — pass `pairs=[("A", "B")]` or `pairs="all"`
on functions that support it. The p-value method is printed to stdout; capture
it for the figure legend.

**SVG text became outlines, or the warning about `mutool`** — install MuPDF
(`brew install mupdf-tools`) for Illustrator-optimized SVG post-processing.
Without it, output is a standard matplotlib SVG.

**Missing glyphs / CJK or unicode boxes** — call `cns.apply_unicode_font()` or
supply a font that covers the characters.

**Global style leaked into later figures** — wrap overrides in
`with cns.settings.context(...):` instead of assigning to `cns.settings`.

**Colors indistinguishable** — switch `color_cycle` (`Ecotyper1`, `Cell`,
`Nature`, `Science`, `Set1`) and check greyscale/color-vision legibility for
categorical series. List the accepted names with
`python3 scripts/dump_style.py palettes`. Red-green pairs are the usual
offender: prefer blue-orange for a two-level contrast, or add a non-color
channel.

**The same category is a different color in different panels** — the hue order
came from each panel's data, so a panel missing a category shifts every color
after it. Define the order once and pass `hue_order=` on every panel that shares
the variable. For a subset panel, also pass a matching `color_cycle` built from
your category-to-color map. See [color-strategy.md](color-strategy.md).

**Diverging colormap looks misleading** — the scale is not centered, so the
midpoint color sits at an arbitrary value. Set `vmin`/`vmax` symmetrically about
the meaningful midpoint (usually 0) whenever you use `BuRd_custom`,
`OrBu_custom`, or `BlueRed` for signed values.

**`RuntimeError: Wrong Choice!` from `cns.palettes()`** — a sequential colormap
name was passed to a qualitative-palette function. `settings.palette_seq`
defaults to `'gnuplot'`, which `cns.palettes()` rejects. For continuous data use
`color_map=` on `cns.figure()` / `mp.panel()`, or `plt.get_cmap(name)`.

**Custom artist ignores the journal style** — you passed the property
explicitly. `fontsize=`, `frameon=`, `linewidth=` on spines, and
`tick_params(width=)` all override rcParams that cnsplots set. Omit them, or
read the value from `mpl.rcParams` / `cns.settings`. See
[rcparams.md](rcparams.md).

**Style silently reverted mid-script** — something called
`plt.style.use(...)` or `mpl.rcParams.update(mpl.rcParamsDefault)` after the
cnsplots setup, or another library reset the defaults on import. Check
`mpl.rcParams["axes.linewidth"]`: `0.5` means the style is active, `0.8` means it
was clobbered. Re-apply with `cns.setup_matplotlib()`.

**Labels shift between machines** — `font.sans-serif` is Helvetica-first with a
DejaVu Sans fallback. The fallback has different metrics, and multipanel measures
rendered decoration widths, so panel geometry differs where Helvetica is absent.

**Survival results look inverted** — verify the event column codes 1 = event,
0 = censored, and confirm the reference group and time units with the user.
