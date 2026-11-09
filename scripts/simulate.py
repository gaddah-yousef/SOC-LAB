#!/usr/bin/env python3
"""Run one allowlisted, non-destructive SOC lab scenario."""

from __future__ import annotations

import argparse
import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = REPOSITORY_ROOT / "scenarios" / "catalog.yml"
FIXED_SOURCE_IP = "198.51.100.23"


def load_catalog() -> dict[str, dict[str, Any]]:
    document = yaml.safe_load(CATALOG_PATH.read_text(encoding="utf-8"))
    return {item["slug"]: item for item in document["scenarios"]}


def parse_arguments(catalog: dict[str, dict[str, Any]]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scenario", choices=sorted(catalog))
    parser.add_argument("--dry-run", action="store_true", help="print the fixed plan")
    parser.add_argument(
        "--root",
        type=Path,
        default=REPOSITORY_ROOT,
        help=argparse.SUPPRESS,
    )
    return parser.parse_args()


def plan_for(slug: str, metadata: dict[str, Any]) -> dict[str, Any]:
    actions = {
        "ssh-bruteforce": [
            "append six synthetic sshd failures to runtime endpoint telemetry"
        ],
        "web-recon": [
            "run pinned curl simulator against http://web-target:3000/ftp"
        ],
        "persistence-artifact": [
            "create inert runtime/telemetry/endpoint/fim/lab-update.conf"
        ],
    }
    return {
        "id": metadata["id"],
        "scenario": slug,
        "technique": metadata["technique"],
        "actions": actions[slug],
        "expected_rules": metadata["expected_rules"],
        "safety_controls": metadata["safety_controls"],
    }


def simulate_ssh_failures(root: Path) -> list[str]:
    destination = root / "runtime/telemetry/endpoint/auth.log"
    destination.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(UTC).strftime("%b %d %H:%M:%S")
    lines = [
        (
            f"{timestamp} finance-workstation-01 sshd[{4100 + attempt}]: "
            f"Failed password for invalid user svc-backup from {FIXED_SOURCE_IP} "
            f"port {50100 + attempt} ssh2"
        )
        for attempt in range(6)
    ]
    with destination.open("a", encoding="utf-8") as stream:
        stream.write("\n".join(lines) + "\n")
    return [str(destination.relative_to(root))]


def simulate_web_recon(root: Path) -> list[str]:
    command = [
        "docker",
        "compose",
        "--project-name",
        "enterprise-soc-lab",
        "--profile",
        "core",
        "--profile",
        "network",
        "--profile",
        "attack",
        "run",
        "--rm",
        "attack-simulator",
        "--fail-with-body",
        "--silent",
        "--show-error",
        "--max-time",
        "10",
        "--user-agent",
        "Enterprise-SOC-Lab-Recon/1.0",
        "http://web-target:3000/ftp",
    ]
    result = subprocess.run(command, cwd=root, check=False)
    if result.returncode != 0:
        raise RuntimeError(
            "web scenario failed; start core,network and verify Docker integration"
        )
    return [
        "runtime/telemetry/suricata/eve.json",
        "runtime/telemetry/zeek/http.log",
    ]


def simulate_persistence_artifact(root: Path) -> list[str]:
    destination = root / "runtime/telemetry/endpoint/fim/lab-update.conf"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        "# inert SOC lab fixture; this file is never executed\n"
        "scenario=LAB-ENDPOINT-002\n",
        encoding="utf-8",
    )
    return [str(destination.relative_to(root))]


def write_evidence(
    root: Path, metadata: dict[str, Any], generated_artifacts: list[str]
) -> Path:
    evidence_directory = root / "runtime/evidence"
    evidence_directory.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(UTC)
    destination = evidence_directory / (
        f"{metadata['id']}-{timestamp.strftime('%Y%m%dT%H%M%SZ')}.json"
    )
    destination.write_text(
        json.dumps(
            {
                "scenario_id": metadata["id"],
                "scenario": metadata["slug"],
                "executed_at": timestamp.isoformat(),
                "technique": metadata["technique"],
                "expected_rules": metadata["expected_rules"],
                "generated_artifacts": generated_artifacts,
                "result": "simulation-generated",
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return destination


def main() -> int:
    catalog = load_catalog()
    arguments = parse_arguments(catalog)
    metadata = catalog[arguments.scenario]
    if arguments.dry_run:
        print(json.dumps(plan_for(arguments.scenario, metadata), indent=2))
        return 0

    root = arguments.root.resolve()
    runners = {
        "ssh-bruteforce": simulate_ssh_failures,
        "web-recon": simulate_web_recon,
        "persistence-artifact": simulate_persistence_artifact,
    }
    generated = runners[arguments.scenario](root)
    evidence = write_evidence(root, metadata, generated)
    print(f"Scenario {metadata['id']} generated; evidence: {evidence}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
