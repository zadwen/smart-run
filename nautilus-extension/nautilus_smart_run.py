"""
Adds a 'Smart Run' entry to the right-click menu in Nautilus for files that
look like they might be programs or installers. All the actual detection
and launching logic lives in the smart-run CLI - this just calls it.
"""
import subprocess

import gi
gi.require_version("Nautilus", "4.0")
from gi.repository import GObject, Nautilus

RELEVANT_EXTENSIONS = (
    ".exe", ".msi", ".jar", ".run", ".bin", ".sh", ".appimage",
    ".deb", ".rpm", ".py", ".zip", ".tar", ".tar.gz", ".tgz",
    ".tar.xz", ".tar.bz2", ".7z",
)


class SmartRunProvider(GObject.GObject, Nautilus.MenuProvider):

    def get_file_items(self, *args):
        # older nautilus-python passes (window, files), newer just (files)
        files = args[-1]
        if len(files) != 1:
            return []

        file_obj = files[0]
        if file_obj.get_uri_scheme() != "file":
            return []

        path = file_obj.get_location().get_path()
        if not path or not path.lower().endswith(RELEVANT_EXTENSIONS):
            return []

        item = Nautilus.MenuItem(
            name="SmartRun::run",
            label="Smart Run",
            tip="Detect this file's type and run it",
        )
        item.connect("activate", self._activate, path)
        return [item]

    def _activate(self, menu, path):
        subprocess.Popen(["smart-run", path])
