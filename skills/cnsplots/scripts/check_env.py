#!/usr/bin/env python3
"""Report whether this environment can build cnsplots figures."""

from __future__ import annotations

import importlib
import importlib.util
import shutil
import sys


def main() -> int:
    print(f"python      : {sys.version.split()[0]}")
    print(f"executable  : {sys.executable}")

    if importlib.util.find_spec("cnsplots") is None:
        print("cnsplots    : MISSING")
        print()
        print("Install it (ask the user first):")
        print("  python3 -m pip install cnsplots")
        print("  # or: uv pip install cnsplots")
        return 1

    cns = importlib.import_module("cnsplots")
    print(f"cnsplots    : {cns.__version__}")

    for name in ("matplotlib", "numpy", "pandas", "seaborn", "lifelines", "gseapy", "scanpy"):
        spec = importlib.util.find_spec(name)
        print(f"{name:<12}: {'ok' if spec else 'missing'}")

    matplotlib = importlib.import_module("matplotlib")
    print(f"backend     : {matplotlib.get_backend()} (use Agg when headless)")

    mutool = shutil.which("mutool")
    print(f"mutool      : {mutool or 'missing (SVG falls back to plain matplotlib)'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
