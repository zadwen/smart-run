#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "$0")"
python3 - <<'PY'
import pathlib
import shutil
import site
import sys
if sys.version_info < (3, 12):
    raise SystemExit('Smart Run needs Python 3.12 or newer for safe archive extraction.')
home = pathlib.Path.home()
package = pathlib.Path(site.getusersitepackages()) / 'smart_run'
package.mkdir(parents=True, exist_ok=True)
for source in pathlib.Path('smart_run').glob('*.py'):
    shutil.copy2(source, package / source.name)
launcher = home / '.local/bin/smart-run'
launcher.parent.mkdir(parents=True, exist_ok=True)
launcher.write_text('#!/usr/bin/env python3\nfrom smart_run.cli import main\nraise SystemExit(main())\n')
launcher.chmod(0o755)
extensions = home / '.local/share/nautilus-python/extensions'
extensions.mkdir(parents=True, exist_ok=True)
shutil.copy2('nautilus-extension/nautilus_smart_run.py', extensions)
apps = home / '.local/share/applications'
apps.mkdir(parents=True, exist_ok=True)
escaped = str(launcher).replace('\\', '\\\\').replace('"', '\\"').replace('`', '\\`').replace('$', '\\$').replace('%', '%%')
(apps / 'smart-run.desktop').write_text('[Desktop Entry]\nType=Application\nName=Smart Run\nComment=Choose and run a downloaded program or installer\nExec="' + escaped + '" %f\nIcon=system-run\nTerminal=false\nCategories=Utility;\nStartupNotify=false\n')
print('Smart Run updated. Open Smart Run in the application menu, or right-click a downloaded file.')
print('If the right-click menu has not refreshed, close and reopen Files.')
PY
