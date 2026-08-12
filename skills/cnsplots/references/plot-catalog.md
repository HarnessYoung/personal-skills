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

- `figure(width, height, color_cycle=..., color_map=...)`: pixel-sized canvas.
- `multipanel(max_width=...)` + `panel(label, width, height)`: labeled panels.
- `add_panel_label`, `take_legend_out`, `apply_unicode_font`.
- `savefig(path)`: saves and creates parent directories.
- `settings.context(...)`: scoped style overrides.
- `palettes`, `get_hexcolors_from_apalette`, and constants `cns.RED`,
  `cns.BLUE`, `cns.GREEN`, `cns.ORANGE`, `cns.PURPLE`, `cns.GRAY`, etc.
- `setup_matplotlib`, `setup_ax`, `setup_scanpy`, `setup_ggplot`: apply cnsplots
  styling to figures built with other libraries.

Palettes: qualitative `Ecotyper1`-`Ecotyper6`, `Cell`, `Nature`, `Science`,
`Set1`-`Set3`, `Tableau`, `Bold`; sequential `parula`, `gnuplot`; diverging
`BlueRed`, `BuRd_custom`, `OrBu_custom`.

### Multi-panel skeleton

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
