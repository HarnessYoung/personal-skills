# Upstream showcase source (vendored, unmodified)

Verbatim source of the two showcase figures from the cnsplots documentation:
<https://cnsplots.farid.one/latest/examples/showcase.html>

- `figure1.py` — 18 panels, all plot types, `max_width=485`
- `figure2.py` — 13 panels including micrographs, composite plotters, and an
  embedded upsetplot, `max_width=540`

Copyright Farid Rashidi, BSD-3-Clause, same terms as the cnsplots package. These
files are **reference material, not our work**. They are vendored here because a
distilled description can drift from what the author actually did; when the two
disagree, these files win.

## Reading them

`references/dense-figures.md` explains the techniques; `templates/dense_figure.py`
is a smaller runnable adaptation. Come here when you need to see the real thing:
the exact offsets used to interlock panels of different heights, and the full
sequence of annotation rework.

## Running them

Both need `include_showcase_images=True` data that ships with the package:

```bash
cd /tmp && python3 <path-to-skill>/templates/upstream-showcase/figure1.py
```

Output goes to `$CNSPLOTS_GALLERY_OUTPUT_DIR` or the current directory. Verified
against cnsplots 0.7.0: both run and produce their SVG.

Two caveats observed when reproducing them at 0.7.0, neither a bug in the source:

- `figure1.py` panel R renders with **overlapping heatmap legends**. The
  `legend_hpad` / `legend_hgap` / `legend_width` values are absolute nudges tuned
  for the docs build; they do not rescale across font or size differences. Re-tune
  rather than copying them.
- `figure2.py` calls `cns.utils._capture_detached_axes_layout`, a private
  function. The public rescale in `dense_figure.py` is sufficient when performed
  after every `mp.panel()` call. Prefer the public form in new code.
