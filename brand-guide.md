# Tenax Web Brand Guide

The shared visual standard for Tenax web surfaces — admin tools, dashboards, portals, and the like. New and existing apps should adopt the tokens and rules below so every surface looks and behaves consistently.

**Primary brand reference:** [tenaxsolutions.com](https://www.tenaxsolutions.com) is the authoritative source for all brand decisions (colors, typography, logo usage). Individual apps must match its visual language.

Master brand assets live in this repo under `assets/icons/` (the Tenax icon) and `assets/logos/` (the Tenax + IPP main logo) — the `@4x.png` marketing originals. Apps **vendor their own copies** from these into their build; they do not depend on this repo at runtime.

---

## Palette

Derived from tenaxsolutions.com's live stylesheet.

| Role | Hex | Notes |
|------|-----|-------|
| Background | `#181818` | warm near-black page background |
| Surface (card) | `#242424` | cards, panels, inputs on dark |
| Border | `#3d3020` | warm, gold-tinted |
| Gold (accent) | `#ef910a` | primary Tenax brand gold — buttons, headings, active states |
| Light gold | `#f0d085` | gradient end-stop; subtle accents and hover only |
| Text | `#eaeaea` | body copy and primary values |
| Muted | `#9a8e7e` | secondary labels, sub-headings, helper text, table headers |

**Gold gradient** (CTAs, hero sections, accent bands): `linear-gradient(90deg, #ef910a, #f0d085)`
This gradient is used on tenaxsolutions.com for primary buttons and highlighted section backgrounds.

Functional status colors (not brand, keep consistent across apps): success `#22c55e`, error `#ef4444`, warning `#eab308`, info `#3b82f6`.

---

## Typography

Tenax uses **Adobe Typekit** fonts loaded via `https://use.typekit.net`.

| Role | Font family | Weight |
|------|-------------|--------|
| Body / UI | `aktiv-grotesk, sans-serif` | 400 |
| Headings / CTAs | `aktiv-grotesk-extended, sans-serif` | 500–700 |

- All nav links, body copy, and form labels use `aktiv-grotesk`.
- Headings (`h1`–`h2`) and CTA button labels use `aktiv-grotesk-extended` in uppercase.
- Fallback for both: `sans-serif`.

Include the Typekit preconnect in each app's `<head>`:

```html
<link rel="preconnect" href="https://use.typekit.net" crossorigin>
```

---

## CSS tokens

Copy this into each app's `:root` so values match exactly:

```css
:root {
  /* Palette */
  --bg: #181818;
  --card: #242424;
  --border: #3d3020;
  --text: #eaeaea;
  --muted: #9a8e7e;
  --accent: #ef910a;
  --accent-light: #f0d085;
  --accent-gradient: linear-gradient(90deg, #ef910a, #f0d085);

  /* Status */
  --green: #22c55e;
  --red: #ef4444;
  --yellow: #eab308;
  --blue: #3b82f6;

  /* Typography */
  --font-body: aktiv-grotesk, sans-serif;
  --font-heading: aktiv-grotesk-extended, sans-serif;
}
```

---

## UI rules

### Buttons

- **Primary / active buttons:** gold gradient background (`--accent-gradient`), dark `#181818` text — never white text on gold (poor contrast).
- **Secondary buttons:** `--card` background, `--text` color, `--border` border.
- Button labels use `aktiv-grotesk-extended`, uppercase, font-weight 700.

### Headings

- `h1`, `h2` (section titles, uppercase): `--accent` gold `#ef910a`, `aktiv-grotesk-extended`, weight 500–700.
- `h3` / sub-section labels: `--muted` `#9a8e7e`.
- Body copy and primary values: `--text` `#eaeaea`.

### Navigation

- Active nav / tab chip: gold text + gold border; inactive chips use `--muted`.
- Nav background matches `--bg` `#181818`.

### Hierarchy rule

Reserve tones for their intended roles:

- Light gold `#f0d085` — gradient end-stop and hover accents only; never for standalone headings (reads dull against dark).
- Muted `#9a8e7e` — sub-headings, helper text, table headers.
- Text `#eaeaea` — body copy and primary values.

---

## Logo & favicon

### Logo

Use the **Gradient + White** variant as the primary wordmark on dark backgrounds — this is what tenaxsolutions.com uses in its navbar:

- **Dark backgrounds (all apps):** `assets/logos/TENAX IPP MAIN LOGO_GRADIENT_WHITE1@4x.png` — gradient icon + white text. Matches the live site.
- **Light backgrounds:** `assets/logos/TENAX IPP MAIN LOGO_GRADIENT_BLACK@4x.png` or `TENAX IPP MAIN LOGO_BLACK@4x.png`.
- **Icon-only (no wordmark):** `assets/icons/TENAX ICON_GRADIENT@4x.png` (colored), `TENAX ICON_ALABASTER@4x.png` (white/near-white).

Never use the black icon on `#181818` — it is invisible.

**Sizing:** scale to context — compact in a header/nav (1.8–2 rem tall), larger on a login/splash screen (2.5 rem+), left-aligned or centered above the app title.

**Wordmark:** the app title may sit beside the icon in `#eaeaea`; the brand mark is carried by the icon.

### Favicon

**Preferred favicon:** `https://oncall.tenaxsolutions.com/static/favicon.png`

Use this exact file (or a locally vendored copy of it) as the favicon for all Tenax web apps. It is the canonical tab icon established by the Call Manager admin. The `TENAX ICON_GRADIENT@4x.png` asset from this repo is the source for generating it if a rebuild is needed.

```html
<link rel="icon" href="/static/favicon.png">
```

---

## Reference implementation

The **Tenax Call Manager admin** (`oncall.tenaxsolutions.com/admin`) is the canonical implementation of this guide — full palette, gradient buttons, alabaster icon in the nav, and the preferred favicon. Use it as the working reference when building a new Tenax surface.

The **tenaxsolutions.com** marketing site is the primary brand authority — any token, color, or font decision should be verified against what is live there.