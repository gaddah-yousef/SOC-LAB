#!/usr/bin/env bash
set -Eeuo pipefail

readonly required_certificates=(
  root-ca.pem
  root-ca-manager.pem
  admin.pem
  admin-key.pem
  wazuh.indexer.pem
  wazuh.indexer-key.pem
  wazuh.manager.pem
  wazuh.manager-key.pem
  wazuh.dashboard.pem
  wazuh.dashboard-key.pem
)

all_present=true
for certificate in "${required_certificates[@]}"; do
  if [[ ! -s "runtime/certs/${certificate}" ]]; then
    all_present=false
    break
  fi
done

if [[ "$all_present" == true ]]; then
  printf 'Existing Wazuh certificates preserved.\n'
  exit 0
fi

docker compose --project-name enterprise-soc-lab \
  --profile bootstrap run --rm cert-generator

for certificate in "${required_certificates[@]}"; do
  [[ -s "runtime/certs/${certificate}" ]] || {
    printf 'certificate generation failed: %s is missing\n' "$certificate" >&2
    exit 1
  }
done

printf 'Wazuh certificates generated under runtime/certs.\n'
