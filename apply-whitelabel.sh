#!/usr/bin/env bash
# =============================================================================
# Tenax SecureOps - Wazuh Dashboard Whitelabel Script
# =============================================================================
# Replaces default Wazuh Dashboard logos with Tenax branding.
#
# WHEN TO RUN: After every Wazuh Dashboard upgrade. Dashboard upgrades
# overwrite the logo files in the assets directory, restoring Wazuh defaults.
#
# PREREQUISITES:
#   - Tenax logo source files must exist in LOGO_SOURCE_DIR (see below)
#   - Run as root or with sudo
#
# USAGE:
#   sudo bash /root/siem-whitelabel/apply-whitelabel.sh
# =============================================================================

set -euo pipefail

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------
LOGO_SOURCE_DIR="/root/whitelabel"
ASSETS_DIR="/usr/share/wazuh-dashboard/src/core/server/core_app/assets"
LOGO_TARGET_DIR="${ASSETS_DIR}/logos"
FAVICON_TARGET_DIR="${ASSETS_DIR}/favicons"
BRANDING_TARGET_DIR="${ASSETS_DIR}/default_branding"
CORE_ENTRY_JS="/usr/share/wazuh-dashboard/src/core/target/public/core.entry.js"
SECURITY_PLUGIN_JS="/usr/share/wazuh-dashboard/plugins/securityDashboards/target/public/securityDashboards.plugin.js"
WAZUH_PLUGIN_JS="/usr/share/wazuh-dashboard/plugins/wazuh/target/public/wazuh.plugin.js"
BACKUP_DIR="/root/siem-whitelabel/backups/$(date +%Y%m%d_%H%M%S)"
DASHBOARD_CONFIG="/etc/wazuh-dashboard/opensearch_dashboards.yml"
WAZUH_CONFIG="/usr/share/wazuh-dashboard/data/wazuh/config/wazuh.yml"

# -----------------------------------------------------------------------------
# Source Logo Mapping
# -----------------------------------------------------------------------------
# Marketing Original Name                  -> Whitelabel Filename
# TENAX IPP MAIN LOGO_BLACK.SVG            -> tenax_ipp_main_logo_black.svg
# TENAX IPP MAIN LOGO_WHITE.SVG            -> tenax_ipp_main_logo_white.svg
# TENAX_ICON_BLACK_TIGHT_80                -> tenax_icon_black_tight_80.svg
# TENAX_ICON_WHITE_TIGHT_80                -> tenax_icon_white_tight_80.svg
# TENAX IPP MAIN LOGO_BLACK.PNG            -> tenax_ipp_main_logo_black.png  (reports)
# TENAX_FAVICON.ICO                        -> tenax_favicon.ico              (browser tab)
# -----------------------------------------------------------------------------

# Tenax main logo (black/light variant) replaces these dashboard logos:
LOGO_BLACK_TARGETS=(
    "spinner_on_light.svg"
    "wazuh_dashboards.svg"
    "wazuh_dashboards_on_light.svg"
)

# Tenax main logo (white/dark variant) replaces these dashboard logos:
LOGO_WHITE_TARGETS=(
    "spinner_on_dark.svg"
    "wazuh_dashboards_on_dark.svg"
)

# Tenax icon (black variant) replaces these dashboard icons:
ICON_BLACK_TARGETS=(
    "icon_light.svg"
    "wazuh_mark_on_light.svg"
    "wazuh.svg"
    "wazuh_center_mark.svg"
    "wazuh_center_mark_on_light.svg"
    "wazuh_mark.svg"
    "wazuh_on_light.svg"
)

# Tenax icon (white variant) replaces these dashboard icons:
ICON_WHITE_TARGETS=(
    "icon_dark.svg"
    "wazuh_mark_on_dark.svg"
    "wazuh_center_mark_on_dark.svg"
    "wazuh_on_dark.svg"
)

# Tenax icon (black variant) replaces these favicon files (requires PNG/ICO exports):
# Source files expected in LOGO_SOURCE_DIR/favicons/
FAVICON_TARGETS=(
    "favicon.ico"
    "favicon-16x16.png"
    "favicon-32x32.png"
    "apple-touch-icon.png"
    "android-chrome-192x192.png"
    "android-chrome-512x512.png"
    "safari-pinned-tab.svg"
    "mstile-70x70.png"
    "mstile-144x144.png"
    "mstile-150x150.png"
    "mstile-310x150.png"
    "mstile-310x310.png"
)

# Tenax icon replaces default OpenSearch branding marks:
BRANDING_TARGETS_BLACK=(
    "opensearch_mark_default_mode.svg"
)
BRANDING_TARGETS_WHITE=(
    "opensearch_mark_dark_mode.svg"
)

# -----------------------------------------------------------------------------
# Functions
# -----------------------------------------------------------------------------

log()  { echo "[INFO]  $*"; }
warn() { echo "[WARN]  $*" >&2; }
err()  { echo "[ERROR] $*" >&2; }

preflight_check() {
    local missing=0

    local required_files=(
        "tenax_ipp_main_logo_black.svg"
        "tenax_ipp_main_logo_white.svg"
        "tenax_icon_black_tight_80.svg"
        "tenax_icon_white_tight_80.svg"
    )

    for f in "${required_files[@]}"; do
        if [[ ! -f "${LOGO_SOURCE_DIR}/${f}" ]]; then
            err "Missing source file: ${LOGO_SOURCE_DIR}/${f}"
            missing=1
        fi
    done

    if [[ ! -f "${LOGO_SOURCE_DIR}/tenax_ipp_main_logo_black.png" ]]; then
        warn "Missing PNG for reports: ${LOGO_SOURCE_DIR}/tenax_ipp_main_logo_black.png"
        warn "Report logos will not be updated."
    fi

    if [[ ! -d "${LOGO_TARGET_DIR}" ]]; then
        err "Target directory not found: ${LOGO_TARGET_DIR}"
        err "Is Wazuh Dashboard installed?"
        exit 1
    fi

    if [[ ${missing} -eq 1 ]]; then
        err "One or more required source files are missing. Aborting."
        exit 1
    fi
}

backup_originals() {
    log "Backing up originals to ${BACKUP_DIR}"
    mkdir -p "${BACKUP_DIR}/logos" "${BACKUP_DIR}/favicons" "${BACKUP_DIR}/default_branding"
    cp -a "${LOGO_TARGET_DIR}/." "${BACKUP_DIR}/logos/"
    cp -a "${FAVICON_TARGET_DIR}/." "${BACKUP_DIR}/favicons/"
    cp -a "${BRANDING_TARGET_DIR}/." "${BACKUP_DIR}/default_branding/"
    log "Backup complete"
}

replace_logos() {
    local source_file="$1"
    shift
    local targets=("$@")
    local source_path="${LOGO_SOURCE_DIR}/${source_file}"
    local count=0

    for target in "${targets[@]}"; do
        local target_path="${LOGO_TARGET_DIR}/${target}"
        if [[ -f "${target_path}" ]]; then
            cp "${source_path}" "${target_path}"
            count=$((count + 1))
        else
            warn "Target not found (skipped): ${target_path}"
        fi
    done

    log "Replaced ${count}/${#targets[@]} files with ${source_file}"
}

patch_bundle() {
    # Patch a compiled JS bundle: apply a sed replacement, remove compressed
    # copies (.br/.gz), and fix ownership so the dashboard can read it.
    # Usage: patch_bundle <file> <description> <sed_expression>
    local js_file="$1"
    local desc="$2"
    local sed_expr="$3"
    local name
    name=$(basename "${js_file}")

    if [[ ! -f "${js_file}" ]]; then
        warn "  Bundle not found: ${name}"
        return 1
    fi

    sed -i "${sed_expr}" "${js_file}"
    rm -f "${js_file}.br" "${js_file}.gz"
    chown wazuh-dashboard:wazuh-dashboard "${js_file}"
    log "  [PATCHED] ${name}: ${desc}"
}

hide_help_menu() {
    # Hide the help menu button via CSS injected into compiled bundles.
    local css_marker='.chrHeaderHelpMenu__version{text-transform:none}'
    local css_hide='[data-test-subj="helpMenuButton"]{display:none!important}'

    for js_file in "${CORE_ENTRY_JS}" "${SECURITY_PLUGIN_JS}"; do
        local name
        name=$(basename "${js_file}")

        if grep -q 'helpMenuButton.*display:none' "${js_file}" 2>/dev/null; then
            log "  [OK] ${name}"
            continue
        fi

        patch_bundle "${js_file}" "hide help menu" \
            "s|${css_marker}|${css_marker}${css_hide}|g"
    done
}

remove_about_page() {
    # Remove the About link from the Dashboard Management sidebar.
    local name
    name=$(basename "${WAZUH_PLUGIN_JS}")

    if ! grep -q 'appSettings,about,ITHygiene' "${WAZUH_PLUGIN_JS}" 2>/dev/null; then
        log "  [OK] ${name}"
        return
    fi

    patch_bundle "${WAZUH_PLUGIN_JS}" "remove About page" \
        's/appSettings,about,ITHygiene/appSettings,ITHygiene/g'
}

apply_config() {
    # opensearch_dashboards.yml - login brand image and application title
    # Ensure correct ownership after modifications (service runs as wazuh-dashboard)
    if [[ -f "${DASHBOARD_CONFIG}" ]]; then
        # Branding block (nested YAML) - applicationTitle and faviconUrl
        if grep -q "opensearchDashboards:" "${DASHBOARD_CONFIG}" 2>/dev/null; then
            log "  [OK] opensearchDashboards branding block already present"
            # Verify applicationTitle has the correct value
            if grep -q 'applicationTitle:' "${DASHBOARD_CONFIG}" 2>/dev/null; then
                if ! grep -q 'applicationTitle: "Tenax SecureOps"' "${DASHBOARD_CONFIG}" 2>/dev/null; then
                    sed -i 's/applicationTitle:.*/applicationTitle: "Tenax SecureOps"/' "${DASHBOARD_CONFIG}"
                    log "  [FIX] applicationTitle corrected to \"Tenax SecureOps\""
                else
                    log "  [OK] applicationTitle is correct"
                fi
            else
                sed -i '/branding:/a\    applicationTitle: "Tenax SecureOps"' "${DASHBOARD_CONFIG}"
                log "  [ADD] opensearchDashboards.branding.applicationTitle"
            fi
            # Add faviconUrl under existing branding block if missing
            if ! grep -q "faviconUrl:" "${DASHBOARD_CONFIG}" 2>/dev/null; then
                sed -i '/applicationTitle:/a\    faviconUrl: "/ui/favicons/favicon.ico"' "${DASHBOARD_CONFIG}"
                log "  [ADD] opensearchDashboards.branding.faviconUrl"
            fi
        else
            log "  [ADD] opensearchDashboards branding block"
            cat >> "${DASHBOARD_CONFIG}" <<'YAML'
opensearchDashboards:
  branding:
    applicationTitle: "Tenax SecureOps"
    faviconUrl: "/ui/favicons/favicon.ico"
YAML
        fi

        local dashboard_pairs=(
            'opensearch_security.ui.basicauth.login.showbrandimage|true'
            'opensearch_security.ui.basicauth.login.brandimage|"/ui/tenax_ipp_main_logo_black.svg"'
        )

        for pair in "${dashboard_pairs[@]}"; do
            local key="${pair%%|*}"
            local value="${pair#*|}"
            if grep -q "^${key}:" "${DASHBOARD_CONFIG}" 2>/dev/null; then
                if grep -q "^${key}: ${value}$" "${DASHBOARD_CONFIG}" 2>/dev/null; then
                    log "  [OK] ${key} already correct"
                else
                    sed -i "s|^${key}:.*|${key}: ${value}|" "${DASHBOARD_CONFIG}"
                    log "  [FIX] ${key} corrected to ${value}"
                fi
            else
                log "  [ADD] ${key}: ${value}"
                echo "${key}: ${value}" >> "${DASHBOARD_CONFIG}"
            fi
        done

        chown wazuh-dashboard:wazuh-dashboard "${DASHBOARD_CONFIG}"
    else
        warn "Dashboard config not found: ${DASHBOARD_CONFIG}"
    fi

    # wazuh.yml - custom logos and report headers
    # Use an indexed array to preserve order (associative arrays iterate randomly)
    if [[ -f "${WAZUH_CONFIG}" ]]; then
        log "Verifying Wazuh config customizations in ${WAZUH_CONFIG}"

        local config_pairs=(
            "customization.logo.app|tenax_ipp_main_logo_black.svg"
            "customization.logo.healthcheck|tenax_ipp_main_logo_black.svg"
            "customization.logo.reports|tenax_ipp_main_logo_black.png"
            "customization.reports.footer|Tenax SecureOps"
            "customization.reports.header|Tenax SecureOps"
        )

        for pair in "${config_pairs[@]}"; do
            local key="${pair%%|*}"
            local value="${pair#*|}"
            if grep -q "^${key}:" "${WAZUH_CONFIG}" 2>/dev/null; then
                if grep -q "^${key}: \"${value}\"" "${WAZUH_CONFIG}" 2>/dev/null; then
                    log "  [OK] ${key} already correct"
                else
                    sed -i "s|^${key}:.*|${key}: \"${value}\"|" "${WAZUH_CONFIG}"
                    log "  [FIX] ${key} corrected to \"${value}\""
                fi
            else
                log "  [ADD] ${key}: \"${value}\""
                echo "${key}: \"${value}\"" >> "${WAZUH_CONFIG}"
            fi
        done
    else
        warn "Wazuh config not found: ${WAZUH_CONFIG}"
    fi
}

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

log "============================================"
log "Tenax SecureOps Whitelabel - Logo Replacement"
log "============================================"
log ""

preflight_check

backup_originals

log ""
log "Replacing logo files..."

replace_logos "tenax_ipp_main_logo_black.svg" "${LOGO_BLACK_TARGETS[@]}"
replace_logos "tenax_ipp_main_logo_white.svg" "${LOGO_WHITE_TARGETS[@]}"
replace_logos "tenax_icon_black_tight_80.svg" "${ICON_BLACK_TARGETS[@]}"
replace_logos "tenax_icon_white_tight_80.svg" "${ICON_WHITE_TARGETS[@]}"

log ""
log "Replacing default branding marks..."

for target in "${BRANDING_TARGETS_BLACK[@]}"; do
    target_path="${BRANDING_TARGET_DIR}/${target}"
    if [[ -f "${target_path}" ]]; then
        cp "${LOGO_SOURCE_DIR}/tenax_icon_black_tight_80.svg" "${target_path}"
        log "  Replaced ${target}"
    else
        warn "  Target not found (skipped): ${target_path}"
    fi
done

for target in "${BRANDING_TARGETS_WHITE[@]}"; do
    target_path="${BRANDING_TARGET_DIR}/${target}"
    if [[ -f "${target_path}" ]]; then
        cp "${LOGO_SOURCE_DIR}/tenax_icon_white_tight_80.svg" "${target_path}"
        log "  Replaced ${target}"
    else
        warn "  Target not found (skipped): ${target_path}"
    fi
done

log ""
log "Replacing favicons..."

# Replace favicon.ico with tenax_favicon.ico
if [[ -f "${LOGO_SOURCE_DIR}/tenax_favicon.ico" ]]; then
    cp "${LOGO_SOURCE_DIR}/tenax_favicon.ico" "${FAVICON_TARGET_DIR}/favicon.ico"
    log "  Replaced favicon.ico with tenax_favicon.ico"
else
    warn "  tenax_favicon.ico not found in ${LOGO_SOURCE_DIR}"
fi

# Replace remaining favicon PNG/SVG files if marketing provides them
if [[ -d "${LOGO_SOURCE_DIR}/favicons" ]]; then
    local_count=0
    for target in "${FAVICON_TARGETS[@]}"; do
        if [[ -f "${LOGO_SOURCE_DIR}/favicons/${target}" ]]; then
            cp "${LOGO_SOURCE_DIR}/favicons/${target}" "${FAVICON_TARGET_DIR}/${target}"
            local_count=$((local_count + 1))
        fi
    done
    log "  Replaced ${local_count} additional favicon files from favicons/"
else
    log "  No additional favicon exports found in ${LOGO_SOURCE_DIR}/favicons/ (optional)"
fi

log ""
log "Patching UI bundles..."

hide_help_menu
remove_about_page

log ""
log "Checking configuration files..."

apply_config

log ""
log "Restarting wazuh-dashboard service..."
systemctl restart wazuh-dashboard
log "Service restarted successfully"

log ""
log "============================================"
log "Whitelabel complete."
log "============================================"
