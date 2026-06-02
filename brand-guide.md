# Tenax Web Brand Guide

The shared visual standard for Tenax web surfaces — admin tools, dashboards,
portals, and the like. New and existing apps should adopt the tokens and rules
below so every surface looks and behaves consistently.

Master brand assets live in this repo under `assets/icons/` (the Tenax icon) and
`assets/logos/` (the Tenax + IPP main logo) — the `@4x.png` marketing originals.
Apps **vendor their own copies** from these into their build; they do not depend
on this repo at runtime.

## Palette

| Role | Hex | Notes |
|------|-----|-------|
| Background | `#181818` | warm near-black page background |
| Surface (card) | `#242424` | cards, panels, inputs on dark |
| Border | `#3d3020` | warm, gold-tinted |
| Gold (accent) | `#ef910a` | primary Tenax brand gold |
| Light gold | `#f0d085` | subtle accents / hover only |
| Text | `#eaeaea` | body copy and primary values |
| Muted | `#9a8e7e` | secondary labels, sub-headings, helper text, table headers |

Functional status colors (not brand, but keep them consistent across apps):
success `#22c55e`, error `#ef4444`, warning `#eab308`, info `#3b82f6`.

## CSS tokens

Copy this into each app's `:root` so values match exactly:

```css
:root {
  --bg: #181818; --card: #242424; --border: #3d3020;
  --text: #eaeaea; --muted: #9a8e7e;
  --accent: #ef910a; --accent-light: #f0d085;
  --green: #22c55e; --red: #ef4444; --yellow: #eab308; --blue: #3b82f6;
}
```

## UI rules

Headings and primary buttons share the gold `#ef910a` so they read as one family:

- **Buttons** (primary / active): gold background, dark `#181818` text — never
  white on gold (low contrast).
- **Card / section headings** (h2, uppercase): gold `#ef910a`.
- **Section or tab headings**: gold, larger (~`1.25rem`) and bold (`700`).
- **Active nav / tab chip**: gold text + gold border; inactive chips are muted.

Reserve the other tones for hierarchy, not for headings:

- **Light gold `#f0d085`** — subtle accents / hover only (reads dull for headings;
  don't use it for titles).
- **Muted `#9a8e7e`** — secondary labels, sub-headings (h3), helper text, table headers.
- **Text `#eaeaea`** — body copy and primary values.

## Logo & favicon

- **Logo:** the Alabaster (near-white) Tenax icon —
  `assets/icons/TENAX ICON_ALABASTER@4x.png` — placed on the dark UI, where it
  reads cleanly. (Black is invisible on `#181818`.)
- **Favicon:** the same Alabaster icon. The gold **Gradient** icon
  (`assets/icons/TENAX ICON_GRADIENT@4x.png`) is the alternative if a
  tab-legible favicon on light browser tabs is ever wanted.
- **Sizing:** scale to context — compact in a header/nav (~`1.8–2rem` tall),
  larger on a login/splash screen (~`2.5rem`), typically left of or centered
  above the app title.
- **Wordmark:** the app title may sit beside the logo in `#eaeaea` text; the
  gold/brand mark is carried by the icon.

## Reference implementation

The on-call **Call Manager** admin app is the canonical implementation of this
guide — full palette and rule conformance. Use it as the working example when
building a new Tenax surface.
