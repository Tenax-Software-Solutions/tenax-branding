#!/usr/bin/env python3
"""Derive web-ready Tenax Solutions brand assets from the agency delivery in source/.

The 2026 logo package (Digital Mules) has two gaps this script fills:

  * ``Icon/`` shipped completely empty -- every format subfolder was present but
    contained no files, even though the identity guide devotes a page to the icon
    and calls it the favicon / app-icon asset.
  * The Primary lockup shipped with no vector at all -- only 12.8k-wide PNGs and
    one JPG. Primary is the website-header logo, so an SVG matters most there.

Both are recoverable from what *was* delivered, because every lockup is built
from the same three groups of artwork (mark, "TENAX", "SOLUTIONS") and the
Secondary lockup's SVG contains all three:

  * the icon is the mark group, re-framed onto a square viewBox;
  * Primary is those groups repositioned. The group proportions are identical
    across all three delivered lockups (measured aspect ratios agree to four
    decimal places -- see PRIMARY_LAYOUT), so repositioning reproduces the
    artwork rather than approximating it.

Derived SVGs also drop the source's ``<style>`` blocks in favour of presentation
attributes. The delivered files all key their fills off ``.cls-1``/``.cls-2``,
which collide with each other -- and with the host page -- the moment two logos
are inlined into the same document.

Colours are preserved exactly as delivered rather than normalised to the identity
guide's palette; the guide and the shipped vectors disagree slightly (see
ASSET-REQUESTS.md) and silently repainting the artwork would be the wrong fix.

Requires only PIL and the standard library.

Usage:
    python3 tools/build-assets.py            # build into assets/
    python3 tools/build-assets.py --verify   # rebuild to a temp dir, diff vs committed
"""

from __future__ import annotations

import argparse
import filecmp
import re
import shutil
import sys
import tempfile
from pathlib import Path

from PIL import Image

Image.MAX_IMAGE_PIXELS = None

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "source" / "Logo Package"
OUT = ROOT / "assets"

VARIANTS = ("color", "inverse", "black", "white")
SRC_VARIANT = {"color": "Color", "inverse": "Inverse", "black": "Black", "white": "White"}

# Command Black, from the identity guide. Used as the favicon tile so the mark
# stays legible against both light and dark browser chrome.
TILE_BG = "#0D1016"


# ---------------------------------------------------------------------------
# Minimal SVG path geometry
#
# The delivered paths use only M/L/H/V/C/S/Z (plus relative forms) -- no arcs,
# no quadratics -- so exact bounding boxes need line endpoints and cubic extrema.
# ---------------------------------------------------------------------------

_TOKENS = re.compile(r"([MmLlHhVvCcSsZz])|(-?(?:\d*\.\d+|\d+\.?)(?:[eE][-+]?\d+)?)")


def _tokenize(d: str):
    for cmd, num in _TOKENS.findall(d):
        yield cmd if cmd else float(num)


def _cubic_bounds(p0: float, p1: float, p2: float, p3: float) -> tuple[float, float]:
    """Exact min/max of one dimension of a cubic bezier."""
    lo, hi = min(p0, p3), max(p0, p3)
    a = -p0 + 3 * p1 - 3 * p2 + p3
    b = 2 * (p0 - 2 * p1 + p2)
    c = -p0 + p1
    for t in _quad_roots(3 * a, 2 * b, c):
        if 0 < t < 1:
            mt = 1 - t
            v = mt**3 * p0 + 3 * mt**2 * t * p1 + 3 * mt * t**2 * p2 + t**3 * p3
            lo, hi = min(lo, v), max(hi, v)
    return lo, hi


def _quad_roots(a: float, b: float, c: float):
    if abs(a) < 1e-12:
        if abs(b) > 1e-12:
            yield -c / b
        return
    disc = b * b - 4 * a * c
    if disc < 0:
        return
    r = disc**0.5
    yield (-b + r) / (2 * a)
    yield (-b - r) / (2 * a)


def path_bbox(d: str) -> tuple[float, float, float, float]:
    """Exact bounding box of an SVG path's ``d`` attribute."""
    xs: list[float] = []
    ys: list[float] = []
    toks = list(_tokenize(d))
    i = 0
    cx = cy = sx = sy = 0.0
    prev_c2: tuple[float, float] | None = None
    cmd = ""

    def take(n: int) -> list[float]:
        nonlocal i
        vals = toks[i : i + n]
        i += n
        return vals  # type: ignore[return-value]

    while i < len(toks):
        if isinstance(toks[i], str):
            cmd = toks[i]
            i += 1
            if cmd in "Zz":
                cx, cy = sx, sy
                prev_c2 = None
                continue
        rel = cmd.islower()
        c = cmd.upper()

        if c == "M":
            x, y = take(2)
            cx, cy = (cx + x, cy + y) if rel else (x, y)
            sx, sy = cx, cy
            xs.append(cx)
            ys.append(cy)
            prev_c2 = None
            cmd = "l" if rel else "L"  # subsequent pairs are implicit lineto
        elif c == "L":
            x, y = take(2)
            cx, cy = (cx + x, cy + y) if rel else (x, y)
            xs.append(cx)
            ys.append(cy)
            prev_c2 = None
        elif c == "H":
            (x,) = take(1)
            cx = cx + x if rel else x
            xs.append(cx)
            ys.append(cy)
            prev_c2 = None
        elif c == "V":
            (y,) = take(1)
            cy = cy + y if rel else y
            xs.append(cx)
            ys.append(cy)
            prev_c2 = None
        elif c in ("C", "S"):
            if c == "C":
                x1, y1, x2, y2, x, y = take(6)
                if rel:
                    x1, y1, x2, y2, x, y = cx + x1, cy + y1, cx + x2, cy + y2, cx + x, cy + y
            else:
                x2, y2, x, y = take(4)
                if rel:
                    x2, y2, x, y = cx + x2, cy + y2, cx + x, cy + y
                x1, y1 = (2 * cx - prev_c2[0], 2 * cy - prev_c2[1]) if prev_c2 else (cx, cy)
            bx = _cubic_bounds(cx, x1, x2, x)
            by = _cubic_bounds(cy, y1, y2, y)
            xs.extend(bx)
            ys.extend(by)
            prev_c2 = (x2, y2)
            cx, cy = x, y
        else:
            raise ValueError(f"unsupported path command {cmd!r}")

    return min(xs), min(ys), max(xs), max(ys)


# ---------------------------------------------------------------------------
# Reading the delivered SVGs
# ---------------------------------------------------------------------------

_EL = re.compile(r"<(path|circle)\b([^>]*?)/?>", re.S)
_ATTR = re.compile(r'(\w[\w-]*)="([^"]*)"')
_STYLE_FILL = re.compile(r"\.(cls-\d+)\s*\{\s*fill:\s*(#[0-9a-fA-F]+)")


class Element:
    """One drawable element plus its resolved fill and bounding box."""

    def __init__(self, tag: str, attrs: dict[str, str], fill: str):
        self.tag = tag
        self.attrs = attrs
        self.fill = fill
        if tag == "path":
            self.bbox = path_bbox(attrs["d"])
        else:
            cx, cy, r = (float(attrs[k]) for k in ("cx", "cy", "r"))
            self.bbox = (cx - r, cy - r, cx + r, cy + r)

    def render(self, fill: str | None = None) -> str:
        keep = {k: v for k, v in self.attrs.items() if k != "class"}
        body = " ".join(f'{k}="{v}"' for k, v in keep.items())
        return f'<{self.tag} {body} fill="{fill or self.fill}"/>'


def read_svg(path: Path) -> tuple[tuple[float, float, float, float], list[Element]]:
    text = path.read_text()
    vb = tuple(float(v) for v in re.search(r'viewBox="([^"]+)"', text).group(1).split())
    fills = dict(_STYLE_FILL.findall(text))
    elements = []
    for tag, raw in _EL.findall(text):
        attrs = dict(_ATTR.findall(raw))
        elements.append(Element(tag, attrs, fills.get(attrs.get("class", ""), "#000000")))
    return vb, elements  # type: ignore[return-value]


def group_secondary(elements: list[Element]) -> dict[str, list[Element]]:
    """Split the Secondary lockup into mark / TENAX / SOLUTIONS.

    The lockup is stacked, so a horizontal band test separates the groups
    cleanly: the mark ends at y~478, TENAX spans y~582-818, SOLUTIONS y~908-1000.
    """
    groups: dict[str, list[Element]] = {"mark": [], "tenax": [], "solutions": []}
    for el in elements:
        top = el.bbox[1]
        if top < 500:
            groups["mark"].append(el)
        elif top < 850:
            groups["tenax"].append(el)
        else:
            groups["solutions"].append(el)
    for name, els in groups.items():
        if not els:
            raise RuntimeError(f"Secondary lockup yielded no elements for {name!r}")
    return groups


def group_bbox(els: list[Element]) -> tuple[float, float, float, float]:
    return (
        min(e.bbox[0] for e in els),
        min(e.bbox[1] for e in els),
        max(e.bbox[2] for e in els),
        max(e.bbox[3] for e in els),
    )


def fmt(value: float, places: int = 4) -> str:
    """Trim trailing zeros so the emitted SVG stays readable."""
    text = f"{value:.{places}f}".rstrip("0").rstrip(".")
    return "0" if text in ("", "-0", "0") else text


def place(els: list[Element], target: tuple[float, float, float, float]) -> str:
    """Wrap a group in a transform that maps its bbox onto ``target``.

    Identity components are omitted -- a stray scale(1,1) in a shipped asset
    reads like a bug.
    """
    x0, y0, x1, y1 = group_bbox(els)
    tx0, ty0, tx1, ty1 = target
    sx = (tx1 - tx0) / (x1 - x0)
    sy = (ty1 - ty0) / (y1 - y0)

    parts = []
    if round(tx0, 4) or round(ty0, 4):
        parts.append(f"translate({fmt(tx0)},{fmt(ty0)})")
    if round(sx, 6) != 1 or round(sy, 6) != 1:
        parts.append(f"scale({fmt(sx, 6)},{fmt(sy, 6)})")
    if round(x0, 4) or round(y0, 4):
        parts.append(f"translate({fmt(-x0)},{fmt(-y0)})")

    inner = "".join(f"\n    {e.render()}" for e in els)
    transform = f' transform="{" ".join(parts)}"' if parts else ""
    return f"  <g{transform}>{inner}\n  </g>"


def svg_document(width: float, height: float, body: str, title: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {fmt(width)} {fmt(height)}" '
        f'role="img" aria-label="{title}">\n'
        f"  <title>{title}</title>\n"
        f"{body}\n</svg>\n"
    )


# ---------------------------------------------------------------------------
# Primary lockup geometry
#
# Measured from source/Logo Package/Primary/PNG/Tenax_Main_Color.png (12847x4168)
# by alpha bounding box, then normalised to a 1000-unit-tall viewBox. The mark
# and both wordmark groups are measured independently, so their relative
# positions and sizes come from the delivered artwork, not from guesswork.
# ---------------------------------------------------------------------------

PRIMARY_PNG_SIZE = (12847, 4168)
PRIMARY_LAYOUT = {  # pixel bounding boxes within the Primary PNG
    "mark": (1, 44, 3851, 4124),
    "tenax": (4385, 506, 12677, 2279),
    "solutions": (4556, 2946, 12846, 3646),
}


def primary_targets() -> tuple[float, float, dict[str, tuple[float, float, float, float]]]:
    pw, ph = PRIMARY_PNG_SIZE
    k = 1000.0 / ph
    targets = {
        name: (x0 * k, y0 * k, x1 * k, y1 * k) for name, (x0, y0, x1, y1) in PRIMARY_LAYOUT.items()
    }
    return pw * k, 1000.0, targets


# ---------------------------------------------------------------------------
# Builders
# ---------------------------------------------------------------------------


def build_logos(out: Path) -> dict[str, tuple[float, float, float, float]]:
    """Write every lockup x variant as a clean, class-free SVG."""
    logos = out / "logos"
    logos.mkdir(parents=True, exist_ok=True)
    mark_boxes = {}

    for variant in VARIANTS:
        sv = SRC_VARIANT[variant]
        sec_vb, sec_els = read_svg(SRC / f"Secondary/SVG/Tenax_Secondary_{sv}.svg")
        sub_vb, sub_els = read_svg(SRC / f"Submark/SVG/Tenax_Submark_{sv}.svg")
        groups = group_secondary(sec_els)

        # Secondary + Submark: same artwork, re-emitted without <style> classes.
        for name, (vb, els) in {"secondary": (sec_vb, sec_els), "submark": (sub_vb, sub_els)}.items():
            body = "".join(f"  {e.render()}\n" for e in els).rstrip("\n")
            (logos / f"{name}-{variant}.svg").write_text(
                svg_document(vb[2], vb[3], body, f"Tenax Solutions ({name} lockup)")
            )

        # Icon: the mark, re-framed onto a square viewBox. Not delivered at all.
        mark = groups["mark"]
        x0, y0, x1, y1 = group_bbox(mark)
        mark_boxes[variant] = (x0, y0, x1, y1)
        side = max(x1 - x0, y1 - y0)
        off = ((side - (x1 - x0)) / 2, (side - (y1 - y0)) / 2)
        body = place(mark, (off[0], off[1], off[0] + (x1 - x0), off[1] + (y1 - y0)))
        (logos / f"icon-{variant}.svg").write_text(
            svg_document(side, side, body, "Tenax Solutions icon")
        )

        # Primary: reassembled from the three groups. No vector was delivered.
        pw, phh, targets = primary_targets()
        body = "\n".join(place(groups[g], targets[g]) for g in ("mark", "tenax", "solutions"))
        (logos / f"primary-{variant}.svg").write_text(
            svg_document(pw, phh, body, "Tenax Solutions (primary lockup)")
        )

    return mark_boxes


def _crop_mark(variant: str, box: tuple[float, float, float, float]) -> Image.Image:
    """Crop the mark out of a Secondary PNG using its exact viewBox mapping.

    The Secondary PNG (4701x4167) is a pixel-exact raster of the 1128x1000
    viewBox, so vector coordinates convert to pixels by a single scale factor.
    """
    png = Image.open(SRC / f"Secondary/PNG/Tenax_Secondary_{SRC_VARIANT[variant]}.png")
    sx = png.width / 1128.0
    sy = png.height / 1000.0
    x0, y0, x1, y1 = box
    return png.convert("RGBA").crop(
        (round(x0 * sx), round(y0 * sy), round(x1 * sx), round(y1 * sy))
    )


def _tile(mark: Image.Image, size: int, pad: float = 0.16, bg: str = TILE_BG) -> Image.Image:
    """Centre the mark on a solid brand tile at ``size`` px square."""
    canvas = Image.new("RGBA", (size, size), bg)
    inner = max(1, int(size * (1 - 2 * pad)))
    scale = min(inner / mark.width, inner / mark.height)
    w, h = max(1, round(mark.width * scale)), max(1, round(mark.height * scale))
    resized = mark.resize((w, h), Image.LANCZOS)
    canvas.paste(resized, ((size - w) // 2, (size - h) // 2), resized)
    return canvas


def build_favicons(out: Path, mark_boxes: dict) -> None:
    fav = out / "favicon"
    fav.mkdir(parents=True, exist_ok=True)

    inverse = _crop_mark("inverse", mark_boxes["inverse"])  # light mark, orange dot

    sizes = {
        "favicon-16x16.png": 16,
        "favicon-32x32.png": 32,
        "favicon-48x48.png": 48,
        "apple-touch-icon.png": 180,
        "android-chrome-192x192.png": 192,
        "android-chrome-512x512.png": 512,
        "mstile-70x70.png": 70,
        "mstile-144x144.png": 144,
        "mstile-150x150.png": 150,
        "mstile-310x310.png": 310,
    }
    for name, size in sizes.items():
        _tile(inverse, size).convert("RGB").save(fav / name)

    # Wide Windows tile: mark centred on a 310x150 field.
    wide = Image.new("RGBA", (310, 150), TILE_BG)
    tile = _tile(inverse, 150)
    wide.paste(tile, ((310 - 150) // 2, 0), tile)
    wide.convert("RGB").save(fav / "mstile-310x150.png")

    # Multi-resolution .ico
    _tile(inverse, 256).convert("RGB").save(
        fav / "favicon.ico", format="ICO", sizes=[(16, 16), (32, 32), (48, 48), (64, 64)]
    )

    # Adaptive SVG favicon: transparent, mark flips with the browser theme.
    logos = out / "logos"
    colour_body = re.search(r"<g .*</g>", (logos / "icon-color.svg").read_text(), re.S).group(0)
    inverse_body = re.search(r"<g .*</g>", (logos / "icon-inverse.svg").read_text(), re.S).group(0)
    side = re.search(r'viewBox="0 0 ([\d.]+)', (logos / "icon-color.svg").read_text()).group(1)
    (fav / "favicon.svg").write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {side} {side}">\n'
        f"  <title>Tenax Solutions</title>\n"
        f'  <g class="on-light">{colour_body}</g>\n'
        f'  <g class="on-dark">{inverse_body}</g>\n'
        f"  <style>\n"
        f"    .on-dark {{ display: none; }}\n"
        f"    @media (prefers-color-scheme: dark) {{\n"
        f"      .on-light {{ display: none; }}\n"
        f"      .on-dark {{ display: inline; }}\n"
        f"    }}\n"
        f"  </style>\n"
        f"</svg>\n"
    )

    # Safari pinned tab: single-colour mask, pure black on transparent.
    _, els = read_svg(SRC / "Secondary/SVG/Tenax_Secondary_Black.svg")
    mark = group_secondary(els)["mark"]
    x0, y0, x1, y1 = group_bbox(mark)
    side_f = max(x1 - x0, y1 - y0)
    off = ((side_f - (x1 - x0)) / 2, (side_f - (y1 - y0)) / 2)
    body = place(mark, (off[0], off[1], off[0] + (x1 - x0), off[1] + (y1 - y0)))
    (fav / "safari-pinned-tab.svg").write_text(
        svg_document(side_f, side_f, re.sub(r'fill="#[0-9a-fA-F]+"', 'fill="#000"', body),
                     "Tenax Solutions")
    )

    (fav / "site.webmanifest").write_text(
        '{\n'
        '  "name": "Tenax Solutions",\n'
        '  "short_name": "Tenax",\n'
        '  "icons": [\n'
        '    { "src": "/android-chrome-192x192.png", "sizes": "192x192", "type": "image/png" },\n'
        '    { "src": "/android-chrome-512x512.png", "sizes": "512x512", "type": "image/png" }\n'
        '  ],\n'
        f'  "theme_color": "{TILE_BG}",\n'
        f'  "background_color": "{TILE_BG}",\n'
        '  "display": "standalone"\n'
        '}\n'
    )


RASTER_SOURCES = {
    "primary": "Primary/PNG/Tenax_Main_{v}.png",
    "secondary": "Secondary/PNG/Tenax_Secondary_{v}.png",
    "submark": "Submark/PNG/Tenax_Submark_{v}.png",
}


def build_rasters(out: Path, mark_boxes: dict) -> None:
    """Downscale the 4k-16k marketing PNGs to sizes usable on the web."""
    raster = out / "raster"
    raster.mkdir(parents=True, exist_ok=True)

    for lockup, pattern in RASTER_SOURCES.items():
        for variant in VARIANTS:
            src = SRC / pattern.format(v=SRC_VARIANT[variant])
            im = Image.open(src).convert("RGBA")
            for width in (480, 960):
                h = max(1, round(im.height * width / im.width))
                im.resize((width, h), Image.LANCZOS).save(raster / f"{lockup}-{variant}-{width}w.png")

    for variant in VARIANTS:
        mark = _crop_mark(variant, mark_boxes[variant])
        for size in (128, 256, 512):
            h = max(1, round(mark.height * size / mark.width))
            mark.resize((size, h), Image.LANCZOS).save(raster / f"icon-{variant}-{size}.png")


def build(out: Path) -> None:
    mark_boxes = build_logos(out)
    build_favicons(out, mark_boxes)
    build_rasters(out, mark_boxes)


# ---------------------------------------------------------------------------


def verify() -> int:
    """Rebuild into a temp dir and diff against the committed assets."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_out = Path(tmp) / "assets"
        build(tmp_out)
        mismatched, missing = [], []
        for built in sorted(tmp_out.rglob("*")):
            if built.is_dir():
                continue
            rel = built.relative_to(tmp_out)
            committed = OUT / rel
            if not committed.exists():
                missing.append(rel)
            elif not filecmp.cmp(built, committed, shallow=False):
                mismatched.append(rel)
        for rel in missing:
            print(f"MISSING    {rel}")
        for rel in mismatched:
            print(f"MISMATCH   {rel}")
        if missing or mismatched:
            print(f"\n{len(missing)} missing, {len(mismatched)} mismatched")
            return 1
        print("assets are reproducible: committed output matches a fresh build")
        return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--verify", action="store_true", help="diff a fresh build against committed assets")
    args = ap.parse_args()

    if not SRC.is_dir():
        print(f"error: agency delivery not found at {SRC}", file=sys.stderr)
        return 2
    if args.verify:
        return verify()

    built_dirs = ("logos", "favicon", "raster")
    for sub in built_dirs:
        shutil.rmtree(OUT / sub, ignore_errors=True)
    build(OUT)
    count = sum(1 for sub in built_dirs for p in (OUT / sub).rglob("*") if p.is_file())
    print(f"built {count} files into {OUT.relative_to(ROOT)}/{{{','.join(built_dirs)}}}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
