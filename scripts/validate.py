#!/usr/bin/env python3
"""Validate repository configuration and enforce the SOC lab safety policy."""

from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

import yaml


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
MOVING_TAGS = {"latest", "snapshot", "main", "master", "stable", "lts"}
ALLOWED_CAPABILITIES = {
    "suricata": {"NET_ADMIN", "NET_RAW"},
    "zeek": {"NET_RAW"},
}


def image_tag(image: str) -> str | None:
    without_digest = image.split("@", 1)[0]
    final_component = without_digest.rsplit("/", 1)[-1]
    if ":" not in final_component:
        return None
    return final_component.rsplit(":", 1)[1]


def validate_compose(compose: dict[str, Any]) -> list[str]:
    findings: list[str] = []
    services = compose.get("services", {})
    networks = compose.get("networks", {})

    for name, service in services.items():
        image = service.get("image", "")
        tag = image_tag(image)
        if not tag:
            findings.append(f"{name}: image is not pinned to an explicit tag")
        elif tag.lower() in MOVING_TAGS:
            findings.append(f"{name}: moving image tag '{tag}' is forbidden")

        for published_port in service.get("ports", []):
            value = (
                published_port
                if isinstance(published_port, str)
                else str(published_port.get("host_ip", ""))
            )
            if not value.startswith("127.0.0.1:"):
                findings.append(
                    f"{name}: published port must bind to loopback: {published_port}"
                )

        if service.get("network_mode") == "host":
            findings.append(f"{name}: host network mode is forbidden")
        if service.get("privileged") is True:
            findings.append(f"{name}: privileged containers are forbidden")

        for volume in service.get("volumes", []):
            volume_text = volume if isinstance(volume, str) else str(volume)
            source = volume_text.split(":", 1)[0]
            if "docker.sock" in volume_text:
                findings.append(f"{name}: mounting the Docker socket is forbidden")
            if source in {"/", "/etc", "/var", "/home"}:
                findings.append(f"{name}: broad host mount is forbidden: {source}")

        capabilities = set(service.get("cap_add", []))
        allowed = ALLOWED_CAPABILITIES.get(name, set())
        unexpected = capabilities - allowed
        if unexpected:
            findings.append(
                f"{name}: undocumented capabilities: {', '.join(sorted(unexpected))}"
            )

    target_network = networks.get("target-segment", {})
    if target_network.get("internal") is not True:
        findings.append("target-segment: attack network must be internal")

    simulator = services.get("attack-simulator", {})
    if "target-segment" not in simulator.get("networks", []):
        findings.append("attack-simulator: must only join target-segment")
    if simulator.get("cap_drop") != ["ALL"]:
        findings.append("attack-simulator: must drop all Linux capabilities")
    if simulator.get("read_only") is not True:
        findings.append("attack-simulator: root filesystem must be read-only")

    return findings


def validate_xml_files(root: Path) -> list[str]:
    findings: list[str] = []
    paths = [
        root / "config/wazuh-manager/ossec.conf",
        root / "config/wazuh-agent/ossec.conf",
        root / "detections/wazuh/local_rules.xml",
    ]
    for path in paths:
        try:
            ET.parse(path)
        except (ET.ParseError, OSError) as error:
            findings.append(f"{path.relative_to(root)}: invalid XML: {error}")
    return findings


def validate_detection_pack(root: Path) -> list[str]:
    findings: list[str] = []
    try:
        rules_root = ET.parse(root / "detections/wazuh/local_rules.xml").getroot()
    except (ET.ParseError, OSError):
        return findings

    rules = rules_root.findall("rule")
    rule_ids = [rule.get("id", "") for rule in rules]
    if len(rules) < 5:
        findings.append("detections/wazuh: at least five Wazuh rules are required")
    if len(rule_ids) != len(set(rule_ids)):
        findings.append("detections/wazuh: rule IDs must be unique")
    for rule in rules:
        if not rule.findall("./mitre/id"):
            findings.append(f"Wazuh rule {rule.get('id')}: missing MITRE mapping")

    suricata_rules = (root / "detections/suricata/lab.rules").read_text(
        encoding="utf-8"
    )
    suricata_ids = re.findall(r"\bsid:(\d+);", suricata_rules)
    if len(suricata_ids) < 3 or len(suricata_ids) != len(set(suricata_ids)):
        findings.append("detections/suricata: require three unique signature IDs")
    return findings


def validate_scenarios(root: Path) -> list[str]:
    findings: list[str] = []
    try:
        catalog = yaml.safe_load(
            (root / "scenarios/catalog.yml").read_text(encoding="utf-8")
        )
        scenarios = catalog["scenarios"]
    except (OSError, KeyError, TypeError, yaml.YAMLError) as error:
        return [f"scenarios/catalog.yml: invalid catalog: {error}"]
    if len(scenarios) < 3:
        findings.append("scenarios: at least three scenarios are required")
    slugs = [item.get("slug") for item in scenarios]
    if len(slugs) != len(set(slugs)):
        findings.append("scenarios: slugs must be unique")
    for item in scenarios:
        if not re.fullmatch(r"T\d{4}(?:\.\d{3})?", item.get("technique", "")):
            findings.append(f"scenario {item.get('slug')}: invalid ATT&CK technique")
        if not item.get("expected_rules") or not item.get("safety_controls"):
            findings.append(f"scenario {item.get('slug')}: incomplete contract")
    return findings


def validate_repository(root: Path) -> list[str]:
    findings: list[str] = []
    try:
        compose = yaml.safe_load((root / "compose.yaml").read_text(encoding="utf-8"))
        findings.extend(validate_compose(compose))
    except (OSError, yaml.YAMLError) as error:
        findings.append(f"compose.yaml: invalid YAML: {error}")

    findings.extend(validate_xml_files(root))
    findings.extend(validate_detection_pack(root))
    findings.extend(validate_scenarios(root))

    gitignore = (root / ".gitignore").read_text(encoding="utf-8").splitlines()
    for required_entry in (".env", "runtime/"):
        if required_entry not in gitignore:
            findings.append(f".gitignore: missing {required_entry}")

    deployable_paths = [root / "compose.yaml", root / ".env.example"]
    deployable_paths.extend(path for path in (root / "config").rglob("*") if path.is_file())
    for path in deployable_paths:
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for known_default in ("SecretPassword", "MyS3cr37P450r"):
            if known_default in content:
                findings.append(
                    f"{path.relative_to(root)}: known Wazuh demo credential found"
                )

    return sorted(set(findings))


def main() -> int:
    findings = validate_repository(REPOSITORY_ROOT)
    if findings:
        print("Validation failed:", file=sys.stderr)
        for finding in findings:
            print(f"- {finding}", file=sys.stderr)
        return 1
    print("Repository policy, XML, YAML, detection and scenario checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
