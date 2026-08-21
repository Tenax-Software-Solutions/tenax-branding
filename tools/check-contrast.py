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
    ("--tenax-on-action", "--tenax-action", AA_NORMAL, "label on a solid action-orange fill"),
    ("--tenax-action", "--tenax-bg", AA_NONTEXT, "action-orange fill against the page"),
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
    ("--tenax-on-action", "--tenax-accent",
     "a white label on Signal Orange — why --tenax-action is darkened, and what design "
     "variant V2 shipped"),
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


def mix(a: str, b: str, t: float) -> str:
    a, b = a.lstrip("#"), b.lstrip("#")
    return "#%02x%02x%02x" % tuple(
        round(int(a[i : i + 2], 16) * (1 - t) + int(b[i : i + 2], 16) * t) for i in (0, 2, 4)
    )


def check_gradient(tokens: dict[str, str]) -> int:
    """The primary action fill is a gradient, so a single token pair cannot
    describe its label contrast. Sample along it instead.

    A centred label sits over the middle of the pill, so the midpoint is what
    must pass. The orange end is allowed to fall to large-text-only -- that is a
    documented consequence of the design, not a regression.
    """
    need = ("--tenax-accent-gradient-start", "--tenax-accent-gradient-end",
            "--tenax-on-accent-gradient")
    if not all(k in tokens for k in need):
        print("\nGRADIENT\n  gradient tokens not found — skipped")
        return 0
    start, end, label = (tokens[k] for k in need)

    print(f"\nPRIMARY ACTION GRADIENT  {start} -> {end}, label {label}")
    stops = [i / 10 for i in range(11)]
    ratios = {t: ratio(label, mix(start, end, t)) for t in stops}
    passing = [t for t, r in ratios.items() if r >= AA_NORMAL]
    edge = max(passing) if passing else 0.0

    mid = ratios[0.5]
    ok = mid >= AA_NORMAL
    print(f"  midpoint (where a centred label sits): {mid:.2f}:1  {'ok' if ok else 'FAIL'}")
    worst = min(ratios.values())
    if worst >= AA_NORMAL:
        print(f"  worst point {worst:.2f}:1 — the whole ramp clears AA, labels can be any length")
        return 0 if ok else 1
    print(f"  clears AA up to {edge:.0%} along the ramp; worst point {worst:.2f}:1")
    if worst < AA_LARGE:
        print("  WARNING: part of the ramp is below 3:1 even for large text")
        return 1
    print("  keep primary button labels short so they stay inside the passing region")
    return 0 if ok else 1


def parse_themes(css: str) -> dict[str, dict[str, str]]:
    """Return {theme: {token: hex}}. Light inherits everything dark declares."""
    blocks = re.findall(r"(:root|\[data-theme=\"light\"\])\s*\{(.*?)\n\}", css, re.S)
    themes: dict[str, dict[str, str]] = {"dark": {}, "light": {}}
    for selector, body in blocks:
        target = "dark" if selector == ":root" else "light"
        pattern = r"(--tenax-[\w-]+)\s*:\s*(#[0-9a-fA-F]{3,8}|var\(\s*--tenax-[\w-]+\s*\))\s*;"
        for name, value in re.findall(pattern, body):
            themes[target][name] = value.strip()
    themes["light"] = {**themes["dark"], **themes["light"]}

    # Resolve var() indirection so callers always see a literal colour.
    for theme in themes.values():
        for name in list(theme):
            seen = set()
            while theme[name].startswith("var("):
                ref = theme[name][4:-1].strip()
                if ref in seen or ref not in theme:
                    break            # cycle, or points outside the palette
                seen.add(ref)
                theme[name] = theme[ref]
    return themes


def main() -> int:
    if not CSS.exists():
        print(f"error: {CSS} not found", file=sys.stderr)
        return 2
    css = CSS.read_text()
    themes = parse_themes(css)

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

    failures += check_gradient(themes["dark"])

    if failures:
        print(f"\n{failures} contrast contract violation(s).")
        return 1
    print(f"\nall {len(CONTRACT) * 2} contrast checks passed across both themes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
