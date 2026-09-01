## [1.7.0] — 2026-09-01

Recommends overriding two installed defaults (`palette_seq='gnuplot'` and
Helvetica-first `font_sans_serif`) that conflict with journal requirements and
perceptual uniformity, and replaces the Rec. 601 luma approximation with rigorous
CIE L* measurements.

### Added
- `scripts/recommended_overrides.py` — explains why `palette_seq='viridis'` and
  Arial-first font order are recommended, with measured perceptual-uniformity
  reasoning. `--code` emits a ready three-line block to paste at script top.
- `scripts/dump_style.py` gains `colormap <name>` mode, which measures perceptual
  uniformity of a continuous colormap: CIE L* range, monotonicity, step-size
  coefficient of variation, descending-step count, and greyscale collisions (value
  pairs >0.1 apart in data space that fall within 1 L* and become
  indistinguishable when printed). Verified: `gnuplot` reports CV 0.66, 4
  descending steps, 39 collisions; `viridis` reports CV 0.07, 0 descending, 0
  collisions.
- Workflow section 2 in `SKILL.md` now mandates applying the overrides at the top
  of every plotting script, with the full reasoning inline.

### Changed
- **`scripts/dump_style.py greyscale` now uses CIE L*** (perceptual lightness)
  rather than Rec. 601 luma, and reports pairs within 5 L* rather than 0.10 luma.
  The Rec. 601 approximation is too crude: it reported `gnuplot` as monotonic when
  rigorous CIE L* shows it is non-monotonic with 4 descending steps and CV 0.66.
  `Ecotyper1` has 6 pairs within 5 L* (e.g. entries 0 and 3 differ by 0.4 L*,
  entries 2 and 6 by 0.2 L*), meaning those hues collapse in greyscale.
- `references/journal-specs.md` and `references/color-strategy.md` replace the
  incorrect "gnuplot is a rainbow" reasoning with measured CIE L* data: gnuplot is
  non-monotonic (CV 0.66, identical to the canonical counterexample `jet` at 0.65)
  and produces 39 value pairs separated by >0.1 in data space that collapse to
  within 1 L* in greyscale (e.g. data 0.19 and 0.43 render at L* 97.5 and 98.2).
  `viridis` is strictly monotonic (CV 0.07, zero collisions) and starts dark (L*
  14.9, readable on white). Both documents now recommend overriding
  `palette_seq='viridis'` at script top.
- `references/journal-specs.md` adds that the installed
  `settings.multipanel_max_width=540` (190.5 mm) exceeds all three journals'
  widest columns (Cell 174, Nature 183, Science 184), and that
  `font_sans_serif` prioritises Helvetica, which means Cell Press submissions
  embed Helvetica rather than the required Arial. Moving Arial to the front while
  keeping fallbacks ensures compliance without breaking on systems that lack Arial.
- `references/troubleshooting.md` adds "Quantitative heatmap looks misleading in
  greyscale" and notes that `multipanel_max_width=540` exceeds all journals.

### Rationale
The installed `palette_seq='gnuplot'` makes equal data steps look unequal and
collapses distinct values in greyscale, which is a **data integrity issue** rather
than a style preference. The installed `font_sans_serif` order means macOS users
silently submit Helvetica to Cell Press rather than the required Arial. Both
issues survive into publication unless caught, and neither is obvious without
measurement. The skill now surfaces them at workflow step 2 with measured
reasoning, provides a ready override block, and gives the tools (`dump_style.py
colormap`) to verify claims rather than trust documentation.

The CIE L* upgrade replaces a 1990s TV-era luma approximation with the perceptual
standard that actually predicts whether two colours are distinguishable. Rec. 601
told us gnuplot was fine; CIE L* shows it collapses 39 value pairs and is
non-monotonic. That is why the correction matters.

### Verified
Against `cnsplots` 0.7.0 on Python 3.12.14 / matplotlib 3.10.9: all six scripts
including `recommended_overrides.py` and the new `dump_style.py colormap` mode, all
four templates, both vendored upstream scripts, and a full override block that sets
`palette_seq='viridis'` and moves Arial first. See `skill.json` → `verification`.

## [1.6.0] — 2026-09-01
