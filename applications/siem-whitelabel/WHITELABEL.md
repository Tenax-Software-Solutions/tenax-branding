# Tenax SecureOps — Wazuh Dashboard Whitelabel Guide

## Overview

The Wazuh Dashboard ships with default Wazuh/OpenSearch branding. We replace it with
Tenax SecureOps branding. **Dashboard upgrades overwrite the logo files**, so the
replacement script must be re-run after every upgrade.

Branding is the 2026 Tenax Solutions identity — see `brand-guide.md` at the repo root.

## Quick Reference

```bash
# Apply branding (run as root, from wherever this directory lives)
sudo bash /root/siem-whitelabel/apply-whitelabel.sh

# The script restarts the dashboard itself; to do it manually:
sudo systemctl restart wazuh-dashboard
```

The script resolves its own directory, so it works from a repo checkout or a copy on the
server. Override `LOGO_SOURCE_DIR` to point at a different asset directory.

---

## Source Files

Logos live in `logos/`, next to the script, and ship with it — there is no separate copy
step.

**These files are generated.** They are produced from the repo's `assets/` by
`tools/sync-app-assets.py`. Don't edit them in place; change the brand assets and
re-run the sync, or they will be silently overwritten.

| Brand asset | Working filename | Purpose |
|-------------|------------------|---------|
| `logos/primary-color.svg` | `tenax_logo_on_light.svg` | full lockup, light backgrounds |
| `logos/primary-inverse.svg` | `tenax_logo_on_dark.svg` | full lockup, dark backgrounds |
| `logos/icon-color.svg` | `tenax_icon_on_light.svg` | mark only, light backgrounds |
| `logos/icon-inverse.svg` | `tenax_icon_on_dark.svg` | mark only, dark backgrounds |
| `raster/primary-color-960w.png` | `tenax_logo_on_light.png` | PDF report generation |
| `favicon/favicon.ico` | `tenax_favicon.ico` | browser tab |
| `favicon/*` | `favicons/` | full icon set (12 files) |

Filenames describe the **background** a mark goes on, not its ink colour — matching how
the dashboard names its own targets (`*_on_light` / `*_on_dark`).

> **Note:** the PNG is required for PDF report generation. Reports print on white, so it
> is the `color` (dark-mark) variant.

---

## Logo Replacement Map

All targets are under
`/usr/share/wazuh-dashboard/src/core/server/core_app/assets/logos/`.

### `tenax_logo_on_light.svg`

| Target File | Usage |
|-------------|-------|
| `spinner_on_light.svg` | Loading spinner (light theme) |
| `wazuh_dashboards.svg` | Dashboard header logo |
| `wazuh_dashboards_on_light.svg` | Dashboard logo (light theme) |

### `tenax_logo_on_dark.svg`

| Target File | Usage |
|-------------|-------|
| `spinner_on_dark.svg` | Loading spinner (dark theme) |
| `wazuh_dashboards_on_dark.svg` | Dashboard logo (dark theme) |

### `tenax_icon_on_light.svg`

| Target File | Usage |
|-------------|-------|
| `icon_light.svg` | Icon (light theme) |
| `wazuh_mark_on_light.svg` | Mark/watermark (light theme) |
| `wazuh.svg` | Default Wazuh logo |
| `wazuh_center_mark.svg` | Centered mark |
| `wazuh_center_mark_on_light.svg` | Centered mark (light theme) |
| `wazuh_mark.svg` | Default mark |
| `wazuh_on_light.svg` | Wazuh logo (light theme) |

### `tenax_icon_on_dark.svg`

| Target File | Usage |
|-------------|-------|
| `icon_dark.svg` | Icon (dark theme) |
| `wazuh_mark_on_dark.svg` | Mark/watermark (dark theme) |
| `wazuh_center_mark_on_dark.svg` | Centered mark (dark theme) |
| `wazuh_on_dark.svg` | Wazuh logo (dark theme) |

### Default Branding Marks

Under `.../assets/default_branding/`:

| Target File | Replaced With |
|-------------|---------------|
| `opensearch_mark_default_mode.svg` | `tenax_icon_on_light.svg` |
| `opensearch_mark_dark_mode.svg` | `tenax_icon_on_dark.svg` |

### Favicons

Under `.../assets/favicons/`. The 2026 identity ships a complete set, so all twelve
targets are now replaced with real files rather than relying on the `faviconUrl` config
fallback:

`favicon.ico` · `favicon-16x16.png` · `favicon-32x32.png` · `apple-touch-icon.png` ·
`android-chrome-192x192.png` · `android-chrome-512x512.png` · `safari-pinned-tab.svg` ·
`mstile-70x70.png` · `mstile-144x144.png` · `mstile-150x150.png` ·
`mstile-310x150.png` · `mstile-310x310.png`

If `logos/favicons/` is missing, the script warns and falls back to the config-only
behaviour — that means the vendored copy is stale, so run `tools/sync-app-assets.py`.

---

## Configuration Files

These settings are **not overwritten** during upgrades, but the script verifies them on
every run and corrects drift.

### `/etc/wazuh-dashboard/opensearch_dashboards.yml`

```yaml
opensearchDashboards:
  branding:
    applicationTitle: "Tenax SecureOps"
    faviconUrl: "/ui/favicons/favicon.ico"
opensearch_security.ui.basicauth.login.showbrandimage: true
opensearch_security.ui.basicauth.login.brandimage: "/ui/tenax_logo_on_light.svg"
```

### `/usr/share/wazuh-dashboard/data/wazuh/config/wazuh.yml`

```yaml
customization.logo.app: "tenax_logo_on_light.svg"
customization.logo.healthcheck: "tenax_logo_on_light.svg"
customization.logo.reports: "tenax_logo_on_light.png"
customization.reports.footer: "Tenax SecureOps"
customization.reports.header: "Tenax SecureOps"
```

---

## UI Patches

Beyond logos, the script patches two compiled bundles. Both are idempotent and re-check
on each run:

- **Hide the help menu** — CSS injected into `core.entry.js` and
  `securityDashboards.plugin.js`.
- **Remove the About page** — from the Dashboard Management sidebar in
  `wazuh.plugin.js`.

---

## Post-Upgrade Checklist

1. Run the script: `sudo bash /root/siem-whitelabel/apply-whitelabel.sh`
2. Verify the output shows no `[ERROR]` lines and `Replaced 12/12 favicon files`
3. The script restarts the dashboard service automatically
4. Spot-check in a browser:
   - Login page shows the Tenax lockup
   - Dashboard header shows the Tenax lockup
   - Toggle light/dark theme and verify both variants
   - Browser tab shows the Tenax favicon
   - Generate a test report and verify logo + header/footer text
5. Confirm a backup was created under `backups/`

Running the script twice is safe — the second run should report `[OK]` for every config
key and patch.

---

## Backups

Each run creates a timestamped backup of the originals, next to the script:

```
backups/
  20260821_143000/
  20260815_091500/
```

To revert to Wazuh defaults:

```bash
BACKUP="/root/siem-whitelabel/backups/<timestamp>"
ASSETS="/usr/share/wazuh-dashboard/src/core/server/core_app/assets"
sudo cp -a "$BACKUP/logos/." "$ASSETS/logos/"
sudo cp -a "$BACKUP/favicons/." "$ASSETS/favicons/"
sudo cp -a "$BACKUP/default_branding/." "$ASSETS/default_branding/"
sudo systemctl restart wazuh-dashboard
```

Note that reverting restores logos only. The config changes and bundle patches are not
backed up; undo those by editing the YAML and reinstalling the affected packages.

---

## File Locations Summary

| Path | Purpose |
|------|---------|
| `<script dir>/logos/` | Tenax source logos (generated — see above) |
| `<script dir>/logos/favicons/` | Full favicon set |
| `<script dir>/apply-whitelabel.sh` | Whitelabel script |
| `<script dir>/backups/` | Pre-replacement backups |
| `<script dir>/WHITELABEL.md` | This document |

Paths are resolved relative to the script, so a checkout at
`~/projects/tenax-branding/applications/siem-whitelabel` and a copy at
`/root/siem-whitelabel` both work.
