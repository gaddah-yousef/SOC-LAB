# Third-party configuration notice

The Wazuh Compose topology and configuration keys in this repository are
adapted from the official `wazuh/wazuh-docker` single-node deployment tagged
`v4.14.10` (GPL-2.0). Project-specific changes include loopback-only published
ports, generated credentials, profiles, lab telemetry mounts and custom rules.

Sources reviewed:

- <https://github.com/wazuh/wazuh-docker/tree/v4.14.10/single-node>
- <https://documentation.wazuh.com/current/deployment-options/docker/wazuh-container.html>

Third-party container images retain their own licenses and notices. This
repository does not redistribute those images.
