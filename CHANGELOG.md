# Changelog

All notable changes to this project are documented here.

## [1.0.0] - 2026-11-09

### Added

- Wazuh 4.14.10 SIEM/HIDS core with generated credentials and TLS certificates.
- Simulated Linux endpoint with FIM, authentication logs and inventory telemetry.
- Suricata 8 and Zeek 9 sensors sharing the web target network namespace.
- Six Wazuh detections, three Suricata signatures and ATT&CK metadata.
- Three safe simulations for SSH guessing, web reconnaissance and persistence.
- TheHive 6 optional case-management profile and case-bundle generator.
- MISP-compatible local threat feed and Wazuh CDB IOC correlation.
- Security policy validator, unit/contract tests and GitHub Actions quality gate.
- Architecture, threat model, runbook, incident playbooks and bilingual portfolio guide.

### Security

- All published ports bind to loopback by default.
- Attack networks are internal; arbitrary targets, host networking, privileged
  containers and Docker socket mounts are rejected by policy.
- Secrets, certificates, telemetry and evidence are generated locally and ignored.

### Known limitations

- Runtime container startup was not verified in the original build environment
  because the Docker Linux engine remained unavailable; client-side Compose
  rendering and all repository tests passed.
- Image versions are pinned by tag, not by digest.
- Suricata runs as passive IDS; inline IPS is intentionally out of scope.
