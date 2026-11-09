#!/usr/bin/env python3
"""Create local SOC lab secrets and runtime directories without overwriting data."""

from __future__ import annotations

import argparse
import os
import secrets
from pathlib import Path

import bcrypt


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = REPOSITORY_ROOT / "config/wazuh-indexer/internal_users.yml.template"
THEHIVE_INDEX_TEMPLATE = REPOSITORY_ROOT / "config/thehive/index.conf.template"
THEHIVE_SECRET_TEMPLATE = REPOSITORY_ROOT / "config/thehive/secret.conf.template"
SECRET_KEYS = (
    "WAZUH_INDEXER_PASSWORD",
    "WAZUH_API_PASSWORD",
    "WAZUH_DASHBOARD_PASSWORD",
    "WAZUH_REGISTRATION_PASSWORD",
    "CASE_MANAGEMENT_SECRET",
    "CASE_INDEX_PASSWORD",
)
RUNTIME_DIRECTORIES = (
    "runtime/certs",
    "runtime/config/wazuh-agent",
    "runtime/config/wazuh-indexer",
    "runtime/config/thehive",
    "runtime/telemetry/endpoint/fim",
    "runtime/telemetry/suricata",
    "runtime/telemetry/zeek",
    "runtime/evidence",
)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=REPOSITORY_ROOT,
        help="project root to initialize (defaults to the repository root)",
    )
    return parser.parse_args()


def parse_env(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if line and not line.startswith("#"):
            key, value = line.split("=", 1)
            values[key] = value
    return values


def create_or_load_secrets(root: Path) -> dict[str, str]:
    env_path = root / ".env"
    if env_path.exists():
        values = parse_env(env_path)
        missing = [key for key in SECRET_KEYS if key not in values]
        if missing:
            additions = {key: secrets.token_urlsafe(32) for key in missing}
            with env_path.open("a", encoding="utf-8") as stream:
                stream.writelines(f"{key}={value}\n" for key, value in additions.items())
            values.update(additions)
            os.chmod(env_path, 0o600)
            print(f"Existing .env preserved; added {len(missing)} new secret(s).")
        else:
            print("Existing .env preserved; secrets were not rotated.")
        return values

    values = {key: secrets.token_urlsafe(32) for key in SECRET_KEYS}
    content = "".join(f"{key}={value}\n" for key, value in values.items())
    descriptor = os.open(env_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
        stream.write(content)
    os.chmod(env_path, 0o600)
    print("Generated .env with local-only credentials.")
    return values


def bcrypt_hash(secret: str) -> str:
    return bcrypt.hashpw(secret.encode(), bcrypt.gensalt(rounds=12)).decode()


def render_internal_users(root: Path, values: dict[str, str]) -> None:
    destination = root / "runtime/config/wazuh-indexer/internal_users.yml"
    template = TEMPLATE.read_text(encoding="utf-8")
    rendered = template.replace(
        "__ADMIN_HASH__", bcrypt_hash(values["WAZUH_INDEXER_PASSWORD"])
    ).replace(
        "__DASHBOARD_HASH__", bcrypt_hash(values["WAZUH_DASHBOARD_PASSWORD"])
    )
    destination.write_text(rendered, encoding="utf-8")
    os.chmod(destination, 0o600)


def render_registration_password(root: Path, values: dict[str, str]) -> None:
    destination = root / "runtime/config/wazuh-agent/authd.pass"
    destination.write_text(values["WAZUH_REGISTRATION_PASSWORD"], encoding="utf-8")
    os.chmod(destination, 0o600)


def render_case_management(root: Path, values: dict[str, str]) -> None:
    destination = root / "runtime/config/thehive"
    index_config = THEHIVE_INDEX_TEMPLATE.read_text(encoding="utf-8").replace(
        "__CASE_INDEX_PASSWORD__", values["CASE_INDEX_PASSWORD"]
    )
    secret_config = THEHIVE_SECRET_TEMPLATE.read_text(encoding="utf-8").replace(
        "__CASE_MANAGEMENT_SECRET__", values["CASE_MANAGEMENT_SECRET"]
    )
    (destination / "index.conf").write_text(index_config, encoding="utf-8")
    (destination / "secret.conf").write_text(secret_config, encoding="utf-8")
    os.chmod(destination / "index.conf", 0o600)
    os.chmod(destination / "secret.conf", 0o600)


def main() -> int:
    root = parse_arguments().root.resolve()
    root.mkdir(parents=True, exist_ok=True)
    for relative_path in RUNTIME_DIRECTORIES:
        (root / relative_path).mkdir(parents=True, exist_ok=True)
    values = create_or_load_secrets(root)
    render_internal_users(root, values)
    render_registration_password(root, values)
    render_case_management(root, values)
    print("Runtime layout and Wazuh indexer credentials are ready.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
