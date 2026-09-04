# Smart Run

Right-click a downloaded file in Nautilus, pick **Smart Run**, and it figures
out what the file actually is and launches it correctly — no more manually
`chmod +x`-ing `.run` files, remembering `java -jar`, or digging Wine out for
a `.exe`.

## Supported file types

| Type | What happens |
|---|---|
| `.AppImage` | made executable, launched directly |
| `.run`, `.bin`, unlabeled ELF binaries | made executable, launched in a terminal |
| `.sh` | run with `bash` in a terminal |
| `.jar` | run with `java -jar` |
| `.exe`, `.msi` | run with Wine |
| `.deb` | installed via `gdebi` (or `apt` as a fallback) |
| `.rpm` | installed via `rpm` |
| `.py` | run with `python3` in a terminal |
| `.zip`, `.tar.gz`, `.tar.xz`, `.tar.bz2`, `.7z` | extracted, then it looks inside for an `install.sh`/`setup.sh`/`.AppImage` and offers to run that |
| anything else | opened with `xdg-open` |

You always get a confirmation prompt before anything actually runs.

## Install

```bash
git clone https://github.com/zadwen/smart-run.git
cd smart-run
chmod +x install.sh
./install.sh
```

This installs the `smart-run` CLI and the Nautilus extension, and restarts
Nautilus so the new context menu item shows up.

For `.exe` support you'll also need Wine:

```bash
sudo apt install wine
```

## Usage

- **From Nautilus**: right-click a file → **Smart Run**.
- **From the terminal**: `smart-run path/to/file`

## Uninstall

```bash
./uninstall.sh
```

## Notes

- Built for GTK/Nautilus-based desktops (GNOME, Cinnamon, etc). It doesn't
  hook into other file managers (Dolphin, Thunar) — that'd need separate
  extensions for each.
- Archive handling looks for an obvious installer inside; if it doesn't find
  one it just opens the extracted folder so you can look yourself.

## License

MIT-Zadwen
