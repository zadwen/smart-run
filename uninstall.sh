#!/usr/bin/env bash
set -e

rm -f ~/.local/share/nautilus-python/extensions/nautilus_smart_run.py
pip3 uninstall -y smart-run || true
nautilus -q || true

echo "Uninstalled. Restart Nautilus/your file manager if the menu doesn't refresh."
