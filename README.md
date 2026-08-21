# tenax-branding

Single source of truth for Tenax Solutions brand assets and the tools that apply them.

Currently carrying the **2026 Tenax Solutions identity** (Digital Mules, July 2026),
which fully replaces the previous Tenax IPP branding. Start with
[`brand-guide.md`](brand-guide.md), then open [`reference/index.html`](reference/index.html)
in a browser.

## Layout

```
brand-guide.md         The web brand standard — read this first
ASSET-REQUESTS.md      Gaps in the agency delivery, written to send back to them

source/                Agency delivery, verbatim. Never edited. The brand authority.
  Tenax Solutions _Lite Visual Identity.pdf
  Logo Package/        Primary · Secondary · Submark (Icon/ shipped empty)

assets/                What apps actually consume — all generated from source/
  logos/               {primary,secondary,submark,icon} × {color,inverse,black,white}.svg
  raster/              Web-sized PNG exports
  favicon/             Complete favicon set + webmanifest
  fonts/               Self-hosted Urbanist + Sora (variable woff2) + OFL licences
  tokens/
    tenax.css          CSS custom properties — the file apps copy
    tenax.tokens.json  Same values for non-CSS consumers (generated from the CSS)

reference/index.html   Live reference page — palette, type, logos, components

archive/ipp-2025/      Previous identity, deprecated but still in production

applications/
  siem-whitelabel/     Wazuh dashboard whitelabel tool (script + vendored logos + docs)

tools/                 Regeneration and verification — PIL + stdlib only
```

## Adopting the brand in a new app

1. Copy `assets/tokens/tenax.css` and `assets/fonts/` into the app.
2. Link both, and add `class="tenax"` to `<body>` for the base layer.
3. Copy `assets/favicon/` to the web root and link `favicon.svg` + `favicon.ico`.
4. Pick one logo from `assets/logos/` — `*-inverse.svg` on dark, `*-color.svg` on light.
5. Build with `var(--tenax-*)`. If you add a colour, add it to the contract in
   `tools/check-contrast.py` and run it.

Apps **vendor their own copies**; they don't depend on this repo at runtime. Treat it as
the upstream you copy *from*.

## Tools

| Command | Does |
|---------|------|
| `python3 tools/build-assets.py` | Rebuild `assets/{logos,raster,favicon}` from `source/` |
| `python3 tools/build-assets.py --verify` | Confirm committed assets match a fresh build |
| `python3 tools/fetch-fonts.py` | Re-vendor Urbanist + Sora from Google Fonts |
| `python3 tools/build-tokens.py` | Regenerate `tenax.tokens.json` from `tenax.css` |
| `python3 tools/build-tokens.py --check` | Fail if the JSON is stale |
| `python3 tools/check-contrast.py` | Assert the documented contrast contract holds |
| `python3 tools/sync-app-assets.py` | Refresh each application's vendored asset copies |
| `python3 tools/sync-app-assets.py --check` | Fail if a vendored copy is stale |

Everything under `assets/` is generated. Change `source/` or `tenax.css` and re-run —
don't hand-edit the outputs.

Two assets in `assets/logos/` are **reconstructions**, because the agency delivery is
missing them: the icon (its folder shipped empty) and the Primary vector (PNG only). Both
are derived from the delivered artwork and verified against it; see `ASSET-REQUESTS.md`.

## The previous identity

`archive/ipp-2025/` holds the Tenax IPP assets and the guide that described them. It is
deprecated, but **still live** on tenaxsolutions.com and on any app that hasn't migrated,
so it's kept for reference rather than deleted.
