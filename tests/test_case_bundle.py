from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
BUILD_CASE = REPOSITORY_ROOT / "scripts" / "build_case.py"


class CaseBundleTests(unittest.TestCase):
    def test_builds_thehive_ready_case_from_latest_scenario_evidence(self) -> None:
        with tempfile.TemporaryDirectory(dir="/tmp") as directory:
            root = Path(directory)
            evidence_directory = root / "runtime/evidence"
            evidence_directory.mkdir(parents=True)
            (evidence_directory / "LAB-ENDPOINT-001-20260101T000000Z.json").write_text(
                json.dumps(
                    {
                        "scenario_id": "LAB-ENDPOINT-001",
                        "scenario": "ssh-bruteforce",
                        "executed_at": "2026-01-01T00:00:00+00:00",
                        "technique": "T1110.001",
                        "expected_rules": [5710, 100100],
                        "generated_artifacts": [
                            "runtime/telemetry/endpoint/auth.log"
                        ],
                        "result": "simulation-generated",
                    }
                ),
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(BUILD_CASE),
                    "ssh-bruteforce",
                    "--root",
                    str(root),
                ],
                cwd=REPOSITORY_ROOT,
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            bundle_path = Path(result.stdout.strip())
            bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
            self.assertEqual(bundle["title"], "[LAB-ENDPOINT-001] Repeated SSH authentication failures")
            self.assertEqual(bundle["severity"], 2)
            self.assertIn("attack:T1110.001", bundle["tags"])
            self.assertEqual(bundle["sourceRef"], "LAB-ENDPOINT-001")
            self.assertGreaterEqual(len(bundle["tasks"]), 3)

    def test_rejects_missing_evidence(self) -> None:
        with tempfile.TemporaryDirectory(dir="/tmp") as directory:
            result = subprocess.run(
                [
                    sys.executable,
                    str(BUILD_CASE),
                    "web-recon",
                    "--root",
                    directory,
                ],
                cwd=REPOSITORY_ROOT,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("no evidence", result.stderr.lower())


if __name__ == "__main__":
    unittest.main()
