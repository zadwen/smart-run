"""
Figures out what kind of file we're dealing with.

Checks the extension first since that's fast and usually right. If there's
no useful extension (or it's something weird), falls back to asking the
`file` command to sniff the magic bytes.
"""
import os
import subprocess

EXT_MAP = {
    ".appimage": "appimage",
    ".run": "run_script",
    ".bin": "run_script",
    ".sh": "shell_script",
    ".jar": "jar",
    ".exe": "exe",
    ".msi": "exe",
    ".deb": "deb",
    ".rpm": "rpm",
    ".py": "python",
    ".zip": "archive_zip",
    ".tar": "archive_tar",
    ".7z": "archive_7z",
}

DOUBLE_EXT = (".tar.gz", ".tar.xz", ".tar.bz2", ".tgz")


def detect(path):
    if not os.path.isfile(path):
        raise FileNotFoundError(path)

    name = os.path.basename(path).lower()

    for ext in DOUBLE_EXT:
        if name.endswith(ext):
            return "archive_tar"

    ext = os.path.splitext(name)[1]
    if ext in EXT_MAP:
        return EXT_MAP[ext]

    return _detect_by_magic(path)


def _detect_by_magic(path):
    try:
        out = subprocess.check_output(["file", "-b", path], text=True).lower()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "unknown"

    if "elf" in out and "executable" in out:
        return "run_script"  # native linux binary, treat like a .run
    if "shell script" in out or ("bash" in out and "script" in out):
        return "shell_script"
    if "pe32" in out or "ms-dos" in out:
        return "exe"
    if "zip archive" in out or "java archive" in out and "zip" in out:
        return "archive_zip"
    if "java archive" in out:
        return "jar"
    if "gzip compressed" in out or "tar archive" in out or "xz compressed" in out:
        return "archive_tar"
    if "7-zip" in out:
        return "archive_7z"
    return "unknown"
