# Enterprise SOC Lab — Task checklist

## Task 1: Project contract

**Acceptance:** project rules, `.env.example`, ignore rules and stable commands
exist; destructive and network boundaries are explicit.

**Verify:** `python3 scripts/validate.py` (available after Task 2).

**Dependencies:** None.

**Files:** `AGENTS.md`, `.gitignore`, `.env.example`, `Makefile`.

- [x] Complete

## Task 2: Safe bootstrap

**Acceptance:** bootstrap creates strong local secrets and runtime directories,
is idempotent, and never overwrites an existing secret file.

**Verify:** `python3 -m unittest tests.test_bootstrap -v`.

**Dependencies:** Task 1.

**Files:** `scripts/bootstrap.py`, `tests/test_bootstrap.py`,
`config/wazuh-indexer/internal_users.yml.template`.

- [x] Complete

## Task 3: Wazuh configuration baseline

**Acceptance:** minimal upstream-derived configuration is attributed, pinned and
extended only for lab telemetry paths.

**Verify:** XML/YAML parsing plus source/version checks in `make validate`.

**Dependencies:** Task 2.

**Files:** up to five files under `config/wazuh-*` plus `NOTICE.md`.

- [x] Complete

## Task 4: Wazuh core compose

**Acceptance:** manager, indexer and dashboard are persistent, loopback-bound and
use generated secrets/certificates.

**Verify:** static compose validation; bounded health check when Docker exists.

**Dependencies:** Tasks 2-3.

**Files:** `compose.yaml`, `compose/wazuh.yaml`, `scripts/health.sh`.

- [x] Complete

## Task 5: Endpoint telemetry

**Acceptance:** the simulated Linux endpoint enrolls with Wazuh, monitors auth
logs and FIM paths, and is honestly described as container-scoped.

**Verify:** config parse and endpoint fixture contract test.

**Dependencies:** Task 4.

**Files:** `compose/endpoint.yaml`, `config/wazuh-agent/ossec.conf`, endpoint fixtures.

- [x] Complete

## Task 6: Network visibility

**Acceptance:** web target and simulator use an internal network; Suricata and
Zeek share the target namespace and write telemetry for Wazuh.

**Verify:** static privilege/network-policy tests and compose rendering.

**Dependencies:** Task 4.

**Files:** `compose/network.yaml`, Suricata config/rules, Zeek policy.

- [x] Complete

## Task 7: Detection pack

**Acceptance:** at least five custom detections cover endpoint, web and network
behaviors and map to ATT&CK.

**Verify:** detection metadata/unit tests and Wazuh rule syntax checks.

**Dependencies:** Tasks 5-6.

**Files:** `detections/` rules, metadata and fixtures.

- [x] Complete

## Task 8: Attack scenarios

**Acceptance:** three allowlisted, non-destructive scenarios produce expected
endpoint/network/application evidence without arbitrary targets.

**Verify:** scenario contract tests and `make simulate --dry-run` equivalent.

**Dependencies:** Task 7.

**Files:** `scenarios/`, `scripts/simulate.py`, scenario tests.

- [x] Complete

## Task 9: Optional investigation profile

**Acceptance:** a resource-isolated, loopback-bound case-management profile and
documented Wazuh handoff contract exist without blocking core startup.

**Verify:** config parse and profile validation.

**Dependencies:** Task 4.

**Files:** `compose/cases.yaml`, relevant config and integration documentation.

- [x] Complete

## Task 10: Operations and response documentation

**Acceptance:** architecture, threat model, operations runbook and three incident
playbooks reflect the implemented system.

**Verify:** documentation link and command checks.

**Dependencies:** Tasks 4-9.

**Files:** focused documents under `docs/`.

- [x] Complete

## Task 11: Portfolio presentation

**Acceptance:** the README explains the lab architecture, supported scenarios,
security boundaries and links to technical playbooks.

**Verify:** manual documentation review against the implementation.

**Dependencies:** Tasks 8 and 10.

**Files:** `README.md`, `docs/architecture/` and `docs/playbooks/`.

- [x] Complete

## Task 12: Final gate

**Acceptance:** all feasible checks pass; Docker-dependent checks are executed or
explicitly marked blocked with the exact remediation.

**Verify:** fresh `make validate` and `make test`, plus requirement traceability.

**Dependencies:** Tasks 1-11.

**Files:** `tasks/todo.md`, `.github/workflows/quality.yml`.

- [x] Complete
