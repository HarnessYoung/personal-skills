#!/usr/bin/env python3
"""Dump the style contract cnsplots applies, read from the installed package.

Nothing here is hardcoded from documentation. Every value is measured from the
live `cnsplots.settings` object and from a real before/after diff of
`matplotlib.rcParams`, so the output is always true for the *installed*
version.

Sections:
  rcparams  diff of matplotlib.rcParams caused by cns.setup_matplotlib()
  settings  every public cns.settings field and its current value
  palettes  qualitative palette names that cns.palettes() accepts
  colors    module-level color constants (cns.RED, ...)

Usage:
  python3 dump_style.py                 # all sections, human readable
  python3 dump_style.py rcparams        # one section
  python3 dump_style.py --markdown      # markdown tables, for reference docs
"""

from __future__ import annotations

import argparse
import sys
from typing import Any

SECTIONS = ("rcparams", "settings", "palettes", "colors", "greyscale")

# Candidate palette names probed against the installed package. Names that the
# installed cns.palettes() rejects are reported as unavailable rather than
# assumed present.
PALETTE_CANDIDATES = (
    # Qualitative
    "Ecotyper1", "Ecotyper2", "Ecotyper3", "Ecotyper4", "Ecotyper5", "Ecotyper6",
    "Cell", "Nature", "Science", "NEJM", "Tableau", "Bold", "ECharts",
    "Set1", "Set2", "Set3", "Pastel1", "Pastel2", "Paired", "Dark2", "Accent",
    # Sequential / diverging that palettes() also accepts
    "BlueRed", "BuRd_custom", "OrBu_custom", "WhYlOrRd_custom", "YlGnBu_custom",
    "parula",
    # Probed to confirm they are rejected: plain matplotlib colormap names
    "gnuplot", "viridis", "Blues",
)

COLOR_CONSTANTS = (
    "RED", "BLUE", "GREEN", "ORANGE", "PURPLE", "YELLOW",
    "PINK", "GRAY", "BROWN", "VIOLET", "CHOCOLATE",
)


def measure_rcparams() -> list[tuple[str, Any, Any]]:
    """Diff matplotlib.rcParams before and after cns.setup_matplotlib()."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib as mpl

    mpl.rcParams.update(mpl.rcParamsDefault)
    matplotlib.use("Agg")
    before = dict(mpl.rcParams)

    import cnsplots as cns

    cns.setup_matplotlib()
    after = dict(mpl.rcParams)

    rows = []
    for key in sorted(after):
        old, new = before.get(key), after[key]
        if str(old) == str(new) or key == "backend":
            continue
        rows.append((key, old, new))
    return rows


def collect_settings() -> list[tuple[str, Any]]:
    import cnsplots as cns

    out = []
    for name in sorted(dir(cns.settings)):
        if name.startswith("_"):
            continue
        value = getattr(cns.settings, name)
        if callable(value):
            continue
        out.append((name, value))
    return out


def probe_palettes() -> tuple[list[str], list[str]]:
    import cnsplots as cns

    ok, missing = [], []
    for name in PALETTE_CANDIDATES:
        try:
            cns.palettes(name)
        except Exception:  # noqa: BLE001 - probing, any failure means unavailable
            missing.append(name)
        else:
            ok.append(name)
    return ok, missing


def collect_colors() -> list[tuple[str, str]]:
    import cnsplots as cns

    return [(n, getattr(cns, n)) for n in COLOR_CONSTANTS if hasattr(cns, n)]


def check_greyscale(palette: str, count: int | None = None) -> list[tuple]:
    """Report perceived lightness of a palette's colors and flag close pairs.

    Series that differ only in hue collapse when printed in greyscale. This
    computes Rec. 601 luma for each entry and flags pairs within 0.10, which are
    hard to tell apart without color.
    """
    import matplotlib.colors as mcolors

    import cnsplots as cns

    colors = cns.palettes(palette)
    if count:
        colors = list(colors)[:count]

    rows = []
    for index, color in enumerate(colors):
        r, g, b = mcolors.to_rgb(color)
        luma = 0.299 * r + 0.587 * g + 0.114 * b
        rows.append((index, mcolors.to_hex(color), luma))

    clashes = [
        (a[0], b[0], abs(a[2] - b[2]))
        for i, a in enumerate(rows)
        for b in rows[i + 1 :]
        if abs(a[2] - b[2]) < 0.10
    ]
    return rows, clashes


def emit_plain(sections: tuple[str, ...]) -> None:
    import cnsplots as cns

    print(f"cnsplots {cns.__version__}  python {sys.version.split()[0]}")

    if "rcparams" in sections:
        rows = measure_rcparams()
        print(f"\n== rcParams changed by setup_matplotlib() ({len(rows)}) ==")
        for key, old, new in rows:
            print(f"{key:<26} {old!r}  ->  {new!r}")

    if "settings" in sections:
        rows = collect_settings()
        print(f"\n== cns.settings ({len(rows)}) ==")
        for name, value in rows:
            print(f"{name:<32} {value!r}")

    if "palettes" in sections:
        ok, missing = probe_palettes()
        print(f"\n== palettes accepted ({len(ok)}) ==")
        print("  " + ", ".join(ok))
        if missing:
            print(f"== probed but unavailable ({len(missing)}) ==")
            print("  " + ", ".join(missing))

    if "colors" in sections:
        print("\n== color constants ==")
        for name, value in collect_colors():
            print(f"cns.{name:<10} {value}")

    if "greyscale" in sections:
        target = cns.settings.palette_qual
        rows, clashes = check_greyscale(target)
        print(f"\n== greyscale separation: {target} ==")
        for index, hex_value, luma in rows:
            bar = "#" * max(1, round(luma * 40))
            print(f"  [{index}] {hex_value}  luma={luma:.3f}  {bar}")
        if clashes:
            print("  pairs within 0.10 luma (collapse in greyscale):")
            for a, b, delta in clashes:
                print(f"    [{a}] vs [{b}]  delta={delta:.3f}")
        else:
            print("  no pairs within 0.10 luma")


def emit_markdown(sections: tuple[str, ...]) -> None:
    import cnsplots as cns

    print(f"<!-- generated by scripts/dump_style.py against cnsplots "
          f"{cns.__version__} -->")

    if "rcparams" in sections:
        print("\n### rcParams set by `setup_matplotlib()`\n")
        print("| rcParam | matplotlib default | cnsplots |")
        print("| --- | --- | --- |")
        for key, old, new in measure_rcparams():
            print(f"| `{key}` | `{old!r}` | `{new!r}` |")

    if "settings" in sections:
        print("\n### `cns.settings`\n")
        print("| Setting | Value |")
        print("| --- | --- |")
        for name, value in collect_settings():
            print(f"| `{name}` | `{value!r}` |")

    if "palettes" in sections:
        ok, _ = probe_palettes()
        print("\n### Qualitative palettes\n")
        print(", ".join(f"`{n}`" for n in ok))

    if "colors" in sections:
        print("\n### Color constants\n")
        print("| Name | Hex |")
        print("| --- | --- |")
        for name, value in collect_colors():
            print(f"| `cns.{name}` | `{value}` |")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    # No default= here: argparse validates a list default against choices as a
    # single value and rejects it. Empty means "all", resolved below.
    parser.add_argument("sections", nargs="*", choices=SECTIONS,
                        help="sections to dump (default: all)")
    parser.add_argument("--markdown", action="store_true",
                        help="emit markdown tables for reference docs")
    args = parser.parse_args()

    try:
        import cnsplots  # noqa: F401
    except ImportError:
        print("cnsplots is not importable in this interpreter; "
              "run scripts/check_env.py", file=sys.stderr)
        return 1

    sections = tuple(args.sections) or SECTIONS
    if args.markdown:
        emit_markdown(sections)
    else:
        emit_plain(sections)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
