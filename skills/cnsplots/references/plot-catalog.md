# cnsplots plot catalog

Select the narrowest fitting function, then verify its installed signature with
`scripts/inspect_api.py <name>` before writing code.

## Distributions and group comparison

| Function | Use for |
| --- | --- |
| `boxplot` | quartiles/medians across categories; optional pairwise tests |
| `violinplot` | full distribution shape across categories |
| `stripplot` | individual observations, often overlaid on box/violin |
| `barplot` | group estimates as bars (with error bars) |
| `lollipopplot` | values with stems and markers, dense categories |
| `dumbbellplot` | two endpoints per category connected by a line |
| `histplot` | binned univariate or bivariate distributions |
| `kdeplot` | smoothed density estimates |
| `distplot` | compact combined distribution view |
| `ridgeplot` | stacked densities across many groups |
| `qqplot` | observed vs theoretical quantiles |

## Relationships and change

- `scatterplot`: relationship between numeric variables.
- `regplot`: fitted regression with confidence context.
- `lineplot`: trends or repeated measures over an ordered axis.
- `slopeplot`: paired change between two conditions or time points.

## Matrices and classification

- `heatmapplot`: annotated / hierarchically clustered matrices.
- `dotplot`: matrix values encoded by dot size + color (enrichment style).
- `confusionplot`: predicted vs observed classes.

`heatmapplot` and `dotplot` return backend-native plotter objects, not `Axes`.
Style them through their internal axes (`ax`, `ax_heatmap`, `hm_ax`, `cbar_ax`,
`dot_legend`, `ax_row_dendrogram`, `ax_col_dendrogram`, `ax_*_annotation`); note
`hm_ax` and `ax_heatmap` are different objects. See
[dense-figures.md](dense-figures.md).

## Proportions, sets, flows

- `stackplot`: categorical composition across groups (supports Fisher tests).
- `pieplot`, `donutplot`: parts of a whole, few categories only.
- `vennplot`: overlap among 2-3 sets; returns a matplotlib-venn object.
- `upsetplot`: scalable set intersections; returns panel axes.
- `sankeyplot`: flow between source and target categories.

## Survival and model summaries

- `survivalplot`: Kaplan-Meier curves, log-rank tests, pairwise hazard ratios.
- `cumulativeincidenceplot`: competing-risk cumulative incidence.
- `forestplot`: effect estimates with confidence intervals.
- `CoxModel`, `LogisticModel`: fitted models feeding the plots above.

Confirm event coding (1 = event vs censored), time units, reference group, and
requested contrasts before plotting.

## Genomics and evaluation

- `volcanoplot`: effect size vs transformed adjusted significance.
- `gseaplot` / `prerank`: gene-set enrichment results.
- `rocplot`: ROC curves with AUC.
- `phyloplot`: phylogenetic visualization from `AnnData`.

Never infer log transforms or significance cutoffs; read the installed
signature for the exact expected columns.

## Composition, style, export

Figure and layout:

- `figure(width, height, color_cycle=..., color_map=...)`: pixel-sized canvas.
  Applies the full style and returns `None`.
- `multipanel(max_width=..., title=..., loc=..., title_fontweight=...)` with
  `.panel(...)`, `.newline()`, `.get_axes(label)`, `.fig`, `.axes`.
- `add_panel_label(name, pad_left, pad_top)`: labels the **current** axes; there
  is no `ax` parameter, so call `plt.sca(ax)` first.
- `savefig(path)` (alias `save`): saves and creates parent directories.

Style:

- `setup_matplotlib`, `setup_ax`, `setup_scanpy`, `setup_ggplot`: apply cnsplots
  styling to figures built with other libraries. All return `None`.
- `settings.context(...)`: scoped style overrides. `settings.reset()`: restore
  defaults.
- `take_legend_out(title=None, *, ax=None)`: `ax` is keyword-only.
- `apply_unicode_font()`: CJK and symbol coverage.

Color:

- `palettes(name_or_list)`: returns RGB float tuples for **qualitative** names
  only; sequential names such as `gnuplot` raise `RuntimeError`.
- `get_hexcolors_from_apalette(indices)`: specific colors from the active palette.
- Constants: `RED`, `BLUE`, `GREEN`, `ORANGE`, `PURPLE`, `YELLOW`, `PINK`, `GRAY`,
  `BROWN`, `VIOLET`, `CHOCOLATE`. The first seven are `Ecotyper1` members;
  `VIOLET` and `CHOCOLATE` sit outside it and read as non-palette colors.

Choosing and coordinating colors across panels:
[color-strategy.md](color-strategy.md).

Models and data:

- `CoxModel`, `LogisticModel`: fitted models feeding `forestplot` and survival
  plots.
- `prerank`: GSEA prerank input for `gseaplot`.
- `datasets.load_dataset(name)` for built-in demo frames;
  `datasets.get_showcase_data`; `datasets.gallery` is a submodule.
- `placeholderplot(description, *, ax=None)`: draw a captioned placeholder in a
  panel whose real content does not exist yet.
- `utils`, `validation`, `methods`: helper namespaces.

Names accepted by `palettes()`, probed against 0.7.0. Qualitative:
`Ecotyper1`-`Ecotyper6`, `Cell`, `Nature`, `Science`, `NEJM`, `Tableau`, `Bold`,
`ECharts`, `Set1`-`Set3`, `Pastel1`, `Pastel2`, `Paired`, `Dark2`, `Accent`.
Also accepted, and usable as a `color_cycle`: `BlueRed`, `BuRd_custom`,
`OrBu_custom`, `WhYlOrRd_custom`, `YlGnBu_custom`, `parula`. Plain matplotlib
colormap names are **rejected**: `gnuplot`, `viridis`, and `Blues` all raise
`RuntimeError`, so pass those through `color_map=` or `cmap=` instead. Re-probe
with `python3 scripts/dump_style.py palettes`.

Full style contract: [rcparams.md](rcparams.md) and
[settings-catalog.md](settings-catalog.md).

### Layout skeletons

Pick the engine deliberately; see
[composition-patterns.md](composition-patterns.md) for why these are not
interchangeable, and start from `templates/`.

```python
import matplotlib

matplotlib.use("Agg")

import cnsplots as cns

mp = cns.multipanel(max_width=540)

ax_a = mp.panel("A", width=150, height=150)
cns.boxplot(data=grouped, x="group", y="value", ax=ax_a)

ax_b = mp.panel("B", width=150, height=150)
cns.scatterplot(data=continuous, x="x", y="y", ax=ax_b)

cns.savefig("outputs/multipanel.svg")
```

For a uniform repeated grid use `cns.figure()` plus `plt.gcf().subplots(...)`
instead; `multipanel` does not align panel edges.
