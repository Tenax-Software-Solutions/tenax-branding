# Tenax Solutions — Web Brand Guide

The shared visual standard for Tenax web surfaces: admin tools, dashboards, portals,
consoles. New and existing apps adopt the tokens and rules below so every surface looks
like it came from the same company.

**Brand authority:** `source/Tenax Solutions _Lite Visual Identity.pdf` (Digital Mules,
July 2026) and the logo package beside it. That PDF is the source of truth for colour,
type and logo usage. This document is the *web* application of it — the identity guide is
a "Lite" package aimed at marketing, so everything it doesn't cover (surfaces, states,
spacing, status colours) is defined here and marked as such.

> **tenaxsolutions.com is not currently a reference.** It still runs the previous
> Tenax IPP identity — gold `#ef910a`, Adobe Typekit, "TENAX IPP" wordmark. It is a
> consumer of this guide that has not migrated yet, not an authority. The prior guide
> is preserved at `archive/ipp-2025/brand-guide.md`.

---

## Palette

Four named colours. Everything else derives from their tint ramps.

| Role | Name | Hex | RGB | CMYK |
|------|------|-----|-----|------|
| Foundation | **Command Black** | `#0D1016` | 13, 16, 22 | 41, 27, 0, 91 |
| Secondary | **Sentinel Blue** | `#213D6B` | 33, 61, 107 | 69, 43, 0, 58 |
| Accent | **Signal Orange** | `#F45A3C` | 244, 90, 60 | 0, 63, 75, 4 |
| Light | **Secure White** | `#F5F5F3` | 245, 245, 243 | 0, 0, 1, 4 |

Tint ramps, as printed on the identity guide's palette page. Step 1 is the named colour:

| | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| black | `#0D1016` | `#24272C` | `#494B50` | `#85878A` | `#EFEFF0` |
| blue | `#213D6B` | `#365076` | `#586D8D` | `#8F9DB3` | `#C7CED9` |
| orange | `#F45A3C` | `#F56A4F` | `#F6836C` | `#F9AC9D` | `#FCD5CE` |

The black ramp supplies surfaces, borders and muted text. Use it instead of inventing
greys.

### The two rules that aren't obvious

Both come from measured contrast, not taste. `tools/check-contrast.py` enforces them.

**1. Sentinel Blue is a surface, never a foreground.**
Blue on Command Black is **1.76:1** — invisible. It works only as a *filled field*
carrying Secure White text (**9.89:1**). Never use it for body copy, links, icons or
borders on a dark background.

**2. White text never goes on Signal Orange.**
Secure White on Signal Orange is **3.02:1** — it fails AA. Orange fills take Command
Black labels (**5.78:1**). In light mode orange can't carry text at all, which is why
`--tenax-accent-text` exists as a darkened same-hue variant.

Reference ratios on Command Black: Secure White 17.44 · Signal Orange 5.78 ·
Sentinel Blue 1.76.

---

## Signal Orange — the accent rule

Signal Orange is the identity's only accent and the sole non-neutral element in the
logo. It marks **brand and navigational emphasis**, at small scale:

- individual words inside a sentence
- icons and iconography strokes
- active nav items, tab underlines, selected-state indicators
- focus rings
- thin rules and dividers that need to read as branded

It is **not** a status colour, and **solid orange is never a large fill**. Do not paint
a hero band, a card or a table row in it.

The one place orange appears as a fill is the primary action gradient below, where it is
the end stop rather than the whole surface.

The approved homepage design applies this with real discipline: **exactly one keyword per
headline** in orange, never a phrase and never two — "Ahead of the *Threat*.", "*Security*
You Can Measure.", "Proactive Security Starts *Here*.", "Comprehensive *Cybersecurity*
Services". Everything else in the headline is Secure White. Icons are orange line-art, and
small category labels ("Proactive", "Expert-Led") are orange over a muted sub-label.

### Orange vs. severity

This matters most in the SIEM, where orange is conventionally "high severity".

Signal Orange sits at hue **10°**. Every red that passes AA on our surfaces lands within
**7–12°** of it (`#DC2626` 10°, `#F85149` 7°, `#E5484D` 12°). Widening the search to a
25°+ separation only turns up pinks, which no longer read as danger. **Hue cannot
separate brand orange from error red.**

So they are separated by **form** instead:

| | Brand orange | Status colours |
|---|---|---|
| Appears as | text, icons, rules, focus rings | filled badges, row left-borders, dots, validation text |
| Never appears as | any fill | inline prose emphasis |

Different shapes, so adjacency is never ambiguous — and severity keeps conventional,
learnable colours. `reference/index.html` demonstrates the two side by side.

Additional scoping rule: **brand orange never appears inside alerting or validation
UI.** Inside an alert panel, a severity table or a form-error region, orange is off the
table entirely.

### Primary actions: the blue → orange gradient

`--tenax-accent-gradient` — `linear-gradient(90deg, #213D6B, #F45A3C)`.

This is **not in the identity PDF**. It comes from the approved homepage design, which
uses it for every primary CTA ("Explore Services", "Learn More", "View All Services") and
for the active tab chip. It is the one place the two brand colours meet, and it is the
only sanctioned orange fill.

- Primary action: gradient fill, **pill** (`--tenax-radius-full`), white label,
  sentence case.
- Secondary action: ghost pill — transparent, `--tenax-border-strong`, `--tenax-text` label.
- Never use solid `--tenax-accent` as a button fill.

**Label contrast.** A white label clears 4.5:1 across the first ~70% of the ramp and falls
to 3.29:1 at the pure-orange end. Centred labels sit over the compliant region, so keep
primary button text short; if a long label is unavoidable, switch to
`--tenax-on-accent-gradient-safe` (Command Black, 5.78:1 at the worst point).
`tools/check-contrast.py` samples the gradient and reports where the threshold falls.

### Status colours

Not part of the identity guide — defined here because apps need them. All pass AA on
both `--tenax-bg` and `--tenax-surface`, in both themes.

| Role | Dark | Light |
|------|------|-------|
| Success | `#3FB950` | `#1A7F37` |
| Info | `#58A6FF` | `#0A5AA8` |
| Warning | `#E3B341` | `#8A6300` |
| Error / critical | `#FF6B63` | `#C1290B` |

---

## Typography

| Role | Family | Weights |
|------|--------|---------|
| Display — headings, buttons, labels | **Urbanist** | 400–800 |
| Body — copy, UI, forms | **Sora** | 400–700 |
| Code, logs, hostnames | system mono stack | — |

Both are Google Fonts under **SIL OFL 1.1** and are **self-hosted** in
`assets/fonts/` — variable woff2, ~80 KB for both families and all weights. This
replaces the previous Adobe Typekit dependency, which mattered: several Tenax surfaces
(the on-prem Wazuh dashboard especially) have no outbound internet, and a webfont that
silently fails to load takes the brand's typography with it.

The identity guide specifies no monospace face. The system stack is used for log and
code output; if marketing wants a specified mono, that's an open request.

**Case and tracking.** The wordmark sets SOLUTIONS with wide letterspacing, but the
homepage design does *not* carry that into UI text: buttons, eyebrow chips and labels are
all **sentence case**. Reserve `--tenax-tracking-wide` (`0.18em`) for dense-data table
headers, where it aids scanning. Never on body copy, buttons or chips.

Type scale: `--tenax-text-xs` `0.75rem` → `--tenax-text-5xl` `3.25rem`; see
`reference/index.html` for the rendered scale.

---

## Logo

Four lockups, four colour variants each, in `assets/logos/`.

| Lockup | Contents | Use for |
|--------|----------|---------|
| `primary` | mark + TENAX SOLUTIONS, horizontal | website headers, landing pages, sales collateral |
| `secondary` | mark above TENAX above SOLUTIONS | narrow/vertical layouts, social, email signatures |
| `submark` | mark + TENAX, horizontal | footers, section dividers, internal docs, merch |
| `icon` | mark alone | favicons, app icons, avatars, small-scale UI |

| Variant | Composition | Use on |
|---------|-------------|--------|
| `inverse` | light mark + orange dot | **dark backgrounds — the default for Tenax apps** |
| `color` | dark mark + orange dot | light backgrounds |
| `white` | pure white, no dot | photography, Sentinel Blue fields, single-colour repro |
| `black` | solid dark, no dot | light single-colour repro, faxes, engraving |

Prefer `inverse` and `color`; they carry the orange dot, which is the only brand colour
in the mark. `white`/`black` drop it and should be used only where a second colour isn't
available.

**Header:** the homepage uses `primary-inverse.svg` in the navbar, which confirms it as
the default for Tenax app headers.

**Sizing:** 1.8–2 rem tall in a header or nav; 2.5 rem+ on a login or splash screen.
Never place the `color` variant on Command Black, or `inverse` on Secure White — the
mark disappears.

**Clear space:** keep at least the height of the mark's orange dot clear on all sides.

### Derived assets

Two things the agency delivery is missing, reconstructed by `tools/build-assets.py`:

- **The icon.** `Icon/` shipped with every format subfolder present and every one empty.
  The icon is extracted from the Secondary lockup's vector, where the mark is a separable
  group, and re-framed onto a square viewBox.
- **The Primary vector.** Primary shipped as 12.8k-wide PNGs only — no SVG, EPS or PDF.
  It is reassembled from the same three artwork groups the other lockups use. Verified by
  rendering the result at the source PNG's full resolution and diffing: the alpha bounding
  box matches **exactly**, and the difference is 0.39% of the artwork.

  For scale, the same test run against `secondary` — which is a byte-identical re-emit of
  the delivered vector — scores 1.02%, because forcing the render to the PNG's pixel
  dimensions introduces a 0.013% aspect stretch. The reconstruction's error is therefore
  below the noise floor of a known-good control.

Both are flagged in `ASSET-REQUESTS.md` for the agency to supply authoritatively.

Derived SVGs also use presentation attributes rather than the delivered files'
`<style>` blocks, whose generic `.cls-1`/`.cls-2` selectors collide with each other and
with the host page the moment two logos are inlined into one document.

---

## Favicon

`assets/favicon/` holds a complete set. The mark sits on a Command Black tile so it stays
legible against both light and dark browser chrome.

```html
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
```

`favicon.svg` is theme-adaptive — it carries both the `color` and `inverse` marks and
switches on `prefers-color-scheme`. `safari-pinned-tab.svg` is a pure-black mask, as
Safari requires.

---

## Theming

**Dark is the default and applies unconditionally.** Light is opt-in via
`<html data-theme="light">`, for printed reports, PDF exports and light-background
documentation.

This deliberately does *not* follow `prefers-color-scheme`: Tenax apps are dark
surfaces, and a user's OS setting shouldn't silently repaint a security console.

---

## Using the tokens

Copy `assets/tokens/tenax.css` into the app and link it. Every token is prefixed
`--tenax-` so it can coexist with an app's existing custom properties — which matters for
the Wazuh dashboard, which has plenty of its own.

```html
<link rel="stylesheet" href="/assets/fonts/fonts.css">
<link rel="stylesheet" href="/assets/tokens/tenax.css">
<body class="tenax">
```

`assets/tokens/tenax.tokens.json` mirrors the same values for non-CSS consumers
(Tailwind configs, report generators, third-party dashboard themes). It is generated
from the CSS by `tools/build-tokens.py` — edit the CSS, never the JSON.

Key semantic tokens:

| Token | Purpose |
|-------|---------|
| `--tenax-bg` / `--tenax-surface` / `--tenax-surface-raised` | page, card, raised card |
| `--tenax-border` / `--tenax-border-strong` | hairline separator / deliberate divider |
| `--tenax-text` / `--tenax-text-muted` / `--tenax-text-subtle` | body / helper / large-only |
| `--tenax-accent` / `--tenax-accent-text` | orange fill+rule / orange as words |
| `--tenax-on-accent` | label on an orange fill (dark, never white) |
| `--tenax-blue-surface` / `--tenax-on-blue` | Sentinel Blue field + its text |
| `--tenax-success` `-info` `-warning` `-error` / `--tenax-on-status` | status fills + labels |
| `--tenax-focus` | focus ring |

If you add a colour, add it to the contract in `tools/check-contrast.py` and run it.

---

## Reference implementation

`reference/index.html` — open it in a browser. It renders the palette with contrast
ratios computed live from the actual token values, the type scale, every lockup on every
valid background, and real components. It's the fastest way to check whether something
you built matches, and it doubles as the visual regression check when a token changes.

---

## Imagery

From the identity guide: technology, architecture, data and authentic collaboration.
Emphasise innovation, resilience and *proactive* security rather than reactive
problem-solving — environments and people working with purpose. Abstract technology
elements and modern infrastructure, polished and premium. Every image should support the
message that Tenax helps organisations stay ahead of evolving threats.

---

## Shape language

From the homepage design:

- Buttons, chips and eyebrow labels are **pills** — `--tenax-radius-full`.
- Cards and panels use `--tenax-radius-xl` (16px).
- The hero carries a subtle orange particle texture over Command Black. Decorative only;
  it must never sit behind body copy.

---

## Open items

- **Hex discrepancies** between the identity PDF and the shipped vectors — see
  `ASSET-REQUESTS.md`. Tokens follow the PDF; delivered artwork is left untouched.
- **Monospace face** unspecified by the identity guide.
- **Exact gradient stops.** Read from the homepage design at screenshot fidelity and
  implemented as Sentinel Blue → Signal Orange. Worth confirming the precise stops and
  angle with the designer.
