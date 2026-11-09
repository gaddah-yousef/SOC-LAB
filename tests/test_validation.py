from __future__ import annotations

import unittest
from pathlib import Path

from scripts.validate import validate_compose, validate_repository


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


class ComposePolicyTests(unittest.TestCase):
    def test_rejects_unpinned_images_and_public_admin_ports(self) -> None:
        compose = {
            "services": {
                "unsafe": {
                    "image": "vendor/product:latest",
                    "ports": ["0.0.0.0:9200:9200"],
                }
            },
            "networks": {},
        }

        findings = validate_compose(compose)

        self.assertTrue(any("latest" in finding for finding in findings))
        self.assertTrue(any("loopback" in finding for finding in findings))

    def test_rejects_host_network_privileged_and_docker_socket(self) -> None:
        compose = {
            "services": {
                "unsafe": {
                    "image": "vendor/product:1.2.3",
                    "network_mode": "host",
                    "privileged": True,
                    "volumes": ["/var/run/docker.sock:/var/run/docker.sock"],
                }
            },
            "networks": {},
        }

        findings = validate_compose(compose)

        self.assertTrue(any("host network" in finding for finding in findings))
        self.assertTrue(any("privileged" in finding for finding in findings))
        self.assertTrue(any("Docker socket" in finding for finding in findings))

    def test_repository_passes_project_policy(self) -> None:
        findings = validate_repository(REPOSITORY_ROOT)
        self.assertEqual(findings, [], "\n".join(findings))


if __name__ == "__main__":
    unittest.main()
