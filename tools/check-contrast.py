#!/usr/bin/env python3
"""Assert the Tenax token palette still meets its documented contrast contract.

brand-guide.md makes specific accessibility claims about these colours. This
turns those claims into a test, so editing a token to something that "looks
about right" fails loudly instead of quietly shipping unreadable UI.

Reads the real values out of assets/tokens/tenax.css -- there is no second copy
of the palette to drift out of sync.

Also prints the DOCUMENTED HAZARDS: pairs that deliberately fail, and are the
reason certain rules exist in the guide. They are informational, not failures.

Usage:
    python3 tools/check-contrast.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSS = ROOT / "assets" / "tokens" / "tenax.css"

AA_NORMAL = 4.5   # body text
AA_LARGE = 3.0    # >=24px, or >=18.66px bold
AA_NONTEXT = 3.0  # focus rings, icon strokes, meaningful borders

# (foreground token, background token, minimum ratio, what it protects)
CONTRACT = [
    ("--tenax-text", "--tenax-bg", AA_NORMAL, "body copy on the page"),
    ("--tenax-text", "--tenax-surface", AA_NORMAL, "body copy on a card"),
    ("--tenax-text-muted", "--tenax-bg", AA_NORMAL, "helper text on the page"),
    ("--tenax-text-muted", "--tenax-surface", AA_NORMAL, "helper text on a card"),
    ("--tenax-text-subtle", "--tenax-bg", AA_LARGE, "large/decorative text only"),
    ("--tenax-accent-text", "--tenax-bg", AA_NORMAL, "orange word highlights on the page"),
    ("--tenax-accent-text", "--tenax-surface", AA_NORMAL, "orange word highlights on a card"),
    ("--tenax-on-accent", "--tenax-accent", AA_NORMAL, "label on an orange fill"),
    ("--tenax-on-blue", "--tenax-blue-surface", AA_NORMAL, "text on a Sentinel Blue field"),
    ("--tenax-link", "--tenax-bg", AA_NORMAL, "links"),
    ("--tenax-focus", "--tenax-bg", AA_NONTEXT, "focus ring against the page"),
    ("--tenax-focus", "--tenax-surface", AA_NONTEXT, "focus ring against a card"),
]

for _status in ("success", "info", "warning", "error"):
    CONTRACT += [
        (f"--tenax-{_status}", "--tenax-bg", AA_NORMAL, f"{_status} text/icon on the page"),
        (f"--tenax-{_status}", "--tenax-surface", AA_NORMAL, f"{_status} text/icon on a card"),
        ("--tenax-on-status", f"--tenax-{_status}", AA_NORMAL, f"label on a {_status} badge"),
    ]

# Pairs that fail on purpose. Each one is why a rule exists in brand-guide.md.
HAZARDS = [
    ("--tenax-sentinel-blue", "--tenax-bg",
     "Sentinel Blue as a foreground on Command Black — why blue is a surface, never text"),
    ("--tenax-signal-orange", "--tenax-secure-white",
     "Signal Orange as text on Secure White — why light mode needs --tenax-accent-text"),
]


def luminance(hex_colour: str) -> float:
    h = hex_colour.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    channels = []
    for i in (0, 2, 4):
        c = int(h[i : i + 2], 16) / 255
        channels.append(c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4)
    r, g, b = channels
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(fg: str, bg: str) -> float:
    a, b = luminance(fg), luminance(bg)
    hi, lo = max(a, b), min(a, b)
    return (hi + 0.05) / (lo + 0.05)


def parse_themes(css: str) -> dict[str, dict[str, str]]:
    """Return {theme: {token: hex}}. Light inherits everything dark declares."""
    blocks = re.findall(r"(:root|\[data-theme=\"light\"\])\s*\{(.*?)\n\}", css, re.S)
    themes: dict[str, dict[str, str]] = {"dark": {}, "light": {}}
    for selector, body in blocks:
        target = "dark" if selector == ":root" else "light"
        for name, value in re.findall(r"(--tenax-[\w-]+)\s*:\s*(#[0-9a-fA-F]{3,8})\s*;", body):
            themes[target][name] = value
    themes["light"] = {**themes["dark"], **themes["light"]}
    return themes


def main() -> int:
    if not CSS.exists():
        print(f"error: {CSS} not found", file=sys.stderr)
        return 2
    themes = parse_themes(CSS.read_text())

    failures = 0
    for theme in ("dark", "light"):
        tokens = themes[theme]
        print(f"\n{theme.upper()}")
        print(f"  {'ratio':>7}  {'min':>4}  pair")
        for fg, bg, minimum, note in CONTRACT:
            if fg not in tokens or bg not in tokens:
                print(f"  {'?':>7}  {minimum:>4}  MISSING TOKEN {fg} or {bg}")
                failures += 1
                continue
            r = ratio(tokens[fg], tokens[bg])
            ok = r >= minimum
            failures += not ok
            mark = "ok " if ok else "FAIL"
            print(f"  {r:>7.2f}  {minimum:>4}  {mark} {fg} on {bg}  — {note}")

    print("\nDOCUMENTED HAZARDS (expected to fail; each one justifies a rule)")
    dark = themes["dark"]
    for fg, bg, note in HAZARDS:
        print(f"  {ratio(dark[fg], dark[bg]):>7.2f}        {note}")

    if failures:
        print(f"\n{failures} contrast contract violation(s).")
        return 1
    print(f"\nall {len(CONTRACT) * 2} contrast checks passed across both themes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
