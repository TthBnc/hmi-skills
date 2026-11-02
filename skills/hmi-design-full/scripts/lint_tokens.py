#!/usr/bin/env python3
"""List hard-coded colours and pixel sizes that bypass design tokens.

Usage: lint_tokens.py PATH [--ext .css,.scss,.tsx,.jsx,.ts,.rs,.vue,.svelte]
Skips lines that define CSS custom properties (--token: value) and files under
node_modules, dist, build and target. Output: file:line: kind value | line.
Tailwind arbitrary values (bg-[#...], w-[13px]) and raw palette classes
(text-red-500) are reported too.
"""
import argparse
import os
import re
import sys

HEX = re.compile(r"#[0-9a-fA-F]{3,8}\b")
FUNC = re.compile(r"\b(?:rgba?|hsla?)\(")
PX = re.compile(r"\b\d+(?:\.\d+)?px\b")
TW_ARBITRARY = re.compile(r"\b[\w-]+-\[[^\]]+\]")
TW_PALETTE = re.compile(r"\b(?:bg|text|border|ring|fill|stroke)-(?:red|green|yellow|amber|orange|blue|gray|grey|slate|zinc|neutral|stone|emerald|lime|sky|indigo|violet|purple|pink|rose|teal|cyan)-\d{2,3}\b")
SKIP_DIRS = {"node_modules", "dist", "build", "target", ".git", "out"}


def scan(path, exts):
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in files:
            if os.path.splitext(name)[1] in exts:
                yield os.path.join(root, name)


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path")
    parser.add_argument("--ext", default=".css,.scss,.tsx,.jsx,.ts,.rs,.vue,.svelte")
    args = parser.parse_args(argv)
    if not os.path.exists(args.path):
        parser.error("path does not exist")
    exts = set(args.ext.split(","))
    count = 0
    paths = [args.path] if os.path.isfile(args.path) else scan(args.path, exts)
    for f in paths:
        try:
            with open(f, encoding="utf-8", errors="ignore") as source:
                lines = source.read().splitlines()
        except OSError:
            continue
        for n, line in enumerate(lines, 1):
            if re.match(r"\s*--[\w-]+\s*:", line):
                continue
            for kind, rx in (("colour", HEX), ("colour-fn", FUNC), ("px", PX),
                             ("tw-arbitrary", TW_ARBITRARY), ("tw-palette", TW_PALETTE)):
                for m in rx.finditer(line):
                    count += 1
                    print(f"{f}:{n}: {kind} {m.group(0)} | {line.strip()[:100]}")
    print(f"\n{count} hard-coded values found", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
