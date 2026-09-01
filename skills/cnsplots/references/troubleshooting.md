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

**Panels in a visual grid have ragged left edges** — expected: multipanel derives
each panel's reserve from its rendered y tick label width, so differing
magnitudes shift the axes. Do not fix it with `pad_left` (it adds to the reserve)
or `ax.set_position()` (reverted on save). Use a single host panel subdivided
with `fig.add_gridspec()`; see
[composition-patterns.md](composition-patterns.md).

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
`python3 scripts/dump_style.py palettes`.

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
