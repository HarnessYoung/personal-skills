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

**`AttributeError` on the returned object** — `heatmapplot`, `dotplot`,
`vennplot`, and `upsetplot` do not return a plain `Axes`. Inspect with
`type(result)` and reach for the matplotlib axes through the returned object or
`plt.gca()`.

**`TypeError: unexpected keyword argument`** — the signature changed between
releases. Run `python3 scripts/inspect_api.py <function>` and match the
installed signature instead of copying older examples.

**Clipped labels or overlapping ticks** — increase panel width/height, rotate
tick labels via the returned axes (`ax.tick_params(axis="x", rotation=45)`),
shorten category names, or move the legend out with `cns.take_legend_out(ax)`.

**Legend overlaps the data** — `cns.take_legend_out(ax)`, or widen the canvas so
the legend has dedicated space.

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
categorical series.

**Survival results look inverted** — verify the event column codes 1 = event,
0 = censored, and confirm the reference group and time units with the user.
