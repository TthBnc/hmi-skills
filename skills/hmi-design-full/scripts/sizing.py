#!/usr/bin/env python3
"""Panel sizing helper: mm <-> px <-> arcminutes.

Usage:
  sizing.py --ppi 150 --distance-mm 700            print recommended minimums
  sizing.py --ppi 150 --distance-mm 700 --mm 20    convert one size
  sizing.py --ppi 150 --distance-mm 700 --px 48
  ppi from a panel: --diag-in 15.6 --res 1920x1080 (instead of --ppi)

Heuristic starting points (verify against the task and actual panel):
  targets 15 mm bare hand, 20 mm gloved; text 16-22 arcmin.
  PPI refers to physical device pixels. --device-pixel-ratio converts to CSS
  pixels; OS/webview zoom may require additional calibration.
"""
import argparse
import math


def ppi_from_panel(diag_in, res):
    w, h = (int(v) for v in res.lower().split("x"))
    return math.hypot(w, h) / diag_in


def mm_to_px(mm, ppi):
    return mm * ppi / 25.4


def arcmin_to_mm(arcmin, distance_mm):
    return 2 * distance_mm * math.tan(math.radians(arcmin / 60) / 2)


def mm_to_arcmin(mm, distance_mm):
    return math.degrees(2 * math.atan(mm / (2 * distance_mm))) * 60


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--ppi", type=float)
    p.add_argument("--diag-in", type=float)
    p.add_argument("--res")
    p.add_argument("--distance-mm", type=float, default=700)
    p.add_argument("--mm", type=float)
    p.add_argument("--px", type=float, help="physical device pixels")
    p.add_argument("--device-pixel-ratio", type=float, default=1.0)
    a = p.parse_args()

    for key in ("ppi", "diag_in", "distance_mm", "mm", "px", "device_pixel_ratio"):
        value = getattr(a, key)
        if value is not None and (not math.isfinite(value) or value <= 0):
            p.error(f"--{key.replace('_', '-')} must be finite and positive")
    if a.ppi is not None and (a.diag_in is not None or a.res is not None):
        p.error("use --ppi OR --diag-in with --res")
    if a.mm is not None and a.px is not None:
        p.error("use --mm OR --px")
    if a.ppi is None and (a.diag_in is None or a.res is None):
        p.error("give --ppi or --diag-in with --res")
    try:
        if a.res is not None:
            w, h = (int(v) for v in a.res.lower().split("x"))
            if w <= 0 or h <= 0:
                raise ValueError("resolution must be positive")
        ppi = a.ppi if a.ppi is not None else ppi_from_panel(a.diag_in, a.res)
    except ValueError:
        p.error("--res must be positive WIDTHxHEIGHT, for example 1920x1080")
    d = a.distance_mm
    print(f"panel {ppi:.0f} ppi, viewing distance {d:.0f} mm")
    print("Pixel outputs are device pixels; divide by device-pixel-ratio for CSS pixels.")
    print(f"device-pixel-ratio {a.device_pixel_ratio:g}; verify OS/webview zoom on the panel")

    if a.mm is not None or a.px is not None:
        mm = a.mm if a.mm is not None else a.px * 25.4 / ppi
        print(f"{mm:.1f} mm = {mm_to_px(mm, ppi):.0f} device px = "
              f"{mm_to_px(mm, ppi) / a.device_pixel_ratio:.0f} CSS px = "
              f"{mm_to_arcmin(mm, d):.1f} arcmin")
        return

    print("\nTouch targets (physical size, independent of distance):")
    for label, mm in [("bare hand starting point", 15), ("gloved starting point", 20),
                      ("gloved primary / start-stop", 25), ("separation", 4)]:
        print(f"  {label:28} {mm:>4} mm = {mm_to_px(mm, ppi):4.0f} px")

    print("\nText (cap/character height at this distance):")
    for label, arc in [("small-text starting point", 16), ("preferred", 21), ("critical values", 30)]:
        mm = arcmin_to_mm(arc, d)
        px = mm_to_px(mm, ppi)
        # cap height is roughly 0.7 of the CSS font size for common sans fonts
        print(f"  {label:28} {arc:>4} arcmin = {mm:.1f} mm = {px:.0f} px cap height"
              f" (~{px / 0.7:.0f} px font-size)")


if __name__ == "__main__":
    main()
