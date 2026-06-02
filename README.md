# tenax-branding

Single source of truth for Tenax brand assets and the tools that apply them.

(Formerly `siem-whitelabel` — renamed and broadened to cover all Tenax branding,
not just the SIEM dashboard.)

## Layout

```
brand-guide.md              Color palette + logo/favicon usage guidance
assets/
  icons/                    Master Tenax icon — @4x marketing originals (all tones)
  logos/                    Master Tenax + IPP main logo — @4x originals (all tones)
applications/
  siem-whitelabel/          Wazuh dashboard whitelabel tool (script + working logos + docs)
```

## What's here

- **`assets/`** — the canonical marketing originals. Everything else (and every
  consuming app) derives or copies from these. Don't edit in place; replace with
  new marketing exports.
- **`brand-guide.md`** — the palette (`#181818` bg, `#ef910a` gold, …) and the
  logo/favicon usage rules, as applied across Tenax web surfaces.
- **`applications/`** — concrete applications of the brand. Today: the SIEM
  (Wazuh) dashboard whitelabel. The on-call app / training course are separate
  repos that **vendor copies** of `assets/` rather than depend on this repo.

## Consuming the assets

Apps should copy what they need into their own repo and bake it into their build
(this is what the on-call app does with its favicon/logo). Treat this repo as the
upstream you copy *from*, not a runtime dependency.
