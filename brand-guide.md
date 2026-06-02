# Tenax Brand Guide

Master brand assets live in this repo under `assets/icons/` (the Tenax icon) and
`assets/logos/` (the Tenax + IPP main logo) — the `@4x.png` marketing originals.
Consuming apps vendor their own copies from these (see the on-call note below);
they do not depend on this repo at runtime.

## Color Scheme

Tenax brand colors extracted from tenaxsolutions.com:

Background: #181818 (warm near-black)
Card surfaces: #242424
Border: #3d3020 (warm dark, gold-tinted)
Gold accent: #ef910a (primary Tenax brand gold)
Light gold: #f0d085
Text: #eaeaea
Muted text: #9a8e7e


UI usage (applied in the on-call admin; reuse across Tenax web surfaces)

Headings & buttons share the primary gold #ef910a so they read as one family:
- Buttons (primary/active): background #ef910a, dark text #181818.
- Card headings (h2, uppercase): #ef910a.
- Section group titles (the collapsible nav sections): #ef910a, larger (1.25rem)
  and bold (700), with a matching gold caret.
- Active nav chip: text + border #ef910a.

Reserve the other tones for hierarchy, not for headings:
- Light gold #f0d085 — subtle accents/hover only. (It reads dull for headings; do
  not use it for titles.)
- Muted #9a8e7e — secondary labels, sub-headings (h3), helper text, table headers.
- Text #eaeaea — body copy and primary values.

Logo & favicon (as applied in the on-call app + course — keep consistent)

Source asset: TENAX ICON_ALABASTER@4x.png (the Alabaster / near-white icon).
Both the in-app logo AND the favicon use this single asset (the gold Gradient
icon was trialed for the favicon and reverted — Alabaster is the chosen mark
everywhere).

Served copies (clean names; one shared origin so every page + the login screen
reference the same files):
- on-call app:     static/tenax-icon-alabaster.png   (logo)
                   static/favicon.png                (favicon — byte-identical copy)
- training course: soc-oncall-course/tenax-icon-alabaster.png and .../favicon.png

Placement & sizing:
- Admin dashboard header: alabaster icon ~1.8rem tall, left of the
  "Tenax Call Manager Admin" wordmark.
- Login screen: alabaster icon centered, ~2.6rem tall, above the centered heading.
- Course nav: alabaster icon ~26-28px tall, left of the title.
- Favicon markup: <link rel="icon" type="image/png" href="/static/favicon.png">.

Note: black reads invisible on the #181818 background, so Alabaster (chosen
default) and the gold Gradient icon are the on-dark options. Alabaster can look
faint on a light browser tab; TENAX ICON_GRADIENT@4x is the alternative if a
tab-legible favicon is ever wanted.
