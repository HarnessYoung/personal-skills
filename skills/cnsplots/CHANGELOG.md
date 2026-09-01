# Changelog — cnsplots skill

All notable changes to this skill. Versioning is [SemVer](https://semver.org/)
applied to the *skill*, independent of the `cnsplots` package version.

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
