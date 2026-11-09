from __future__ import annotations

import os
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import bcrypt


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
BOOTSTRAP = REPOSITORY_ROOT / "scripts" / "bootstrap.py"
POSIX_TEMP_ROOT = "/tmp" if Path("/tmp").is_dir() else None


def parse_env(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if line and not line.startswith("#"):
            key, value = line.split("=", 1)
            values[key] = value
    return values


class BootstrapTests(unittest.TestCase):
    def run_bootstrap(self, root: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(BOOTSTRAP), "--root", str(root)],
            cwd=REPOSITORY_ROOT,
            check=False,
            capture_output=True,
            text=True,
        )

    def test_bootstrap_generates_strong_secrets_and_runtime_layout(self) -> None:
        with tempfile.TemporaryDirectory(dir=POSIX_TEMP_ROOT) as directory:
            root = Path(directory)

            result = self.run_bootstrap(root)

            self.assertEqual(result.returncode, 0, result.stderr)
            values = parse_env(root / ".env")
            expected_keys = {
                "WAZUH_INDEXER_PASSWORD",
                "WAZUH_API_PASSWORD",
                "WAZUH_DASHBOARD_PASSWORD",
                "WAZUH_REGISTRATION_PASSWORD",
                "CASE_MANAGEMENT_SECRET",
                "CASE_INDEX_PASSWORD",
            }
            self.assertEqual(set(values), expected_keys)
            for value in values.values():
                self.assertGreaterEqual(len(value), 32)
                self.assertNotIn(value, {"admin", "password", "SecretPassword"})

            expected_directories = {
                "runtime/certs",
                "runtime/config/wazuh-indexer",
                "runtime/telemetry/endpoint",
                "runtime/telemetry/suricata",
                "runtime/telemetry/zeek",
                "runtime/evidence",
            }
            for relative_path in expected_directories:
                self.assertTrue((root / relative_path).is_dir(), relative_path)

            registration_password = (
                root / "runtime/config/wazuh-agent/authd.pass"
            ).read_text(encoding="utf-8")
            self.assertEqual(
                registration_password, values["WAZUH_REGISTRATION_PASSWORD"]
            )
            self.assertIn(
                values["CASE_INDEX_PASSWORD"],
                (root / "runtime/config/thehive/index.conf").read_text(
                    encoding="utf-8"
                ),
            )
            self.assertIn(
                values["CASE_MANAGEMENT_SECRET"],
                (root / "runtime/config/thehive/secret.conf").read_text(
                    encoding="utf-8"
                ),
            )

            if os.name == "posix":
                mode = stat.S_IMODE((root / ".env").stat().st_mode)
                self.assertEqual(mode, 0o600)

    def test_bootstrap_does_not_overwrite_existing_secrets(self) -> None:
        with tempfile.TemporaryDirectory(dir=POSIX_TEMP_ROOT) as directory:
            root = Path(directory)

            first = self.run_bootstrap(root)
            original = (root / ".env").read_bytes()
            second = self.run_bootstrap(root)

            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertEqual((root / ".env").read_bytes(), original)
            self.assertIn("preserved", second.stdout.lower())

    def test_bootstrap_renders_bcrypt_credentials_for_indexer_users(self) -> None:
        with tempfile.TemporaryDirectory(dir=POSIX_TEMP_ROOT) as directory:
            root = Path(directory)

            result = self.run_bootstrap(root)

            self.assertEqual(result.returncode, 0, result.stderr)
            values = parse_env(root / ".env")
            internal_users = (
                root / "runtime/config/wazuh-indexer/internal_users.yml"
            ).read_text(encoding="utf-8")

            self.assertNotIn(values["WAZUH_INDEXER_PASSWORD"], internal_users)
            self.assertNotIn(values["WAZUH_DASHBOARD_PASSWORD"], internal_users)

            hashes = [
                line.split('"', 2)[1]
                for line in internal_users.splitlines()
                if line.strip().startswith("hash:")
            ]
            self.assertEqual(len(hashes), 2)
            self.assertTrue(
                bcrypt.checkpw(
                    values["WAZUH_INDEXER_PASSWORD"].encode(), hashes[0].encode()
                )
            )
            self.assertTrue(
                bcrypt.checkpw(
                    values["WAZUH_DASHBOARD_PASSWORD"].encode(), hashes[1].encode()
                )
            )


if __name__ == "__main__":
    unittest.main()
