"""
Given a detected file type, actually does the thing: makes it executable,
picks the right interpreter/runtime, and launches it - in a terminal window
when the program is likely to need one (installers, CLI scripts).
"""
import os
import shutil
import subprocess
import tarfile
import zipfile

from . import dialog

TERMINALS = ["gnome-terminal", "konsole", "xfce4-terminal", "xterm"]


def _find_terminal():
    for t in TERMINALS:
        if shutil.which(t):
            return t
    return None


def _launch_in_terminal(cmd_list, cwd=None):
    term = _find_terminal()
    if term == "gnome-terminal":
        subprocess.Popen([term, "--", *cmd_list], cwd=cwd)
    elif term:
        subprocess.Popen([term, "-e", " ".join(cmd_list)], cwd=cwd)
    else:
        subprocess.Popen(cmd_list, cwd=cwd)


def _make_executable(path):
    os.chmod(path, os.stat(path).st_mode | 0o111)


def run_appimage(path):
    _make_executable(path)
    subprocess.Popen([path])


def run_run_script(path):
    _make_executable(path)
    _launch_in_terminal([path])


def run_shell_script(path):
    _make_executable(path)
    _launch_in_terminal(["bash", path])


def run_jar(path):
    if not shutil.which("java"):
        raise RuntimeError("java isn't installed. Try: sudo apt install default-jre")
    subprocess.Popen(["java", "-jar", path])


def run_exe(path):
    if not shutil.which("wine"):
        raise RuntimeError("wine isn't installed. Try: sudo apt install wine")
    subprocess.Popen(["wine", path])


def run_deb(path):
    if shutil.which("gdebi-gtk"):
        subprocess.Popen(["gdebi-gtk", path])
    elif shutil.which("gdebi"):
        _launch_in_terminal(["sudo", "gdebi", path])
    elif shutil.which("apt"):
        _launch_in_terminal(["sudo", "apt", "install", "-y", path])
    else:
        raise RuntimeError("no installer found for .deb (need gdebi or apt)")


def run_rpm(path):
    if shutil.which("pkexec"):
        subprocess.Popen(["pkexec", "rpm", "-i", path])
    else:
        raise RuntimeError("no privilege helper found to install .rpm")


def run_python(path):
    _launch_in_terminal(["python3", path])


def _extract_archive(path, kind):
    base = os.path.splitext(os.path.basename(path))[0]
    if base.endswith(".tar"):
        base = base[:-4]
    dest = os.path.join(os.path.dirname(path), base + "_extracted")
    os.makedirs(dest, exist_ok=True)

    if kind == "archive_zip":
        with zipfile.ZipFile(path) as z:
            z.extractall(dest)
    elif kind == "archive_tar":
        with tarfile.open(path) as t:
            t.extractall(dest)
    elif kind == "archive_7z":
        if not shutil.which("7z"):
            raise RuntimeError("7z isn't installed. Try: sudo apt install p7zip-full")
        subprocess.run(["7z", "x", f"-o{dest}", path], check=True)
    return dest


def run_archive(path, kind):
    dest = _extract_archive(path, kind)

    candidates = []
    for root, _, files in os.walk(dest):
        for f in files:
            lower = f.lower()
            if lower in ("install.sh", "setup.sh", "run.sh") or lower.endswith(".appimage"):
                candidates.append(os.path.join(root, f))

    if candidates:
        target = candidates[0]
        if dialog.confirm(f"Found {os.path.basename(target)} inside the archive.", "Run it?"):
            inner_kind = "appimage" if target.lower().endswith(".appimage") else "shell_script"
            dispatch(target, inner_kind)
            return

    subprocess.Popen(["xdg-open", dest])


def run_unknown(path):
    subprocess.Popen(["xdg-open", path])


DISPATCH = {
    "appimage": run_appimage,
    "run_script": run_run_script,
    "shell_script": run_shell_script,
    "jar": run_jar,
    "exe": run_exe,
    "deb": run_deb,
    "rpm": run_rpm,
    "python": run_python,
    "unknown": run_unknown,
}


def dispatch(path, kind):
    if kind in ("archive_zip", "archive_tar", "archive_7z"):
        return run_archive(path, kind)
    fn = DISPATCH.get(kind, run_unknown)
    return fn(path)
