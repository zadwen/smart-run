#!/usr/bin/env python3
import sys
import os
import argparse
import subprocess

from . import detector, dialog, runner

LABELS = {
    "appimage": "AppImage",
    "run_script": "Linux installer/binary (.run)",
    "shell_script": "shell script",
    "jar": "Java program (.jar)",
    "exe": "Windows program (.exe) - will run through Wine",
    "deb": "Debian package (.deb)",
    "rpm": "RPM package (.rpm)",
    "python": "Python script",
    "archive_zip": "zip archive",
    "archive_tar": "tar archive",
    "archive_7z": "7z archive",
    "unknown": "unrecognized file - will just try to open it normally",
}


def main(argv=None):
    parser = argparse.ArgumentParser(description="Choose a downloaded program, review what will happen, and launch it.")
    parser.add_argument("file", nargs="?", help="Program, installer, or archive to open")
    args = parser.parse_args(argv)
    path = args.file or dialog.choose_file()
    if not path:
        return 0
    path = os.path.abspath(os.path.expanduser(path))
    try:
        kind = detector.detect(path)
        label = LABELS.get(kind, kind)
        action = "Extract into a new folder" if kind.startswith("archive_") else "Install this package (administrator password may be needed)" if kind in ("deb", "rpm") else "Open with the default application" if kind == "unknown" else "Launch this program"
        detail = f"File: {os.path.basename(path)}\nLocation: {os.path.dirname(path)}\nType: {label}\n\n{action}.\nOnly continue if you trust the source of this file."
        if not dialog.confirm("Ready to continue?", detail):
            return 0
        runner.dispatch(path, kind)
        return 0
    except (OSError, RuntimeError, ValueError, subprocess.SubprocessError) as error:
        dialog.notify(f"Smart Run could not open this file.\n\n{error}\n\nCheck that the file still exists and that you have permission to read it.")
        return 1
    except Exception as error:
        # Archive parsers can raise format-specific exceptions.
        dialog.notify(f"Smart Run could not complete this action:\n{error}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
