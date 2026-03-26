from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "tools" / "export-public-homelab.py"
FIXTURES = REPO_ROOT / "tests" / "fixtures"
SOURCE = FIXTURES / "private-homelab"


class ExportPublicHomelabTests(unittest.TestCase):
    def test_export_rewrites_forbidden_literals(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            destination = Path(tempdir)
            result = subprocess.run(
                [
                    "python3",
                    str(SCRIPT),
                    "--source",
                    str(SOURCE),
                    "--dest",
                    str(destination),
                    "--rules",
                    str(FIXTURES / "rules-pass.json"),
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            output = (destination / "generated" / "install-minio.yml").read_text(encoding="utf-8")
            self.assertIn("edge-1", output)
            self.assertIn("shared-storage", output)
            self.assertNotIn("metatao.net", output)

    def test_dry_run_diff_returns_non_zero_when_changes_exist(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            destination = Path(tempdir)
            result = subprocess.run(
                [
                    "python3",
                    str(SCRIPT),
                    "--source",
                    str(SOURCE),
                    "--dest",
                    str(destination),
                    "--rules",
                    str(FIXTURES / "rules-pass.json"),
                    "--dry-run",
                    "--diff",
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 2)
            self.assertIn("generated/install-minio.yml", result.stdout)

    def test_forbidden_pattern_scan_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            destination = Path(tempdir)
            result = subprocess.run(
                [
                    "python3",
                    str(SCRIPT),
                    "--source",
                    str(SOURCE),
                    "--dest",
                    str(destination),
                    "--rules",
                    str(FIXTURES / "rules-fail.json"),
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("matched forbidden pattern", result.stdout)


if __name__ == "__main__":
    unittest.main()
