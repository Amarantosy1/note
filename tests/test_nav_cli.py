from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from zensical_nav import cli


class ZensicalDelegationTest(unittest.TestCase):
    def test_command_uses_current_python_interpreter(self):
        command = cli._zensical_command(
            "build",
            Path("expanded.yml"),
            ["--clean"],
        )

        self.assertEqual(
            command,
            [
                sys.executable,
                "-m",
                "zensical",
                "build",
                "-f",
                "expanded.yml",
                "--clean",
            ],
        )

    def test_build_delegates_with_current_python_interpreter(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            config = root / "mkdocs.yml"
            expanded = root / ".expanded.yml"
            config.write_text("site_name: Test", encoding="utf-8")
            completed = MagicMock(returncode=7)

            with patch.object(cli, "_temporary_config_path", return_value=expanded), patch.object(
                cli,
                "expand_config_file",
            ), patch.object(cli.subprocess, "run", return_value=completed) as run:
                result = cli._build(config, ["--strict"])

        self.assertEqual(result, 7)
        run.assert_called_once_with(
            [
                sys.executable,
                "-m",
                "zensical",
                "build",
                "-f",
                str(expanded),
                "--strict",
            ],
            check=False,
        )

    def test_serve_delegates_with_current_python_interpreter(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            config = root / "mkdocs.yml"
            expanded = root / ".expanded.yml"
            config.write_text("site_name: Test", encoding="utf-8")
            process = MagicMock()
            process.wait.return_value = 0
            process.poll.return_value = 0
            watcher = MagicMock()

            with patch.object(cli, "_temporary_config_path", return_value=expanded), patch.object(
                cli,
                "expand_config_file",
            ), patch.object(cli.threading, "Thread", return_value=watcher), patch.object(
                cli.subprocess,
                "Popen",
                return_value=process,
            ) as popen:
                result = cli._serve(config, ["--open"], 0.5)

        self.assertEqual(result, 0)
        popen.assert_called_once_with(
            [
                sys.executable,
                "-m",
                "zensical",
                "serve",
                "-f",
                str(expanded),
                "--open",
            ]
        )
        watcher.start.assert_called_once_with()
        watcher.join.assert_called_once_with(timeout=1.0)


if __name__ == "__main__":
    unittest.main()
