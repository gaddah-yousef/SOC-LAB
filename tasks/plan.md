# Implementation Plan: Enterprise SOC Lab

## Overview

Build a portfolio-grade, Docker Compose SOC lab around the official Wazuh
single-node topology. The main demonstration path combines endpoint telemetry,
live web-target traffic, Suricata/Zeek network telemetry, custom detections and
safe ATT&CK-aligned simulations. Resource-heavy investigation platforms remain
optional profiles so the core path stays usable on a 16 GB workstation.

## Architecture decisions

- Pin Wazuh `4.14.10`, matching the current official Docker documentation and
  compose topology, while replacing documented demo credentials with locally
  generated secrets.
- Bind every administrative UI/API to `127.0.0.1` by default.
- Put the attack simulator and target on an `internal: true` Docker network.
- Share the target network namespace with Suricata and Zeek. This gives sensors
  visibility into target traffic without host networking or Docker socket access.
- Use profiles to isolate optional workloads and one-shot attack emulation.
- Store generated secrets, certificates, telemetry and evidence under ignored
  runtime paths; only templates and fixtures are versioned.
- Treat containerized Wazuh agents as lab endpoints, not as host EDR. Document a
  VM integration path for realistic Windows endpoint coverage.
- Test repository-owned logic with Python `unittest`; validate third-party
  configuration statically and use bounded smoke tests when Docker is available.

## Dependency graph

```text
Project contract and safety rules
  -> bootstrap and generated secrets
    -> Wazuh certificates and core compose
      -> endpoint enrollment and telemetry
      -> network target namespace
        -> Suricata + Zeek events
          -> custom Wazuh rules
            -> ATT&CK scenarios
              -> incident playbooks and portfolio demo
  -> optional cases/intel profiles (independent after core contract)
```

## Task list

### Phase 1: Foundation

- [x] Task 1: Persist project rules, environment contract and safe defaults.
- [x] Task 2: Implement and test deterministic bootstrap/config rendering.
- [x] Task 3: Vendor the minimal official Wazuh configuration with attribution.

### Checkpoint: Foundation

- [x] Bootstrap tests pass without Docker.
- [x] No generated secret or runtime artifact is tracked.
- [x] Compose inputs contain no `latest` tags or wildcard host bindings.

### Phase 2: Core detection path

- [x] Task 4: Compose Wazuh central services and health checks.
- [x] Task 5: Add a monitored Linux endpoint and deterministic endpoint fixtures.
- [x] Task 6: Add the web target, isolated simulator and network sensors.
- [x] Task 7: Add Wazuh/Suricata detections and test fixtures.
- [x] Task 8: Implement three bounded ATT&CK scenarios and evidence collection.

### Checkpoint: Core

- [x] Static validation and unit tests pass.
- [x] All supported Compose profiles render successfully with the Docker client.
- [x] Core scenario contracts map generated evidence to expected detections.

### Phase 3: Investigation and portfolio

- [x] Task 9: Add an optional case-management profile and integration contract.
- [x] Task 10: Add architecture, threat model, playbooks and operator runbooks.
- [x] Task 11: Add a bilingual portfolio demo and defensible CV statements.
- [x] Task 12: Run the final quality/security gate and record limitations.

### Checkpoint: Complete

- [x] All specification criteria are traced to evidence.
- [x] Fresh `make validate` and `make test` runs pass.
- [x] Runtime validation status is reported separately from static validation.

## Risks and mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Docker unavailable in current WSL distro | High | Complete static/unit checks; provide exact WSL integration preflight and never claim runtime success without it. |
| Wazuh certificate/password bootstrapping is complex | High | Follow the official single-node topology, generate local bcrypt hashes and certificates, and test rendered config. |
| Suricata cannot see peer traffic on a normal bridge | High | Share the web target network namespace rather than assuming bridge promiscuous capture. |
| Full stack exceeds workstation memory | High | Keep core and optional investigation/intel workloads in separate profiles with documented budgets. |
| Third-party image/config drift | Medium | Pin explicit versions, record sources and add a controlled upgrade procedure. |
| Lab tooling could reach unintended targets | High | Internal Docker network, allowlisted scenario IDs/URLs, no host networking, no Docker socket, no arbitrary target argument. |
| Wazuh agent in a container is mistaken for host EDR | Medium | Label it as a simulated endpoint and document a real VM/host agent extension. |

## Verification checkpoints

1. `python3 -m unittest discover -s tests -v`
2. `python3 scripts/validate.py`
3. `make validate`
4. `docker compose config` for supported profiles, only when Docker is reachable.
5. Bounded health and smoke tests, only after the user enables Docker WSL2 integration.

## Open questions resolved by approved defaults

- Public name: `Enterprise SOC Lab`.
- Documentation: bilingual summary with English technical artifacts where useful.
- Central platform: Wazuh; case-management and intelligence layers are optional.
- Deployment: single-host Docker lab, not production or HA.
