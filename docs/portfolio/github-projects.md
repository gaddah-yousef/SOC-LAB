# GitHub Cybersecurity Portfolio — Yousef Gaddah

> **Purpose:** A recruiter- and mentor-friendly index of technically relevant GitHub projects, organized by specialization, maturity and suggested demonstration. Repository names and content were reviewed on 13 November 2026. **This is a portfolio catalog, not an independent certification that the projects work end to end.**

## Career focus

Engineering student specializing in **Cybersecurity & Cloud Computing**, with hands-on work across **SOC / Blue Team, Cyber Threat Intelligence, Cloud Security, DevSecOps, application security and security automation**.

**GitHub profile:** https://github.com/gaddah-yousef

## Featured projects

| Priority | Project | Area | What to review | Evidence / maturity |
| --- | --- | --- | --- | --- |
| 1 | [SOC-LAB](https://github.com/gaddah-yousef/SOC-LAB) | SOC, SIEM, detection engineering | Wazuh, Suricata, Zeek, emulations, playbooks, test suite | Detailed docs and test sources; run the demo to establish runtime status |
| 2 | [PFA Cyber Threat Intelligence — Sentinel PME](https://github.com/gaddah-yousef/-PFA-Cyber-Threat-Intelligence) | CTI, threat data, application security | FastAPI, collectors, CVE/EPSS/KEV context, React dashboard, risk scoring | Large implementation with docs/tests/CI; review deployment evidence |
| 3 | [Smart Hospital SIEM](https://github.com/gaddah-yousef/-Smart-Hospital-SIEM) | SOC, IoT security, observability | Healthcare telemetry, detection rules, Docker services, Grafana | Multi-service research prototype; independently verify performance claims |
| 4 | [SupplyGuard](https://github.com/gaddah-yousef/SupplyGuard) | DevSecOps, supply-chain security | FastAPI, Pytest, Semgrep, Trivy, Gitleaks, CycloneDX, GHCR | Small code-focused lab; CI results must be checked |
| 5 | [PME SecureOps](https://github.com/gaddah-yousef/pme-secureops) | Azure Cloud Security, GRC, FinOps | Score engines, mock/Azure provider, CLI, Streamlit | Prototype with mock mode; verify real Azure mode separately |
| 6 | [AWS Infrastructure Labs](https://github.com/gaddah-yousef/AWS_Projets) | AWS Cloud Security, networking | VPC, peering, ALB/EC2, hybrid VPN, FinOps scripts | Lab scripts; several guides need reconciliation with implemented files |
| 7 | [YGscan](https://github.com/gaddah-yousef/YGscan) | Web pentest, security tooling | Active/passive scanning and plugin internals | Customized upstream project; preserve original contributors' attribution |
| 8 | [n8n Security Audit](https://github.com/gaddah-yousef/-n8n-security-audit) | Security automation | Workflow JSON, code/secret checks, reporting | Workflow-based demonstration; avoid publishing tokens |
| 9 | [Phishing Detection for SMEs](https://github.com/gaddah-yousef/detecteur-phishing-pme) | Threat Intel, ML fundamentals | PhishTank collection, feature extraction, Streamlit | Milestone prototype, not a validated trained classifier |
| 10 | [Quasar RAT — Defensive Research](https://github.com/gaddah-yousef/Quasar-RAT-Red-Team-Research-Windows-Detection-Analysis) | Blue Team, malware analysis | Benign heartbeat emulation, Windows logging, detection research | Documentation and safe lab; no claim of live RAT evasion |

## Additional projects by category

**Security labs and workflows**
- [SecureLab](https://github.com/gaddah-yousef/securelab) — vulnerable web lab, Nginx logs, Loki/Promtail/Grafana; integration issues documented.
- [SupplyGuard](https://github.com/gaddah-yousef/SupplyGuard) — secure CI/CD.
- [Phishing Detection](https://github.com/gaddah-yousef/detecteur-phishing-pme) — data collection and ML exercise.

**Cloud and engineering**
- [AWS Infrastructure Labs](https://github.com/gaddah-yousef/AWS_Projets)
- [PME SecureOps](https://github.com/gaddah-yousef/pme-secureops)
- [Predictive Maintenance CMAPSS](https://github.com/gaddah-yousef/predictive-maintenance-cmapss) — data-science and machine-learning project.

**Software and other academic projects**
- [MediSync](https://github.com/gaddah-yousef/-medisync) — Angular app.
- [Little Mamma Agdal](https://github.com/gaddah-yousef/little-mamma-agdal), [Capanna](https://github.com/gaddah-yousef/capanna), [Simulation Retraite](https://github.com/gaddah-yousef/simulation_retraite) — examples outside the primary cybersecurity focus.

## How to present the portfolio during a SOC interview

Start with **SOC-LAB**, rather than presenting all repositories at once.

1. **Problem:** what security behavior should the lab detect?
2. **Architecture:** where do endpoint logs, network telemetry and correlation rules live?
3. **Reproduction:** show one of the documented controlled attack simulations.
4. **Evidence:** demonstrate observed logs, alerts, ATT&CK mapping and the case bundle.
5. **Response:** explain the triage and investigation playbook, including potential false positives.
6. **Limitations:** distinguish simulated endpoint data from production EDR deployment, and passive IDS from IPS blocking.

Next demonstrate **Sentinel PME** for CTI and **SupplyGuard** for DevSecOps. This three-project sequence illustrates **detect → enrich → engineer securely**.

## What each README should prove

For recruiting purposes, every project should ideally answer:

1. **Why:** security or engineering problem and intended users.
2. **What:** actual implemented capabilities, not planned features.
3. **How:** architectural diagram, dependencies and main files.
4. **Run:** safe, reproducible installation and setup.
5. **Validate:** tests, sample evidence, metrics and known outcomes.
6. **Security:** authorized use, boundaries, threat model and secret handling.
7. **Limitations:** what is not implemented or verified.
8. **Ownership:** individual contribution, upstream credit and collaborators where applicable.
9. **Next:** focused roadmap.

**Avoid unsupported claims:** live production use, perfect accuracy, <3-second detection, production-readiness, deployment success, Microsoft Defender evasion or zero false positives without reproducible evidence.

## Recommended GitHub profile presentation

**Suggested pinned repos (six):**
1. `SOC-LAB`
2. `-PFA-Cyber-Threat-Intelligence`
3. `-Smart-Hospital-SIEM`
4. `SupplyGuard`
5. `pme-secureops`
6. `YGscan` *(or `AWS_Projets` if prioritizing Cloud Security roles)*

**Suggested profile headline:**

> Cybersecurity & Cloud Computing Engineering Student | SOC & Detection Engineering | Cloud Security | DevSecOps | Threat Intelligence

**Suggested repository topics:**
- `SOC-LAB`: `soc`, `siem`, `wazuh`, `suricata`, `zeek`, `mitre-attack`, `detection-engineering`
- `-PFA-Cyber-Threat-Intelligence`: `threat-intelligence`, `fastapi`, `cve`, `cvss`, `risk-scoring`
- `SupplyGuard`: `devsecops`, `github-actions`, `trivy`, `semgrep`, `sbom`
- `pme-secureops`: `azure`, `cloud-security`, `compliance`, `finops`
- `AWS_Projets`: `aws`, `vpc`, `cloud-security`, `infrastructure`
- `YGscan`: `web-security`, `vulnerability-scanner`, `python`, `pentesting`

**Organization note:** GitHub does not support hierarchical folders for repositories on the profile. Use **pinned repositories, repository topics, clear descriptions and a profile README** to create a coherent navigation structure. Repository renames or archival should be handled only after checking references and the project's maturity.

## Maintenance priorities

**Priority A — presentation:** concise and accurate README, diagram, setup, demo, limitations.

**Priority B — engineering credibility:** green CI, runtime smoke tests, dependency scanning, pinned versions and proof screenshots from local tests.

**Priority C — repo hygiene:** remove generated binaries, credentials and sensitive documents; review unexpectedly large repositories and empty demo repositories; validate licensing and third-party authorship.

**Priority D — UX:** consistent English/French terminology, non-broken badges, clear "work in progress" labels and a featured six-repository story.

---

Prepared as a technical **portfolio organization guide**; no project code has been modified by this index.
