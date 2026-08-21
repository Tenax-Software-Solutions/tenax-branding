# Asset requests — 2026 Tenax Solutions identity

Gaps and inconsistencies in the logo package delivered with
*Tenax Solutions _Lite Visual Identity* (Digital Mules, July 2026). Written to be sent
to the agency as-is.

We have worked around the two blocking gaps locally (see *What we did in the meantime*),
but those are our reconstructions, not authoritative originals — we'd like the real
files.

---

## 1. The `Icon/` folder is empty — every format

`Tenax Logos/Logo Package/Icon/` contains `EPS/`, `JPG/`, `PDF/`, `PNG/` and `SVG/`
subfolders. **All five are empty.** No icon asset shipped in any format.

The identity guide devotes a full page to the icon and names its uses as "website
favicon and browser tabs, social media profile images, mobile app icons and software
interfaces" — so this is the asset we need most for web and product work.

**Requested:** the icon in SVG, PNG (transparent) and EPS, in all four colour variants
(Color, Inverse, Black, White), on a square canvas with defined clear space.

## 2. The Primary lockup has no vector

`Primary/` shipped only:

- `PNG/` — 4 variants at ~12,847 × 4,168 px
- `JPG/` — a single file, `Tenax_Main_Black-50.jpg`

`Primary/SVG/`, `Primary/EPS/` and `Primary/PDF/` are **all empty**.

Primary is the lockup the identity guide designates for "website headers and landing
pages" — the one place an SVG matters most. Secondary and Submark both shipped complete
vector sets, so this looks like an export oversight rather than a deliberate omission.

**Requested:** `Tenax_Main_{Color,Inverse,Black,White}` as SVG, EPS and PDF, matching the
Secondary/Submark structure.

## 3. Colour values disagree between the guide and the artwork

The palette page and the shipped vectors specify different hexes for the same colours:

| Colour | Identity guide (p. 2) | Shipped SVG/EPS artwork |
|--------|----------------------|--------------------------|
| Signal Orange | `#F45A3C` | `#f15c3d` |
| Command Black | `#0D1016` | `#101217` (Color variants) |
| Command Black | `#0D1016` | `#231f20` (Black variants) |
| Secure White | `#F5F5F3` | `#f5f5f3` ✓ matches |

`#231f20` is Illustrator's default rich black, which suggests the Black variants were
never repointed at the brand colour.

The differences are visually negligible but they make it impossible to say which value is
canonical, and they will resurface every time someone diffs a logo against a token.

**Requested:** confirm which set is authoritative and re-export the artwork to match.
In the meantime our UI tokens follow the guide (`#F45A3C`, `#0D1016`) and the delivered
artwork is shipped **unmodified** — we did not repaint it.

## 4. No favicon deliverables

Nothing in the package targets browser or app-icon use: no `.ico`, no sized PNGs, no
Apple touch icon, no maskable/monochrome variants.

**Requested:** ideally an icon master with defined safe-area padding for square crops, so
favicons can be generated consistently rather than each team cropping its own.

## 5. Everything is at print resolution

The smallest raster in the package is 1,129 px wide; the largest is 15,797 px. There are
no web-sized exports.

**Requested:** web exports (roughly 480 / 960 / 1920 px wide) per lockup and variant,
or confirmation that downscaling from the print masters is acceptable — which is what
we're doing now.

## 6. Smaller inconsistencies

- **PDF exports are incomplete.** Secondary and Submark ship PDFs for `Black` and
  `Color` only; `Inverse` and `White` are missing. Their EPS sets are complete.
- **Primary JPG is incomplete.** Only `Black-50` shipped; Secondary and Submark each got
  four (`Black-50/80`, `Color-50/80`).

## 7. Specifications the "Lite" guide doesn't cover

Not defects — scope. Flagging them because product work needs answers, and we've had to
choose defaults:

- **Minimum sizes and clear space** for each lockup. We're using "clear space = the
  height of the orange dot".
- **Monospace face** for log output, hostnames and code. The SIEM needs one; we default
  to the system stack.
- **Status/severity colours.** The guide has no success/warning/error palette. We defined
  one, constrained by the finding that *no accessible red is distinguishable by hue from
  Signal Orange* — every candidate lands within 7–12° of it. See `brand-guide.md`.
- **How far Signal Orange goes in UI.** Marketing's guidance is accent-only (word
  highlights, icons). Confirmation against the homepage mockup would let us finalise
  primary button colour, which is currently provisional.

---

## What we did in the meantime

So work isn't blocked. All of it is reproducible via `tools/build-assets.py`:

- **Icon** — extracted from the Secondary lockup's SVG, where the mark is a separable
  group, and re-framed onto a square viewBox. All four variants.
- **Primary vector** — reassembled from the three artwork groups (mark, TENAX,
  SOLUTIONS) that the delivered lockups share. Their proportions are identical across
  Primary, Secondary and Submark (measured aspect ratios agree to four decimal places),
  so this repositions the real artwork rather than redrawing it.

  Verified by rendering the reconstruction at the source PNG's full 12,847 × 4,168 and
  diffing against it: **the alpha bounding box matches exactly**, and the difference is
  0.39% of the artwork.

  As a control, the same test against the Secondary lockup — where our SVG is a
  byte-identical re-emit of your delivered vector — scores 1.02%, since rendering to the
  PNG's exact pixel dimensions introduces a 0.013% aspect stretch. So the reconstruction
  differs from the delivered PNG by less than a known-identical file does.

- **Favicons** — generated from the mark on a Command Black tile.
- **Web rasters** — downscaled from the print masters.

These are good enough to ship. They are still our reconstruction of someone else's
artwork, so we'd rather replace them with authoritative exports.
