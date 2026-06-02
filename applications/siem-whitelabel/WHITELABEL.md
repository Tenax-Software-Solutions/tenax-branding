# Tenax SecureOps - Wazuh Dashboard Whitelabel Guide

## Overview

The Wazuh Dashboard ships with default Wazuh/OpenSearch branding. We replace these
with Tenax SecureOps logos. **Dashboard upgrades overwrite the logo files**, so the
replacement script must be re-run after every upgrade.

## Quick Reference

```bash
# Apply branding (run as root)
sudo bash /root/siem-whitelabel/apply-whitelabel.sh

# Restart dashboard to pick up changes
sudo systemctl restart wazuh-dashboard
```

---

## Source Files

Tenax logo files are stored in `/root/whitelabel/`. The table below maps each
marketing original to its working filename.

| Marketing Original              | Working Filename                     | Format |
|---------------------------------|--------------------------------------|--------|
| TENAX IPP MAIN LOGO_BLACK.SVG  | `tenax_ipp_main_logo_black.svg`      | SVG    |
| TENAX IPP MAIN LOGO_BLACK.PNG  | `tenax_ipp_main_logo_black.png`      | PNG    |
| TENAX IPP MAIN LOGO_WHITE.SVG  | `tenax_ipp_main_logo_white.svg`      | SVG    |
| TENAX_ICON_BLACK_TIGHT_80      | `tenax_icon_black_tight_80.svg`      | SVG    |
| TENAX_ICON_WHITE_TIGHT_80      | `tenax_icon_white_tight_80.svg`      | SVG    |
| TENAX_FAVICON.ICO              | `tenax_favicon.ico`                  | ICO    |

> **Note:** The PNG variant is required for PDF report generation. If marketing
> provides updated logos, ensure a PNG export is included.

---

## Logo Replacement Map

All targets are under:
`/usr/share/wazuh-dashboard/src/core/server/core_app/assets/logos/`

### tenax_ipp_main_logo_black.svg (light backgrounds)

| Target File                     | Usage                          |
|---------------------------------|--------------------------------|
| `spinner_on_light.svg`          | Loading spinner (light theme)  |
| `wazuh_dashboards.svg`          | Dashboard header logo          |
| `wazuh_dashboards_on_light.svg` | Dashboard logo (light theme)   |

### tenax_ipp_main_logo_white.svg (dark backgrounds)

| Target File                     | Usage                          |
|---------------------------------|--------------------------------|
| `spinner_on_dark.svg`           | Loading spinner (dark theme)   |
| `wazuh_dashboards_on_dark.svg`  | Dashboard logo (dark theme)    |

### tenax_icon_black_tight_80.svg (light backgrounds)

| Target File                        | Usage                              |
|------------------------------------|------------------------------------|
| `icon_light.svg`                   | Favicon/icon (light theme)         |
| `wazuh_mark_on_light.svg`          | Mark/watermark (light theme)       |
| `wazuh.svg`                        | Default Wazuh logo                 |
| `wazuh_center_mark.svg`            | Centered mark                      |
| `wazuh_center_mark_on_light.svg`   | Centered mark (light theme)        |
| `wazuh_mark.svg`                   | Default mark                       |
| `wazuh_on_light.svg`               | Wazuh logo (light theme)           |

### tenax_icon_white_tight_80.svg (dark backgrounds)

| Target File                        | Usage                              |
|------------------------------------|------------------------------------|
| `icon_dark.svg`                    | Favicon/icon (dark theme)          |
| `wazuh_mark_on_dark.svg`           | Mark/watermark (dark theme)        |
| `wazuh_center_mark_on_dark.svg`    | Centered mark (dark theme)         |
| `wazuh_on_dark.svg`                | Wazuh logo (dark theme)            |

### Default Branding Marks

Under `/usr/share/wazuh-dashboard/src/core/server/core_app/assets/default_branding/`:

| Target File                          | Replaced With                      |
|--------------------------------------|------------------------------------|
| `opensearch_mark_default_mode.svg`   | `tenax_icon_black_tight_80.svg`    |
| `opensearch_mark_dark_mode.svg`      | `tenax_icon_white_tight_80.svg`    |

### Favicons

Under `/usr/share/wazuh-dashboard/src/core/server/core_app/assets/favicons/`:

The `faviconUrl` config overrides the browser tab icon with the Tenax SVG icon. For
full favicon coverage (mobile bookmarks, Windows tiles, etc.), place PNG/ICO exports
in `/root/whitelabel/favicons/` matching these filenames:

| Target File                  | Size         |
|------------------------------|--------------|
| `favicon.ico`                | Multi-size   |
| `favicon-16x16.png`         | 16x16        |
| `favicon-32x32.png`         | 32x32        |
| `apple-touch-icon.png`      | 180x180      |
| `android-chrome-192x192.png`| 192x192      |
| `android-chrome-512x512.png`| 512x512      |
| `safari-pinned-tab.svg`     | SVG          |
| `mstile-70x70.png`          | 70x70        |
| `mstile-144x144.png`        | 144x144      |
| `mstile-150x150.png`        | 150x150      |
| `mstile-310x150.png`        | 310x150      |
| `mstile-310x310.png`        | 310x310      |

> **Note:** If the `favicons/` directory is not present in `/root/whitelabel/`,
> the script skips file replacement and relies on the `faviconUrl` config fallback.
> Request PNG/ICO exports from marketing for complete coverage.

---

## Configuration Files

These settings are **not overwritten** during upgrades but should be verified.

### /etc/wazuh-dashboard/opensearch_dashboards.yml

```yaml
opensearchDashboards:
  branding:
    applicationTitle: "Tenax SecureOps"
    faviconUrl: "/ui/favicons/favicon.ico"
opensearch_security.ui.basicauth.login.showbrandimage: true
opensearch_security.ui.basicauth.login.brandimage: "/ui/tenax_ipp_main_logo_black.svg"
```

### /usr/share/wazuh-dashboard/data/wazuh/config/wazuh.yml

```yaml
customization.logo.app: "tenax_ipp_main_logo_black.svg"
customization.logo.healthcheck: "tenax_ipp_main_logo_black.svg"
customization.logo.reports: "tenax_ipp_main_logo_black.png"
customization.reports.footer: "Tenax SecureOps"
customization.reports.header: "Tenax SecureOps"
```

---

## Post-Upgrade Checklist

1. Run the whitelabel script: `sudo bash /root/siem-whitelabel/apply-whitelabel.sh`
2. Verify the script output shows no errors or missing files
3. The script automatically restarts the dashboard service
4. Spot-check in a browser:
   - Login page shows Tenax logo
   - Dashboard header shows Tenax logo
   - Toggle light/dark theme and verify both variants
   - Generate a test report and verify logo + header/footer text
5. Check that a backup was created under `/root/siem-whitelabel/backups/`

---

## Backups

Each script run creates a timestamped backup of the original logos:

```
/root/siem-whitelabel/backups/
  20260215_143000/
  20260210_091500/
  ...
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

---

## File Locations Summary

| Path                                        | Purpose                    |
|---------------------------------------------|----------------------------|
| `/root/whitelabel/`                         | Tenax source logos         |
| `/root/siem-whitelabel/apply-whitelabel.sh` | Whitelabel script          |
| `/root/siem-whitelabel/backups/`            | Pre-replacement backups    |
| `/root/siem-whitelabel/WHITELABEL.md`       | This document              |
