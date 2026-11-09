#!/usr/bin/env bash
set -Eeuo pipefail

readonly profiles=",${COMPOSE_PROFILES:-core},"
readonly attempts=24
readonly delay_seconds=5

wait_for_url() {
  local name="$1"
  local url="$2"
  local attempt
  for ((attempt = 1; attempt <= attempts; attempt++)); do
    if curl --silent --show-error --insecure --output /dev/null "$url"; then
      printf '%-18s healthy (%s)\n' "$name" "$url"
      return 0
    fi
    sleep "$delay_seconds"
  done
  printf '%-18s unhealthy after %ss (%s)\n' "$name" "$((attempts * delay_seconds))" "$url" >&2
  return 1
}

docker info >/dev/null 2>&1 || {
  printf 'Docker Engine is unreachable; enable Docker Desktop WSL2 integration.\n' >&2
  exit 1
}

status=0
if [[ "$profiles" == *",core,"* ]]; then
  wait_for_url "Wazuh indexer" "https://127.0.0.1:9200" || status=1
  wait_for_url "Wazuh dashboard" "https://127.0.0.1:8443" || status=1
  wait_for_url "Web target" "http://127.0.0.1:3000" || status=1
fi
if [[ "$profiles" == *",cases,"* ]]; then
  wait_for_url "TheHive" "http://127.0.0.1:9000/thehive/api/status" || status=1
fi

docker compose --project-name enterprise-soc-lab ps
exit "$status"
