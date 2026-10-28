import os
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch
from smart_run import runner, cli, dialog

class SmartRunTests(unittest.TestCase):
    def test_terminal_preserves_arguments(self):
        for terminal in ('gnome-terminal', 'konsole', 'xfce4-terminal', 'xterm'):
            with self.subTest(terminal=terminal), patch.object(runner, '_find_terminal', return_value=terminal), patch.object(runner.subprocess, 'Popen') as launch:
                runner._launch_in_terminal(['bash', '/tmp/a b;$(touch unwanted).sh'])
                self.assertEqual(launch.call_args.args[0][-2:], ['bash', '/tmp/a b;$(touch unwanted).sh'])
    def test_relative_path_is_absolute(self):
        with patch.dict(runner.DISPATCH, {'python': lambda path: path}):
            self.assertEqual(runner.dispatch('a b.py', 'python'), os.path.abspath('a b.py'))
    def test_msi_uses_installer(self):
        with patch.object(runner.shutil, 'which', return_value='/usr/bin/wine'), patch.object(runner, '_launch_in_terminal') as launch:
            runner.run_exe('/tmp/setup.msi')
            self.assertEqual(launch.call_args.args[0], ['wine', 'msiexec', '/i', '/tmp/setup.msi'])
    def test_zip_rejects_traversal(self):
        with tempfile.TemporaryDirectory() as tmp:
            archive = Path(tmp)/'bad.zip'
            with zipfile.ZipFile(archive, 'w') as z:
                z.writestr('../escape', 'bad')
            with self.assertRaises(RuntimeError):
                runner._extract_archive(str(archive), 'archive_zip')
            self.assertFalse((Path(tmp)/'escape').exists())
    def test_unique_extraction_directories(self):
        with tempfile.TemporaryDirectory() as tmp:
            archive = Path(tmp)/'ok.zip'
            with zipfile.ZipFile(archive, 'w') as z:
                z.writestr('hello.txt', 'hello')
            first = runner._extract_archive(str(archive), 'archive_zip')
            second = runner._extract_archive(str(archive), 'archive_zip')
            self.assertNotEqual(first, second)
    def test_missing_file_reports_failure(self):
        with patch.object(dialog, 'notify') as notify:
            self.assertEqual(cli.main(['/nonexistent/smart-run-test']), 1)
            notify.assert_called_once()
    def test_cancel_does_not_launch(self):
        with tempfile.NamedTemporaryFile(suffix='.py') as f, patch.object(dialog, 'confirm', return_value=False), patch.object(runner, 'dispatch') as dispatch:
            self.assertEqual(cli.main([f.name]), 0)
            dispatch.assert_not_called()
    def test_no_terminal_reports_problem(self):
        with patch.object(runner, '_find_terminal', return_value=None):
            with self.assertRaises(RuntimeError):
                runner._launch_in_terminal(['bash', 'test.sh'])

if __name__ == '__main__':
    unittest.main()
