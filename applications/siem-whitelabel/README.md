# Tenax SecureOps - Wazuh Dashboard Whitelabel

Part of the [`tenax-branding`](../../README.md) repo (`applications/siem-whitelabel/`).

Replaces default Wazuh/OpenSearch branding in the Wazuh Dashboard with Tenax
SecureOps logos, icons, and configuration. Must be re-run after every Wazuh
Dashboard upgrade since upgrades overwrite the modified files.

> The dashboard server does **not** pull this repo — its files are **copied over
> manually**. The script itself is unchanged from prior versions; only the repo
> layout and docs moved.

## What the Script Does

1. **Replaces 16 logo SVGs** across light/dark theme variants (login screen,
   header, spinners, marks, watermarks)
2. **Replaces 2 OpenSearch branding marks** (default and dark mode)
3. **Replaces the favicon** with the Tenax icon
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
- Logo source files deployed to `/root/whitelabel/` (see [Setup](#setup))

## Setup (SIEM / dashboard server)

The server is provisioned by **manual copy** — it does not clone or pull. Place
this folder's contents at `/root/siem-whitelabel/` on the server (the script's
backup path expects that location), then stage the logos where the script reads
them:

```bash
# On the dashboard server, after copying this folder
# (applications/siem-whitelabel/) to /root/siem-whitelabel/:
mkdir -p /root/whitelabel
cp /root/siem-whitelabel/logos/* /root/whitelabel/
```

The script's internal paths (`LOGO_SOURCE_DIR=/root/whitelabel`, backups under
`/root/siem-whitelabel/backups/`) are unchanged — keep this folder at
`/root/siem-whitelabel/` so they resolve.

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
[INFO]  Replaced 3/3 files with tenax_ipp_main_logo_black.svg
[INFO]  Replaced 2/2 files with tenax_ipp_main_logo_white.svg
[INFO]  Replaced 7/7 files with tenax_icon_black_tight_80.svg
[INFO]  Replaced 4/4 files with tenax_icon_white_tight_80.svg
[INFO]
[INFO]  Replacing default branding marks...
[INFO]    Replaced opensearch_mark_default_mode.svg
[INFO]    Replaced opensearch_mark_dark_mode.svg
[INFO]
[INFO]  Replacing favicons...
[INFO]    Replaced favicon.ico with tenax_favicon.ico
[INFO]
[INFO]  Patching UI bundles...
[INFO]    [OK] core.entry.js
[INFO]    [OK] securityDashboards.plugin.js
[INFO]    [OK] wazuh.plugin.js
[INFO]
[INFO]  Checking configuration files...
[INFO]    [OK] opensearchDashboards branding block already present
[INFO]    [OK] opensearch_security.ui.basicauth.login.showbrandimage already present
[INFO]    [OK] opensearch_security.ui.basicauth.login.brandimage already present
[INFO]    [OK] customization.logo.app already present
[INFO]    [OK] customization.logo.healthcheck already present
[INFO]    [OK] customization.logo.reports already present
[INFO]    [OK] customization.reports.footer already present
[INFO]    [OK] customization.reports.header already present
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

Located in the `logos/` directory of this repo. These are renamed from the
marketing originals for filesystem compatibility.

| Marketing Original             | Repo Filename                        | Used For                     |
|--------------------------------|--------------------------------------|------------------------------|
| TENAX IPP MAIN LOGO_BLACK.SVG | `tenax_ipp_main_logo_black.svg`      | Light theme logos             |
| TENAX IPP MAIN LOGO_BLACK.PNG | `tenax_ipp_main_logo_black.png`      | PDF report logos              |
| TENAX IPP MAIN LOGO_WHITE.SVG | `tenax_ipp_main_logo_white.svg`      | Dark theme logos              |
| TENAX_ICON_BLACK_TIGHT_80     | `tenax_icon_black_tight_80.svg`      | Light theme icons/marks       |
| TENAX_ICON_WHITE_TIGHT_80     | `tenax_icon_white_tight_80.svg`      | Dark theme icons/marks        |
| TENAX_FAVICON.ICO             | `tenax_favicon.ico`                  | Browser tab favicon           |

See [WHITELABEL.md](WHITELABEL.md) for the complete file-by-file replacement map
and configuration reference.
