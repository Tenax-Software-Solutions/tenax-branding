# Tenax SecureOps - Wazuh Dashboard Whitelabel

Part of the [`tenax-branding`](../../README.md) repo (`applications/siem-whitelabel/`).

Replaces default Wazuh/OpenSearch branding in the Wazuh Dashboard with Tenax
SecureOps logos, icons, and configuration. Must be re-run after every Wazuh
Dashboard upgrade since upgrades overwrite the modified files.

> The dashboard server does **not** pull this repo — its files are **copied over
> manually**.

Branding is the 2026 Tenax Solutions identity; see [`brand-guide.md`](../../brand-guide.md).
The logos in `logos/` are **generated** from the repo's `assets/` by
`tools/sync-app-assets.py` — regenerate rather than editing them in place.

## What the Script Does

1. **Replaces 16 logo SVGs** across light/dark theme variants (login screen,
   header, spinners, marks, watermarks)
2. **Replaces 2 OpenSearch branding marks** (default and dark mode)
3. **Replaces the favicon** and the full 12-file icon set
4. **Hides the Help menu** button from the dashboard header (CSS patch on
   compiled bundles)
5. **Removes the About page** from the Dashboard Management sidebar
6. **Sets configuration values** in `opensearch_dashboards.yml` and `wazuh.yml`:
   - Browser title: "Tenax SecureOps"
   - Login page brand image
   - App/healthcheck/report logos
   - Report header and footer text
7. **Restarts the dashboard service** to apply all changes

All operations are idempotent — safe to run multiple times. A timestamped backup
of the original files is created on every run.

## Prerequisites

- Wazuh Dashboard installed at `/usr/share/wazuh-dashboard/`
- Root or sudo access
- The logo source files in `logos/` (they ship with this folder — no separate copy needed)

## Setup (SIEM / dashboard server)

The server is provisioned by **manual copy** — it does not clone or pull. Copy
this folder (`applications/siem-whitelabel/`, including its `logos/`) anywhere on
the server and run the script. It is **self-contained**: it sources logos from
its own `logos/` directory and writes backups to `./backups/`, so there's no
separate staging step.

```bash
# e.g. copied to /root/siem-whitelabel/ on the dashboard server:
sudo bash /root/siem-whitelabel/apply-whitelabel.sh
```

To source logos from a different directory, set `LOGO_SOURCE_DIR`:

```bash
sudo LOGO_SOURCE_DIR=/some/other/dir bash /root/siem-whitelabel/apply-whitelabel.sh
```

## Usage

```bash
sudo bash /root/siem-whitelabel/apply-whitelabel.sh
```

### Example Output

```
[INFO]  ============================================
[INFO]  Tenax SecureOps Whitelabel - Logo Replacement
[INFO]  ============================================
[INFO]
[INFO]  Backing up originals to /root/siem-whitelabel/backups/20260215_191042
[INFO]  Backup complete
[INFO]
[INFO]  Replacing logo files...
[INFO]  Replaced 3/3 files with tenax_logo_on_light.svg
[INFO]  Replaced 2/2 files with tenax_logo_on_dark.svg
[INFO]  Replaced 7/7 files with tenax_icon_on_light.svg
[INFO]  Replaced 4/4 files with tenax_icon_on_dark.svg
[INFO]
[INFO]  Replacing default branding marks...
[INFO]    Replaced opensearch_mark_default_mode.svg
[INFO]    Replaced opensearch_mark_dark_mode.svg
[INFO]
[INFO]  Replacing favicons...
[INFO]    Replaced favicon.ico with tenax_favicon.ico
[INFO]    Replaced 12/12 favicon files from favicons/
[INFO]
[INFO]  Patching UI bundles...
[INFO]    [OK] core.entry.js
[INFO]    [OK] securityDashboards.plugin.js
[INFO]    [OK] wazuh.plugin.js
[INFO]
[INFO]  Checking configuration files...
[INFO]    [OK] opensearchDashboards branding block already present
[INFO]    [OK] opensearch_security.ui.basicauth.login.showbrandimage already correct
[INFO]    [OK] opensearch_security.ui.basicauth.login.brandimage already correct
[INFO]    [OK] customization.logo.app already correct
[INFO]    [OK] customization.logo.healthcheck already correct
[INFO]    [OK] customization.logo.reports already correct
[INFO]    [OK] customization.reports.footer already correct
[INFO]    [OK] customization.reports.header already correct
[INFO]
[INFO]  Restarting wazuh-dashboard service...
[INFO]  Service restarted successfully
[INFO]
[INFO]  ============================================
[INFO]  Whitelabel complete.
[INFO]  ============================================
```

## Post-Upgrade Checklist

1. Run the script: `sudo bash /root/siem-whitelabel/apply-whitelabel.sh`
2. Verify the output shows no errors or missing files
3. Spot-check in a browser:
   - Login page shows Tenax logo
   - Browser tab shows "Tenax SecureOps" title and Tenax favicon
   - Dashboard header shows Tenax logo
   - Help menu button is hidden
   - About page is removed from Dashboard Management
   - Toggle light/dark theme and verify both variants
   - Generate a test report and verify logo + header/footer text

## Reverting to Defaults

Each script run creates a timestamped backup:

```bash
BACKUP="/root/siem-whitelabel/backups/<timestamp>"
ASSETS="/usr/share/wazuh-dashboard/src/core/server/core_app/assets"
sudo cp -a "$BACKUP/logos/." "$ASSETS/logos/"
sudo cp -a "$BACKUP/favicons/." "$ASSETS/favicons/"
sudo cp -a "$BACKUP/default_branding/." "$ASSETS/default_branding/"
sudo systemctl restart wazuh-dashboard
```

## Logo Source Files

Located in `logos/`, generated from the repo's `assets/` by
`tools/sync-app-assets.py`. Filenames describe the **background** a mark goes on,
not its ink colour.

| Brand asset                     | Repo filename              | Used for                |
|---------------------------------|----------------------------|-------------------------|
| `logos/primary-color.svg`       | `tenax_logo_on_light.svg`  | Light theme logos       |
| `logos/primary-inverse.svg`     | `tenax_logo_on_dark.svg`   | Dark theme logos        |
| `logos/icon-color.svg`          | `tenax_icon_on_light.svg`  | Light theme icons/marks |
| `logos/icon-inverse.svg`        | `tenax_icon_on_dark.svg`   | Dark theme icons/marks  |
| `raster/primary-color-960w.png` | `tenax_logo_on_light.png`  | PDF report logos        |
| `favicon/favicon.ico`           | `tenax_favicon.ico`        | Browser tab favicon     |
| `favicon/*`                     | `favicons/`                | Full 12-file icon set   |

See [WHITELABEL.md](WHITELABEL.md) for the complete file-by-file replacement map
and configuration reference.
