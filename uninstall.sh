#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PYTHON'
import pathlib, shutil, site
home = pathlib.Path.home()
shutil.rmtree(pathlib.Path(site.getusersitepackages()) / 'smart_run', ignore_errors=True)
for relative in ('.local/bin/smart-run', '.local/share/applications/smart-run.desktop', '.local/share/nautilus-python/extensions/nautilus_smart_run.py'):
    (home / relative).unlink(missing_ok=True)
print('Smart Run removed. Close and reopen Files to refresh its menu.')
PYTHON
