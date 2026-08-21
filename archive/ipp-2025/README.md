# Tenax IPP identity (archived)

The brand this repo carried before the 2026 Tenax Solutions rebrand. Superseded by
[`../../brand-guide.md`](../../brand-guide.md).

**Deprecated, but not dead.** Do not use it for new work — and do not delete it, because
it is still what several live surfaces render:

| Surface | Status as of 2026-08-21 |
|---------|-------------------------|
| tenaxsolutions.com | Still fully on the IPP brand — gold, Typekit, "TENAX IPP" wordmark |
| SIEM / Wazuh dashboard | Migrated — see `applications/siem-whitelabel/` |
| On-call app, training course | Separate repos; each vendored its own copy of these assets and migrates independently |

## What changed

| | Tenax IPP (this folder) | Tenax Solutions (2026) |
|---|---|---|
| Wordmark | TENAX IPP | TENAX SOLUTIONS |
| Background | `#181818` | Command Black `#0D1016` |
| Accent | gold `#ef910a` → `#f0d085` gradient | Signal Orange `#F45A3C`, flat |
| Secondary | — | Sentinel Blue `#213D6B` |
| Text | `#eaeaea` | Secure White `#F5F5F3` |
| Typeface | `aktiv-grotesk` (Adobe Typekit) | Urbanist + Sora (Google, OFL, self-hosted) |
| Mark | gradient icon | angular quadrant mark with orange dot |

Nothing carries over, and there is no gold anywhere in the new system.

The new identity does still use a gradient, but a different one and in a narrower role:
the old brand ran gold → light-gold across CTAs *and* highlighted section backgrounds,
while the new one uses Sentinel Blue → Signal Orange for primary actions only. The logo
itself is completely flat.

## Contents

- `brand-guide.md` — the previous guide, including its (now inverted) claim that
  tenaxsolutions.com is the authoritative brand source
- `icons/` — Tenax icon, `@4x` marketing originals, all tones
- `logos/` — Tenax + IPP main logo, `@4x` originals, all tones

## Migrating an app off this

1. Replace the token block with `assets/tokens/tenax.css`; map old names to new
   (`--accent` → `--tenax-accent`, `--bg` → `--tenax-bg`, and so on).
2. Drop the Typekit `<link>` and the `use.typekit.net` preconnect; link
   `assets/fonts/fonts.css` instead.
3. Swap `aktiv-grotesk` → Sora and `aktiv-grotesk-extended` → Urbanist.
4. Replace logo files with `assets/logos/*-inverse.svg` (dark) or `*-color.svg` (light).
5. Replace gold-gradient rules with `--tenax-accent-gradient` (Sentinel Blue → Signal
   Orange) and only on primary actions — not on section backgrounds, as the old brand did.
   Solid orange is never a large fill. See the accent rule in the current guide.
6. Replace the favicon with `assets/favicon/`. The old guide pointed at
   `oncall.tenaxsolutions.com/static/favicon.png`; that URL still serves the old mark.
7. Run `tools/check-contrast.py` if you introduce any colour of your own.
