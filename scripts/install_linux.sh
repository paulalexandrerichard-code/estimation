#!/usr/bin/env bash
set -euo pipefail
read -rp "Install directory [${HOME}/.local/plumbing-takeoff]: " TARGET
TARGET=${TARGET:-${HOME}/.local/plumbing-takeoff}
mkdir -p "$TARGET"
cp -r dist/plumbing-takeoff/* "$TARGET"/
mkdir -p "$HOME/.local/share/applications"
cat > "$HOME/.local/share/applications/plumbing-takeoff.desktop" <<DESKTOP
[Desktop Entry]
Type=Application
Name=Plumbing Takeoff
Exec=${TARGET}/plumbing-takeoff
Icon=${TARGET}/icon.png
Terminal=false
Categories=Office;
DESKTOP
echo "Installed to $TARGET"
