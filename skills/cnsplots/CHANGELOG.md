# Changelog — cnsplots skill

All notable changes to this skill. Versioning is [SemVer](https://semver.org/)
applied to the *skill*, independent of the `cnsplots` package version.

## [1.5.0] — 2026-09-01

Documents multipanel's self-correcting layout mechanism, and corrects two
over-absolute claims from earlier versions.

### Added
- `references/composition-patterns.md` gains a section on the `draw_event` /
  `_on_draw` relayout loop: why it exists (decoration widths are only knowable
  after rendering), that `panel()` connects it automatically and it is
  multipanel-only, that `_on_draw` is private and silently no-ops if called with
  a fake event, and that `cns.savefig()` already triggers it so no manual call is
  needed.
- The same section explains why `tight_layout` is **not** the analogue: the two
  optimize opposite things. `tight_layout` resizes axes inside a fixed figure,
  while `_on_draw` keeps axes at exactly the requested pixel size (150x90
  requested renders as 150.0x90.0) and adjusts the figure around them.
- `references/troubleshooting.md` adds the `tight_layout` incompatibility
  warning and the "geometry looks wrong before the first draw" case.

### Fixed
- **`fig.tight_layout()` on a multipanel figure was described as destroying
  panel sizes. It does not — it is a no-op.** Panel axes are placed with explicit
  coordinates and have no `SubplotSpec`, so `tight_layout` skips them and warns;
  measured bounds are identical before and after, with the handler connected or
  disconnected. The advice to omit it stands, but because it is useless rather
  than harmful.
- **`ax.set_position()` was described as unconditionally reverting on save.**
  More precisely, it is discarded when the next draw remeasures the layout, and
  whether a given draw does so depends on what changed: y tick `labelsize`
  trips a remeasure (reserve 40.9 to 47.2), whereas replacing the y-axis label
  *text* does not, since that label is rotated 90 degrees and its width follows
  font size rather than string length. One configuration reverted to new values,
  another to the original ragged ones. The override never survives; the specific
  outcome is not predictable.
- `below=` raggedness is now described as proportional to the y tick label width
  difference rather than as a blanket defect: about 19 px at magnitudes 1 vs 1e5,
  but roughly 4 px at 1 vs 1e6 vs 10 with a shared title. `below=` is fine where
  panels share tick formatting; only guaranteed edge alignment requires the
  host-panel plus `GridSpec` pattern.

### Verified
Against `cnsplots` 0.7.0 on Python 3.12.14 / matplotlib 3.10.9. See
`skill.json` → `verification`.

## [1.4.0] — 2026-09-01

Adds cross-panel color strategy guidance, driven by auditing the showcase's
palette choices and measuring what actually happens to a shared category across
panels.

### Added
- `references/color-strategy.md` — how to keep one variable on one color across
  panels, qualitative vs sequential vs diverging, color-vision and greyscale
  legibility checks, and why the showcase's variety is the wrong model to copy.
  Every code sample verified to run.
- `scripts/dump_style.py greyscale` — prints each palette entry's Rec. 601 luma
  and flags pairs within 0.10, which collapse in greyscale. The default
  `Ecotyper1` has several: entries 4 and 6 differ by 0.005 luma.

### Changed
- `SKILL.md` adds the one-palette/one-color-per-meaning rule to the guidelines,
  and expands the visual check to include greyscale and cross-panel color
  consistency.
- `references/dense-figures.md` adds a note that the showcase is a palette
  catalog, not a color-consistent figure, with a pointer to the strategy
  reference.
- `references/troubleshooting.md` gains three color entries: indistinguishable
  colors, inconsistent color for the same category across panels, and misleading
  diverging colormap when the scale is not centered.
- `references/plot-catalog.md` notes which color constants sit outside
  `Ecotyper1`, and links to the color strategy reference.

### Notes
Audited every `color_cycle=` and `cmap=` in the vendored showcase source.
Figure 1 uses **eight different palettes across 18 panels**, and four panels plot
iris `species` in four different colors: `setosa` is `#662506` (all species
identical under `CHOCOLATE`), `#d13570` (`Ecotyper3`), `#d6372e` (`Ecotyper1`),
and `#e41a1c` (`Set1`). That is a feature catalog, not a publication figure; in a
real figure inconsistent color is a defect.

Verified two control mechanisms: same palette + explicit `hue_order` gives
bit-identical colors across panels, and an explicit color list plus a matching
`hue_order` pins specific colors regardless of who else is present. Both tested
on scatterplot and kdeplot pairs.

### Verified
Against `cnsplots` 0.7.0 on Python 3.12.14 / matplotlib 3.10.9. See
`skill.json` → `verification`.

## [1.3.0] — 2026-09-01

Vendors the upstream showcase source as reference material, and tightens the
dense-figure template to match its packing density.

### Added
- `templates/upstream-showcase/figure1.py` and `figure2.py` — the upstream
  showcase source, copied verbatim and unmodified, with a `README.md` explaining
  provenance and the two caveats observed at 0.7.0. A distilled description can
  drift from what the author wrote; these files are authoritative over our prose.
  Both verified to run standalone.

### Changed
- `templates/dense_figure.py` reworked from 9 panels to 14 in three interlocked
  bands. Density is now measured rather than asserted, as the fraction of interior
  all-empty pixel rows: upstream Figure 1 is 4.77%, Figure 2 is 5.44%, and this
  template went from **7.96% to 4.22%**.
- `references/dense-figures.md` leads with the finding that made the difference:
  packing density comes from stacking short panels into a tall neighbour's
  vertical band with `below=`, not from shaving margins. Both showcase figures use
  three such stacks; the earlier template used none. Includes the whitespace
  measurement as a reusable acceptance check.

### Notes
The earlier template's real defect was a 62-px sliver band, caused by a `below=`
stack whose subtree height did not match its neighbours' and so was pushed onto
its own row. The stack's subtree height, not the individual panel heights, sets
the row.

### Verified
Against `cnsplots` 0.7.0 on Python 3.12.14 / matplotlib 3.10.9. See
`skill.json` → `verification`.

## [1.2.0] — 2026-09-01

Adds dense journal-figure technique, derived from reproducing the upstream
showcase (<https://cnsplots.farid.one/latest/examples/showcase.html>) end to end
and verifying each technique independently.

### Added
- `references/dense-figures.md` — building a 15-to-20-panel figure: per-panel
  palettes, negative `pad_*` / `margin_*` to reclaim reserved space, embedded
  raster images, composite plotter internal axes, embedding a detached
  `upsetplot`, and reworking generated annotations and legends.
- `templates/dense_figure.py` — runnable dense figure on the packaged showcase
  data, with a `report_bands()` helper that prints the row structure on save so a
  silent wrap is visible without opening the file.

### Changed
- `scripts/dump_style.py` probes the full palette set. `cns.palettes()` accepts
  27 names, including `NEJM`, `BlueRed`, `parula`, and the `*_custom` diverging
  maps, and rejects plain matplotlib colormap names (`gnuplot`, `viridis`,
  `Blues`). The previous list understated this.
- `references/plot-catalog.md` records that wider palette set and the composite
  plotter axes attributes.
- `references/composition-patterns.md` and `references/troubleshooting.md` gain
  the composite plotter findings: `dotplot` honors `ax=` and stays inside its
  panel, `upsetplot` accepts `ax=` but overflows it, `hm_ax` and `ax_heatmap` are
  different objects, and the `legend_*` nudges are absolute and do not rescale.
- `SKILL.md` adds a fifth row to the layout table for full journal figures.

### Notes
Two findings worth recording. Row membership cannot be read from `y0` or `y1`:
panels of differing heights share a row while agreeing on neither edge, so both
report false wraps. Grouping by vertical overlap reproduces multipanel's internal
grouping and is what `report_bands()` does. And the showcase's
`cns.utils._capture_detached_axes_layout` call is private and not needed: the
public rescale works when performed after every `mp.panel()` call, and the
private tracking is inexact anyway (adding a later panel moved the host `+0.334`
in figure coordinates while the embedded axes moved `+0.200`).

### Verified
Against `cnsplots` 0.7.0 on Python 3.12.14 / matplotlib 3.10.9. See
`skill.json` → `verification`.

## [1.1.0] — 2026-09-01

Adds the style contract and layout composition guidance; re-verified against
`cnsplots` 0.7.0.

### Added
- `references/rcparams.md` — the rcParams `setup_matplotlib()` applies, measured
  as a live before/after diff, plus rules for custom artists (inherit rather than
  restate) and the 72-dpi pixel sizing contract.
- `references/settings-catalog.md` — every `cns.settings` field, grouped by
  purpose, generated from the installed package.
- `references/composition-patterns.md` — when to use a matplotlib grid,
  `cns.multipanel`, or a `GridSpec` inside a host panel, with measurements
  showing multipanel does not align panel edges.
- `references/style-bridge.md` — `setup_matplotlib` / `setup_ax` / `figure`
  responsibilities and four integration patterns for matplotlib, seaborn,
  scanpy, and plotnine.
- `scripts/dump_style.py` — dumps measured rcParams, settings, accepted palette
  names, and color constants; also regenerates the reference tables.
- `templates/mpl_grid_repeat.py`, `templates/multipanel_heterogeneous.py`,
  `templates/mixed_grid_in_panel.py` — each runs unmodified on a built-in
  dataset. Plain Python rather than Jinja2, since the skill has no render step.

### Fixed
- `references/troubleshooting.md` told agents to call `cns.take_legend_out(ax)`.
  `ax` is keyword-only, so the axes bound to `title` and the legend title
  silently became the axes repr string. Now `take_legend_out(ax=ax)` throughout.

### Changed
- `SKILL.md` gains a layout-selection step before the build step, a warning that
  `cns.figure()` applies the whole style and returns `None`, a rule against
  hardcoding values the package already sets, and a stronger validation step: a
  zero exit code is not evidence the figure is correct.
- Statistical integrity now covers functions that annotate a test nobody
  requested: `kdeplot` with a two-level `hue` runs a two-sample
  Kolmogorov-Smirnov test that `add_mode=False` does not suppress.
- `references/plot-catalog.md` updated to the 0.7.0 public surface, with probed
  qualitative palette names and the return-type and keyword-only caveats.
- `references/troubleshooting.md` adds nine measured failure modes: silent
  multipanel row wrap, ragged panel edges, rotated labels colliding with the
  panel below, unrequested p-values, `RuntimeError: Wrong Choice!` from passing a
  sequential colormap to `palettes()`, `None` returns, transparent-background
  previews, clobbered styles, and the `inset_axes` tuple-`loc` draw-time crash.

### Verified
Against `cnsplots` 0.7.0 on Python 3.12.14 / matplotlib 3.10.9. Every published
value is measured from the installed package rather than transcribed. See
`skill.json` → `verification`.

## [1.0.0] — 2026-08-12

Initial release. Derivative enhancement of the upstream skill bundled in
[faridrashidi/cnsplots](https://github.com/faridrashidi/cnsplots)
(`src/cnsplots/_agent_skill/cnsplots`, BSD-3-Clause).

### Added relative to upstream
- `scripts/check_env.py` — interpreter, package version, backend, and `mutool` probe.
- `scripts/inspect_api.py` — prints installed signatures/docstrings; `--list` dumps public API.
- `scripts/validate_output.py` — verifies artifact existence, size, magic bytes, and
  counts SVG `<text>` elements to catch text-outlined output.
- `references/troubleshooting.md` — 13 documented failure modes.

### Changed relative to upstream
- Replaced the ad-hoc heredoc introspection step with a bundled script.
- Expanded the plot catalog with a table layout, palette names, and explicit
  notes on functions that do not return a plain matplotlib `Axes`.

### Verified
Against `cnsplots` 0.6.0 on Python 3.12.13. See `skill.json` → `verification`.
