# Color strategy

How to assign color across a multi-panel figure, and why the showcase's approach
is the wrong model to copy.

## What the showcase actually does

Auditing every color decision in the vendored source
(`templates/upstream-showcase/`), Figure 1 uses **eight different palettes across
18 panels**:

| Panel | `color_cycle` | Kind |
| --- | --- | --- |
| A, E | `[cns.VIOLET]` | single named color |
| B | `[cns.CHOCOLATE]` | single named color |
| C | `"BlueRed"` | 6-color palette |
| D | `get_hexcolors_from_apalette([2, 4], "Bold")` | 2 colors picked by index |
| F, H, K | `"Ecotyper3"` | 8-color palette |
| G | `"Tableau"` | 10-color palette |
| M | `"ECharts"` | 16-color palette |
| N | `"Ecotyper4"` | 9-color palette |
| Q | `"Set1"` | 9-color palette |
| I, J, L, O, P, R | none | inherits `Ecotyper1` |
| R | `cmap="BuRd_custom"` | diverging colormap |

Figure 2 adds `"NEJM"` and `cmap="Blues"`.

**This is a palette catalog, not a figure design.** It exists to show what the
package offers, and it should not be copied as a color scheme.

Four Figure 1 panels plot iris `species`. Measured, the color assigned to
`setosa` in each:

| Panel | Palette | `setosa` renders as |
| --- | --- | --- |
| B violinplot | `[cns.CHOCOLATE]` | `#662506` (all species identical) |
| K kdeplot | `Ecotyper3` | `#d13570` |
| O ridgeplot | `Ecotyper1` (default) | `#d6372e` |
| Q scatterplot | `Set1` | `#e41a1c` |

One category, four appearances, in one figure. In a real figure that is a defect:
a reader reasonably assumes consistent color means the same thing, and
inconsistent color means a different thing.

## Rule: one palette per figure, one color per meaning

Pick one qualitative palette for the whole figure and let it flow from
`settings.palette_qual`. Deviate per panel only for a reason you can state.

```python
cns.settings.palette_qual = "Ecotyper1"     # or set it once via context
```

Legitimate reasons to override on one panel:

- **The panel encodes a different variable.** A treatment-arm panel and a
  cell-type panel are different domains; separate palettes prevent a false
  visual link. This is the strongest reason.
- **The panel is single-series.** One color, no palette:
  `color_cycle=[cns.VIOLET]`. Showcase panels A, B, E do this, and it is good
  practice: a lone box or bar series does not need a cycle.
- **Category count exceeds the palette.** `Ecotyper1` has 9 colors; beyond that
  reach for `ECharts` (16) rather than letting colors repeat.
- **Semantic convention.** Two-level contrasts read better on a diverging pair
  (`BlueRed`), and journals often expect specific conventions.

## Keeping one variable on one color

Two mechanisms, both verified.

**`hue_order` fixes the mapping.** Colors are assigned by position in the hue
order, so the same palette plus the same explicit order gives identical colors
across panels. Measured across a scatterplot and a kdeplot panel: both produced
`['#d6372e', '#5189bb', '#70b460']` for the same three species.

```python
SPECIES = ["setosa", "versicolor", "virginica"]     # define once

cns.scatterplot(data=df, x="a", y="b", hue="species", hue_order=SPECIES, ax=ax1)
cns.kdeplot(data=df, x="c", hue="species", hue_order=SPECIES, ax=ax2)
```

Without `hue_order`, the order comes from the data, so a panel plotting a subset
that lacks one category shifts every subsequent color. **Always pass `hue_order`
in a multi-panel figure**, even when it looks redundant.

**An explicit color list pins specific colors.** For a subset panel, or when a
category must keep its color regardless of who else is present, build the cycle
to match the order you pass:

```python
PALETTE = {"setosa": cns.BLUE, "versicolor": cns.GREEN, "virginica": cns.RED}

present = [s for s in SPECIES if s in subset["species"].unique()]
ax = mp.panel("B", 90, 90, color_cycle=[PALETTE[s] for s in present])
cns.scatterplot(data=subset, x="a", y="b", hue="species",
                hue_order=present, ax=ax)
```

Verified: a two-category subset with `color_cycle=[cns.BLUE, cns.RED]` and a
matching `hue_order` rendered `setosa` as `#5189bb`, exactly `cns.BLUE`.

## Picking related colors from one palette

`get_hexcolors_from_apalette(indices, palette)` pulls specific entries, which is
how you give two panels colors that are distinguishable but visibly from the same
family. Showcase panel D uses `[2, 4]` from `Bold`, giving `#3969ac` and
`#e73f74`.

```python
pair = cns.get_hexcolors_from_apalette([2, 4], "Bold")   # ['#3969ac', '#e73f74']
```

Note it returns **hex strings**, while `cns.palettes(name)` returns **RGB float
tuples**. Do not compare their outputs directly.

## Qualitative, sequential, diverging

Match the encoding to the data, and do not mix the roles:

- **Qualitative** (`Ecotyper1`-`6`, `Cell`, `Nature`, `Science`, `NEJM`,
  `Tableau`, `Bold`, `ECharts`, `Set1`-`3`, ...) for unordered categories, via
  `color_cycle=`.
- **Sequential** for magnitude, via `color_map=` / `cmap=`. `settings.palette_seq`
  defaults to `gnuplot`.
- **Diverging** (`BuRd_custom`, `OrBu_custom`, `BlueRed`) for values around a
  meaningful midpoint: log fold change, z-score, difference from control. The
  showcase heatmap uses `BuRd_custom` on z-scores, which is correct; a sequential
  map there would hide the sign.

`cns.palettes()` accepts qualitative names **and** several sequential/diverging
ones, but rejects plain matplotlib colormap names (`gnuplot`, `viridis`, `Blues`
raise `RuntimeError`). Those go through `color_map=` or `cmap=`. Probe the
accepted set with `python3 $SKILL_DIR/scripts/dump_style.py palettes`.

For a diverging colormap to mean anything, the scale must be centered. Set
`vmin`/`vmax` symmetrically, or the midpoint color lands at an arbitrary value.

## Named constants

`cns.RED` `#D6372E`, `cns.BLUE` `#5189BB`, `cns.GREEN` `#70B460`,
`cns.ORANGE` `#F08F35`, `cns.PURPLE` `#985EA8`, `cns.YELLOW` `#FADD4B`,
`cns.PINK` `#E787E5`, `cns.GRAY` `#A3A3A3`, `cns.BROWN` `#9C5732`,
`cns.VIOLET` `#442288`, `cns.CHOCOLATE` `#662506`.

The first seven are `Ecotyper1` entries, so mixing them with the default palette
stays in family. `VIOLET` and `CHOCOLATE` are darker and sit outside it, which is
why the showcase uses them for single-series panels that should not read as
palette members.

Use `cns.GRAY` for reference lines, annotations, and non-data furniture so the
palette stays reserved for data. The showcase draws its mean lines with
`color="gray"`.

## Verify legibility

Color choice is not done until checked:

- **Color vision.** Roughly 8% of men have red-green deficiency. `Set1` red vs
  green and `Ecotyper1` `#d6372e` vs `#70b460` are the risky pairs. Prefer
  blue-orange for two-level contrasts, or add a non-color channel (marker shape,
  line dash, direct labels).
- **Greyscale.** Convert the PNG to L and confirm the series remain
  distinguishable, since figures get printed and photocopied.
- **Never encode by color alone** where the distinction carries the claim. Add
  shape, dash, or annotation.

```python
from PIL import Image

Image.open("figure.png").convert("L").save("figure_grey.png")   # then look at it
```

For the palette itself, rather than a specific figure:

```bash
python3 $SKILL_DIR/scripts/dump_style.py greyscale
```

That prints each entry's Rec. 601 luma and flags pairs within 0.10, which are the
ones that collapse without color. The **default `Ecotyper1` has several**: entries
4 and 6 (`#f08f35` orange, `#a3a3a3` grey) differ by 0.005 luma, and 1 and 3
(`#5189bb` blue, `#985ea8` purple) by 0.024. If your figure needs to survive
greyscale, either pick series from luma-separated indices with
`get_hexcolors_from_apalette`, or carry the distinction on a second channel. For
three series out of `Ecotyper1`, indices `[0, 4, 8]` are the most separated
(minimum luma gap 0.219, versus 0.005 for the worst pair):

```python
color_cycle=cns.get_hexcolors_from_apalette([0, 4, 8], "Ecotyper1")
```

That trio is red, orange, and cream, which is greyscale-safe but weak for
red-green deficiency. The two goals genuinely conflict; when both matter, stop
relying on color and add a marker or dash channel.

## Checklist

1. One qualitative palette per figure, set once.
2. Per-panel override only for a stated reason; single-series panels get one color.
3. `hue_order` on every panel that shares a categorical variable.
4. Sequential for magnitude, diverging with a centered scale for signed values.
5. `cns.GRAY` for furniture, not palette colors.
6. Check greyscale and a red-green-deficient reading before delivering.
