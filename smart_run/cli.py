#!/usr/bin/env python3
import sys

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


def main():
    if len(sys.argv) < 2:
        print("usage: smart-run <file>")
        sys.exit(1)

    path = sys.argv[1]

    try:
        kind = detector.detect(path)
    except FileNotFoundError:
        print(f"can't find {path}")
        sys.exit(1)

    label = LABELS.get(kind, kind)
    if not dialog.confirm(f"This looks like a {label}.", "Go ahead and run it?"):
        return

    try:
        runner.dispatch(path, kind)
    except RuntimeError as e:
        dialog.notify(str(e))
        print(e)


if __name__ == "__main__":
    main()
