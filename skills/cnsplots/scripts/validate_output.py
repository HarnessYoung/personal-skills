#!/usr/bin/env python3
"""Validate that a saved cnsplots figure exists and looks usable.

Usage:
    python3 validate_output.py outputs/figure.svg [more paths...]
"""

from __future__ import annotations

import sys
from pathlib import Path

MIN_BYTES = 512


def check(path: Path) -> bool:
    if not path.exists():
        print(f"FAIL {path}: does not exist")
        return False

    size = path.stat().st_size
    if size < MIN_BYTES:
        print(f"FAIL {path}: only {size} bytes, likely an empty canvas")
        return False

    suffix = path.suffix.lower()
    head = path.read_bytes()[:1024]

    if suffix == ".svg":
        if b"<svg" not in head:
            print(f"FAIL {path}: missing <svg> root element")
            return False
        text = path.read_text(errors="ignore")
        glyphs = text.count("<text")
        print(f"OK   {path}: {size} bytes, {glyphs} text elements")
        if glyphs == 0:
            print(f"WARN {path}: no <text> elements; labels may be outlined paths")
        return True

    if suffix == ".pdf" and not head.startswith(b"%PDF"):
        print(f"FAIL {path}: missing %PDF header")
        return False

    if suffix == ".png" and not head.startswith(b"\x89PNG"):
        print(f"FAIL {path}: missing PNG signature")
        return False

    print(f"OK   {path}: {size} bytes")
    return True


def main(argv: list[str]) -> int:
    if not argv:
        return print("usage: validate_output.py <figure> [...]") or 2
    return 0 if all(check(Path(a)) for a in argv) else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
