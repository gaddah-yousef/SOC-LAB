from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SIMULATE = REPOSITORY_ROOT / "scripts" / "simulate.py"
CATALOG = REPOSITORY_ROOT / "scenarios" / "catalog.yml"


class ScenarioContractTests(unittest.TestCase):
    def test_catalog_has_three_unique_attack_mapped_scenarios(self) -> None:
        catalog = yaml.safe_load(CATALOG.read_text(encoding="utf-8"))
        scenarios = catalog["scenarios"]

        self.assertGreaterEqual(len(scenarios), 3)
        self.assertEqual(len({item["id"] for item in scenarios}), len(scenarios))
        self.assertEqual(len({item["slug"] for item in scenarios}), len(scenarios))
        for scenario in scenarios:
            self.assertRegex(scenario["id"], r"^LAB-[A-Z]+-[0-9]{3}$")
            self.assertRegex(scenario["technique"], r"^T[0-9]{4}(\.[0-9]{3})?$")
            self.assertTrue(scenario["expected_rules"])
            self.assertTrue(scenario["safety_controls"])

    def test_each_catalog_scenario_has_a_safe_dry_run_plan(self) -> None:
        catalog = yaml.safe_load(CATALOG.read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory(dir="/tmp") as directory:
            root = Path(directory)
            for scenario in catalog["scenarios"]:
                result = subprocess.run(
                    [
                        sys.executable,
                        str(SIMULATE),
                        scenario["slug"],
                        "--dry-run",
                        "--root",
                        str(root),
                    ],
                    cwd=REPOSITORY_ROOT,
                    check=False,
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                plan = json.loads(result.stdout)
                self.assertEqual(plan["scenario"], scenario["slug"])
                self.assertEqual(plan["technique"], scenario["technique"])
                self.assertNotIn("shell", json.dumps(plan).lower())
                self.assertFalse((root / "runtime").exists())

    def test_unknown_scenario_is_rejected_without_side_effects(self) -> None:
        with tempfile.TemporaryDirectory(dir="/tmp") as directory:
            root = Path(directory)
            result = subprocess.run(
                [
                    sys.executable,
                    str(SIMULATE),
                    "arbitrary-target",
                    "--root",
                    str(root),
                ],
                cwd=REPOSITORY_ROOT,
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertFalse((root / "runtime").exists())


if __name__ == "__main__":
    unittest.main()
