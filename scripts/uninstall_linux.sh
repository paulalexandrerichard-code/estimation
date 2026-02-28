#!/usr/bin/env bash
set -euo pipefail
read -rp "Install directory to remove [${HOME}/.local/plumbing-takeoff]: " TARGET
TARGET=${TARGET:-${HOME}/.local/plumbing-takeoff}
rm -rf "$TARGET"
rm -f "$HOME/.local/share/applications/plumbing-takeoff.desktop"
echo "Uninstalled"
