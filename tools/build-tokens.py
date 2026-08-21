#!/usr/bin/env python3
"""Generate assets/tokens/tenax.tokens.json from tenax.css.

The CSS is the single source of truth for token values; this derives the
machine-readable mirror so the two cannot drift. Consume the JSON from build
tooling that isn't CSS (Tailwind configs, React Native, report generators,
theme files for third-party dashboards).

Usage:
    python3 tools/build-tokens.py            # write the JSON
    python3 tools/build-tokens.py --check    # fail if the committed JSON is stale
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSS = ROOT / "assets" / "tokens" / "tenax.css"
JSON_OUT = ROOT / "assets" / "tokens" / "tenax.tokens.json"

# Token name prefix -> section in the JSON output.
SECTIONS = [
    ("font-", "typography"),
    ("text-", "typography"),
    ("leading-", "typography"),
    ("tracking-", "typography"),
    ("weight-", "typography"),
    ("space-", "space"),
    ("radius-", "radius"),
    ("shadow-", "elevation"),
    ("transition", "motion"),
]

BRAND = ("command-black", "sentinel-blue", "signal-orange", "secure-white")
RAMPS = ("black-", "blue-", "orange-")


def classify(name: str) -> str:
    """Bucket a token by its name."""
    if name in BRAND:
        return "brand"
    if any(name.startswith(r) for r in RAMPS) and name[-1].isdigit():
        return "ramp"
    for prefix, section in SECTIONS:
        if name.startswith(prefix):
            return section
    return "color"


def parse(css: str) -> dict:
    blocks = re.findall(r"(:root|\[data-theme=\"light\"\])\s*\{(.*?)\n\}", css, re.S)
    raw: dict[str, dict[str, str]] = {"dark": {}, "light": {}}
    for selector, body in blocks:
        target = "dark" if selector == ":root" else "light"
        for name, value in re.findall(r"--tenax-([\w-]+)\s*:\s*([^;]+);", body):
            tidy = " ".join(value.split()).replace("( ", "(").replace(" )", ")")
            raw[target][name] = tidy

    # Consumers of this file are not CSS engines -- Tailwind configs, report
    # generators, third-party dashboard themes. Resolve var() to literals so they
    # do not each have to reimplement the cascade.
    for target in ("dark", "light"):
        table = {**raw["dark"], **raw[target]}
        for name, value in list(raw[target].items()):
            for _ in range(8):
                refs = re.findall(r"var\(\s*--tenax-([\w-]+)\s*\)", value)
                if not refs:
                    break
                for ref in refs:
                    if ref not in table:
                        break
                    value = re.sub(r"var\(\s*--tenax-" + re.escape(ref) + r"\s*\)",
                                   table[ref], value)
                else:
                    continue
                break
            raw[target][name] = value

    out: dict = {
        "$comment": (
            "Generated from assets/tokens/tenax.css by tools/build-tokens.py. "
            "Do not hand-edit; change the CSS and re-run."
        ),
        "brand": {},
        "ramp": {},
        "typography": {},
        "space": {},
        "radius": {},
        "elevation": {},
        "motion": {},
        "semantic": {"dark": {}, "light": {}},
    }

    for name, value in raw["dark"].items():
        bucket = classify(name)
        if bucket == "color":
            out["semantic"]["dark"][name] = value
        elif bucket == "ramp":
            family, step = name.rsplit("-", 1)
            out["ramp"].setdefault(family, {})[step] = value
        else:
            out[bucket][name] = value

    # Light declares only what it overrides; record the full resolved set so
    # consumers don't have to implement cascade themselves.
    resolved_light = {**out["semantic"]["dark"]}
    for name, value in raw["light"].items():
        if classify(name) == "color":
            resolved_light[name] = value
        elif classify(name) == "elevation":
            out.setdefault("elevationLight", {})[name] = value
    out["semantic"]["light"] = resolved_light

    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true", help="fail if committed JSON is stale")
    args = ap.parse_args()

    if not CSS.exists():
        print(f"error: {CSS} not found", file=sys.stderr)
        return 2

    text = json.dumps(parse(CSS.read_text()), indent=2) + "\n"

    if args.check:
        if not JSON_OUT.exists():
            print(f"error: {JSON_OUT.name} has not been generated", file=sys.stderr)
            return 1
        if JSON_OUT.read_text() != text:
            print(f"error: {JSON_OUT.name} is stale — re-run tools/build-tokens.py", file=sys.stderr)
            return 1
        print(f"{JSON_OUT.name} is up to date with tenax.css")
        return 0

    JSON_OUT.write_text(text)
    data = json.loads(text)
    print(
        f"wrote {JSON_OUT.relative_to(ROOT)}: "
        f"{len(data['brand'])} brand, "
        f"{sum(len(v) for v in data['ramp'].values())} ramp, "
        f"{len(data['semantic']['dark'])} semantic colours per theme"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
