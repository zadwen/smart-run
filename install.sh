#!/usr/bin/env bash
set -e

echo "== Smart Run installer =="

if command -v apt >/dev/null; then
    echo "Installing system packages (needs sudo)..."
    sudo apt update
    sudo apt install -y python3-nautilus python3-gi gir1.2-nautilus-3.0 file
else
    echo "Non-apt system detected - install python3-nautilus / python-gobject manually."
fi

echo "Installing smart-run python package..."
pip3 install --user .

echo "Installing Nautilus extension..."
mkdir -p ~/.local/share/nautilus-python/extensions
cp nautilus-extension/nautilus_smart_run.py ~/.local/share/nautilus-python/extensions/

echo "Restarting Nautilus..."
nautilus -q || true

echo
echo "Done. Right-click an exe/jar/run/etc file and pick 'Smart Run'."
echo "For .exe support: sudo apt install wine"
echo
echo "If 'smart-run' isn't found on the command line, add ~/.local/bin to your PATH:"
echo '  echo '"'"'export PATH="$HOME/.local/bin:$PATH"'"'"' >> ~/.bashrc && source ~/.bashrc'
