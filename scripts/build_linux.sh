#!/usr/bin/env bash
set -euo pipefail
python -m PyInstaller --name plumbing-takeoff --noconfirm --windowed plumbing_takeoff/app.py
