#!/usr/bin/env python3
"""WCAG 2.x contrast ratio for hex colour pairs.

Usage: contrast.py FG BG [FG BG ...]   e.g. contrast.py "#1a1a1a" "#e6e6e6"
Thresholds: 4.5:1 body text, 3:1 large text and UI shapes (WCAG 2.2 AA),
7:1 enhanced (AAA). This computes sRGB colors, not measured panel contrast.
"""
import sys


def luminance(hex_colour):
    h = hex_colour.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    if len(h) != 6:
        raise ValueError(f"not a hex colour: {hex_colour}")
    channels = []
    for i in (0, 2, 4):
        c = int(h[i:i + 2], 16) / 255
        channels.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    r, g, b = channels
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(fg, bg):
    a, b = sorted((luminance(fg), luminance(bg)), reverse=True)
    return (a + 0.05) / (b + 0.05)


def main(args):
    if not args or len(args) % 2:
        print(__doc__)
        return 2
    for fg, bg in zip(args[::2], args[1::2]):
        try:
            r = ratio(fg, bg)
        except ValueError as error:
            print(f"error: {error}", file=sys.stderr)
            return 2
        verdict = ("text OK (>=7, AAA)" if r >= 7 else
                   "text OK (>=4.5 AA)" if r >= 4.5 else
                   "large text / UI shapes only (>=3)" if r >= 3 else
                   "FAIL (<3)")
        print(f"{fg} on {bg}: {r:.2f}:1  {verdict}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
