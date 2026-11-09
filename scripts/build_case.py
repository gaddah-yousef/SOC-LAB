#!/usr/bin/env python3
"""Build a reviewable TheHive case payload from allowlisted lab evidence."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
CATALOG = REPOSITORY_ROOT / "scenarios/catalog.yml"
SEVERITY_BY_SCENARIO = {
    "ssh-bruteforce": 2,
    "web-recon": 3,
    "persistence-artifact": 2,
}


def load_scenarios() -> dict[str, dict[str, Any]]:
    document = yaml.safe_load(CATALOG.read_text(encoding="utf-8"))
    return {item["slug"]: item for item in document["scenarios"]}


def parse_arguments(scenarios: dict[str, dict[str, Any]]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scenario", choices=sorted(scenarios))
    parser.add_argument("--root", type=Path, default=REPOSITORY_ROOT, help=argparse.SUPPRESS)
    return parser.parse_args()


def latest_evidence(root: Path, scenario_id: str) -> Path:
    evidence_directory = root / "runtime/evidence"
    matches = sorted(evidence_directory.glob(f"{scenario_id}-*.json"))
    if not matches:
        raise FileNotFoundError(f"no evidence found for {scenario_id}")
    return matches[-1]


def build_payload(metadata: dict[str, Any], evidence: dict[str, Any]) -> dict[str, Any]:
    artifacts = "\n".join(f"- `{item}`" for item in evidence["generated_artifacts"])
    expected_rules = ", ".join(str(item) for item in metadata["expected_rules"])
    return {
        "title": f"[{metadata['id']}] {metadata['name']}",
        "description": (
            f"Controlled Enterprise SOC Lab simulation.\n\n"
            f"ATT&CK technique: {metadata['technique']} ({metadata['tactic']})\n\n"
            f"Expected detection IDs: {expected_rules}\n\n"
            f"Generated evidence:\n{artifacts}"
        ),
        "type": "internal",
        "source": "enterprise-soc-lab",
        "sourceRef": metadata["id"],
        "severity": SEVERITY_BY_SCENARIO[metadata["slug"]],
        "tlp": 1,
        "pap": 1,
        "tags": [
            "simulation",
            "enterprise-soc-lab",
            f"attack:{metadata['technique']}",
            f"scenario:{metadata['slug']}",
        ],
        "customFields": {
            "scenario-id": {"string": metadata["id"]},
            "attack-technique": {"string": metadata["technique"]},
            "executed-at": {"string": evidence["executed_at"]},
        },
        "tasks": [
            {"title": "Validate alert fidelity and timestamps", "status": "Waiting"},
            {"title": "Scope affected assets and observables", "status": "Waiting"},
            {"title": "Document containment decision", "status": "Waiting"},
            {"title": "Record lessons learned and rule tuning", "status": "Waiting"},
        ],
    }


def main() -> int:
    scenarios = load_scenarios()
    arguments = parse_arguments(scenarios)
    metadata = scenarios[arguments.scenario]
    root = arguments.root.resolve()
    try:
        source = latest_evidence(root, metadata["id"])
    except FileNotFoundError as error:
        print(str(error), file=sys.stderr)
        return 1
    evidence = json.loads(source.read_text(encoding="utf-8"))
    destination_directory = root / "runtime/evidence/cases"
    destination_directory.mkdir(parents=True, exist_ok=True)
    destination = destination_directory / f"{source.stem}-case.json"
    destination.write_text(
        json.dumps(build_payload(metadata, evidence), indent=2) + "\n",
        encoding="utf-8",
    )
    print(destination)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
