# État de vérification

Date de référence: 2026-11-09.

## Vérifié dans l'environnement de construction

- parsing YAML de Compose et des configurations;
- parsing XML Wazuh agent/manager/règles;
- politiques de sécurité Compose;
- bootstrap idempotent, secrets forts, bcrypt et rendu TheHive;
- contrats des trois scénarios et rejet des slugs inconnus;
- génération de bundles de cas;
- mappings ATT&CK et nombre minimum de détections.
- rendu Docker Compose de tous les profils via le client Docker Windows.

Commandes de preuve:

```bash
make validate
make test
python3 -m compileall -q scripts tests
```

## Non vérifié dans l'environnement de construction

Docker Desktop était installé puis a été démarré côté Windows, mais le moteur
Linux n'a pas répondu dans le délai borné et l'intégration WSL2 restait inactive.
Les images n'ont donc pas été tirées et les conteneurs n'ont pas été démarrés
ici. Cela interdit d'affirmer que les health checks runtime ou le parcours UI
ont réussi dans cet environnement.

Pour fermer ce point:

1. activer Docker Desktop WSL2 Integration;
2. exécuter `make preflight`;
3. exécuter `make config PROFILE=core,network,cases`;
4. démarrer `core,network` et exécuter `make health`;
5. rejouer les trois scénarios et capturer les rule IDs attendus;
6. démarrer `cases` séparément si la machine dispose des ressources;
7. consigner versions, durée, résultats et captures dans ce document.

## Critères de clôture runtime

- Wazuh dashboard accessible et agent actif;
- fichiers EVE/Zeek alimentés après `web-recon`;
- règles `100100`, `100110`, `100120`, `100130`, `100140`, `100150` observées;
- bundle accepté/recréé manuellement dans TheHive;
- aucun port publié hors loopback;
- `docker compose ps` sans service unhealthy.
