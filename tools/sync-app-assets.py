#!/usr/bin/env python3
"""Populate each application's vendored asset directory from assets/.

Applications keep their own copy of the marks they need so the directory can be
copied to a server and run standalone -- the SIEM whitelabel script is invoked
as `sudo bash /root/siem-whitelabel/apply-whitelabel.sh` on a host that has no
checkout of this repo. Vendoring by hand is how those copies drift, so the copy
is generated instead.

Filenames here describe the *background* a mark is for, not its ink colour, which
matches how the Wazuh dashboard names its own targets (`*_on_light`, `*_on_dark`).

Usage:
    python3 tools/sync-app-assets.py            # copy
    python3 tools/sync-app-assets.py --check    # fail if a vendored copy is stale
"""

from __future__ import annotations

import argparse
import filecmp
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

SIEM = ROOT / "applications" / "siem-whitelabel" / "logos"

# destination (relative to the app's asset dir) -> source in assets/
SIEM_FILES = {
    "tenax_logo_on_light.svg": "logos/primary-color.svg",
    "tenax_logo_on_dark.svg": "logos/primary-inverse.svg",
    "tenax_icon_on_light.svg": "logos/icon-color.svg",
    "tenax_icon_on_dark.svg": "logos/icon-inverse.svg",
    # PDF report generation needs a raster; reports are printed on white.
    "tenax_logo_on_light.png": "raster/primary-color-960w.png",
    "tenax_favicon.ico": "favicon/favicon.ico",
}

# The whitelabel script replaces a fixed list of favicon filenames; the 2026
# favicon set covers all of them, so the config-only fallback is no longer needed.
SIEM_FAVICONS = [
    "favicon.ico",
    "favicon-16x16.png",
    "favicon-32x32.png",
    "apple-touch-icon.png",
    "android-chrome-192x192.png",
    "android-chrome-512x512.png",
    "safari-pinned-tab.svg",
    "mstile-70x70.png",
    "mstile-144x144.png",
    "mstile-150x150.png",
    "mstile-310x150.png",
    "mstile-310x310.png",
]


def planned() -> dict[Path, Path]:
    plan = {SIEM / dst: ASSETS / src for dst, src in SIEM_FILES.items()}
    plan |= {SIEM / "favicons" / name: ASSETS / "favicon" / name for name in SIEM_FAVICONS}
    return plan


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true", help="fail if a vendored copy is stale")
    args = ap.parse_args()

    plan = planned()
    missing_sources = [s for s in plan.values() if not s.exists()]
    if missing_sources:
        for s in missing_sources:
            print(f"error: source missing: {s.relative_to(ROOT)}", file=sys.stderr)
        print("run tools/build-assets.py first", file=sys.stderr)
        return 2

    stale = []
    for dst, src in plan.items():
        if not dst.exists() or not filecmp.cmp(src, dst, shallow=False):
            stale.append(dst)

    if args.check:
        for dst in stale:
            print(f"STALE  {dst.relative_to(ROOT)}")
        if stale:
            print(f"\n{len(stale)} vendored file(s) out of date — run tools/sync-app-assets.py")
            return 1
        print(f"all {len(plan)} vendored application assets are up to date")
        return 0

    for dst, src in plan.items():
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)
    print(f"synced {len(plan)} files into applications/siem-whitelabel/logos/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
