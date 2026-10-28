"""
Given a detected file type, actually does the thing: makes it executable,
picks the right interpreter/runtime, and launches it - in a terminal window
when the program is likely to need one (installers, CLI scripts).
"""
import os
import sys
import tempfile
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
    if not term:
        raise RuntimeError("A terminal is needed to show this program's output. Install GNOME Terminal or another supported terminal, then try again.")
    # Arguments are passed separately: filenames never become shell commands.
    wrapper = '"$@"; result=$?; printf "\\nProgram finished (exit code %s). Press Enter to close.\\n" "$result"; read -r answer; exit "$result"'
    command = ["bash", "-c", wrapper, "smart-run", *cmd_list]
    if term == "gnome-terminal":
        args = [term, "--", *command]
    elif term == "xfce4-terminal":
        args = [term, "--execute", *command]
    else:
        args = [term, "-e", *command]
    subprocess.Popen(args, cwd=cwd)


def _make_executable(path):
    os.chmod(path, os.stat(path).st_mode | 0o100)


def run_appimage(path):
    _make_executable(path)
    _launch_in_terminal([path], cwd=os.path.dirname(path))


def run_run_script(path):
    _make_executable(path)
    _launch_in_terminal([path], cwd=os.path.dirname(path))


def run_shell_script(path):
    _make_executable(path)
    _launch_in_terminal(["bash", path], cwd=os.path.dirname(path))


def run_jar(path):
    if not shutil.which("java"):
        raise RuntimeError("java isn't installed. Try: sudo apt install default-jre")
    _launch_in_terminal(["java", "-jar", path], cwd=os.path.dirname(path))


def run_exe(path):
    if not shutil.which("wine"):
        raise RuntimeError("wine isn't installed. Try: sudo apt install wine")
    _launch_in_terminal(["wine", "msiexec", "/i", path] if path.lower().endswith(".msi") else ["wine", path], cwd=os.path.dirname(path))


def run_deb(path):
    if shutil.which("gdebi-gtk"):
        subprocess.Popen(["gdebi-gtk", path])
    elif shutil.which("gdebi"):
        _launch_in_terminal(["sudo", "gdebi", path])
    elif shutil.which("apt"):
        _launch_in_terminal(["sudo", "apt", "install", path])
    else:
        raise RuntimeError("no installer found for .deb (need gdebi or apt)")


def run_rpm(path):
    if shutil.which("pkexec") and shutil.which("rpm"):
        subprocess.Popen(["pkexec", "rpm", "-i", path])
    else:
        raise RuntimeError("no privilege helper found to install .rpm")


def run_python(path):
    _launch_in_terminal([sys.executable, path], cwd=os.path.dirname(path))


def _extract_archive(path, kind):
    base = os.path.splitext(os.path.basename(path))[0]
    if base.endswith(".tar"):
        base = base[:-4]
    dest = tempfile.mkdtemp(prefix=base + "_extracted_", dir=os.path.dirname(path))

    if kind == "archive_zip":
        with zipfile.ZipFile(path) as z:
            for member in z.infolist():
                target = os.path.realpath(os.path.join(dest, member.filename))
                if os.path.commonpath([dest, target]) != dest or "\\" in member.filename:
                    raise RuntimeError("This archive contains an unsafe file path and cannot be extracted.")
            z.extractall(dest)
    elif kind == "archive_tar":
        with tarfile.open(path) as t:
            if not hasattr(tarfile, "data_filter"):
                raise RuntimeError("Safe archive extraction needs Python 3.12 or newer.")
            t.extractall(dest, filter="data")
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
        candidates.sort()
        target = dialog.choose_candidate(candidates)
        if target is None:
            subprocess.Popen(["xdg-open", dest])
            return
        if dialog.confirm(f"Run {os.path.basename(target)}?", f"Location: {target}\nOnly continue if you trust the source of this download."):
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
    path = os.path.abspath(os.path.expanduser(os.fspath(path)))
    if kind in ("archive_zip", "archive_tar", "archive_7z"):
        return run_archive(path, kind)
    fn = DISPATCH.get(kind, run_unknown)
    return fn(path)
