#!/usr/bin/env bash
set -Eeuo pipefail

fail() {
  printf 'preflight error: %s\n' "$1" >&2
  exit 1
}

command -v docker >/dev/null 2>&1 || fail "Docker CLI is not installed"
docker info >/dev/null 2>&1 || fail "Docker Engine is unreachable; enable Docker Desktop WSL2 integration"
docker compose version >/dev/null 2>&1 || fail "Docker Compose v2 is required"

if [[ -r /proc/sys/vm/max_map_count ]]; then
  map_count="$(</proc/sys/vm/max_map_count)"
  if (( map_count < 262144 )); then
    fail "vm.max_map_count=${map_count}; Wazuh requires at least 262144"
  fi
fi

printf 'Docker, Compose and kernel preflight checks passed.\n'
