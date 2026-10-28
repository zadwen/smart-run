# Smart Run

Right-click a downloaded file in Nautilus, pick **Smart Run**, and it figures
out what the file actually is and launches it correctly — no more manually
`chmod +x`-ing `.run` files, remembering `java -jar`, or digging Wine out for
a `.exe`.

## Beginner quick start

1. Open **Smart Run** from your application menu and choose your downloaded file, or right-click it in Files and select **Smart Run**.
2. Review the filename, location, and action shown in the confirmation.
3. Continue if you trust the download. Terminal programs keep their output visible; press Enter when finished.

If Wine or Java is missing, Smart Run explains what is needed. It does not install these automatically. Archives extract into a fresh folder; if several installers are found, the folder opens so you can choose. Running a program does not guarantee it is compatible with Linux.

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

Requires Python 3.12 or newer. This installs the CLI, application menu entry, and Nautilus extension in your user account without sudo or pip. The graphical interface needs GTK 3 Python bindings; the right-click menu needs nautilus-python. Close and reopen Files if its menu needs refreshing.

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
