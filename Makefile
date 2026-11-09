SHELL := /usr/bin/env bash
.DEFAULT_GOAL := help

PROFILE ?= core
SCENARIO ?=
COMPOSE := docker compose --project-name enterprise-soc-lab

.PHONY: help bootstrap preflight certs validate test config up health simulate case down destroy

help: ## Show the available operator commands.
	@awk 'BEGIN {FS = ":.*## "; print "Enterprise SOC Lab\n"} /^[a-zA-Z_-]+:.*## / {printf "  %-12s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

bootstrap: ## Generate local secrets and the ignored runtime layout.
	python3 scripts/bootstrap.py

preflight: ## Check Docker, Compose and Wazuh host kernel requirements.
	scripts/preflight.sh

certs: bootstrap ## Generate Wazuh TLS certificates once with the official tool.
	scripts/generate-certs.sh

validate: ## Validate repository policy and configuration syntax.
	python3 scripts/validate.py

test: ## Run the deterministic unit and contract test suite.
	python3 -m unittest discover -s tests -v

config: bootstrap ## Render Compose for the requested comma-separated profiles.
	COMPOSE_PROFILES="$(PROFILE)" $(COMPOSE) config --quiet

up: preflight certs ## Start the requested profiles (default: core).
	COMPOSE_PROFILES="$(PROFILE)" $(COMPOSE) up -d

health: ## Run bounded health checks for enabled services.
	COMPOSE_PROFILES="$(PROFILE)" scripts/health.sh

simulate: ## Run one allowlisted scenario, e.g. SCENARIO=ssh-bruteforce.
	@test -n "$(SCENARIO)" || { echo "SCENARIO is required" >&2; exit 2; }
	python3 scripts/simulate.py "$(SCENARIO)"

case: ## Build a TheHive-ready case bundle from the latest scenario evidence.
	@test -n "$(SCENARIO)" || { echo "SCENARIO is required" >&2; exit 2; }
	python3 scripts/build_case.py "$(SCENARIO)"

down: ## Stop containers while retaining volumes and evidence.
	$(COMPOSE) down

destroy: ## Delete containers and volumes; requires CONFIRM_DESTROY=yes.
	@test "$(CONFIRM_DESTROY)" = "yes" || { echo "Refusing destructive cleanup. Re-run with CONFIRM_DESTROY=yes" >&2; exit 2; }
	$(COMPOSE) down --volumes --remove-orphans
