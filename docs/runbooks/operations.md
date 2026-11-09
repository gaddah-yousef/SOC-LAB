# Runbook opérateur

## 1. Préparer la machine

1. Activer Docker Desktop WSL2 Integration ou démarrer Docker Engine.
2. Régler `vm.max_map_count` à `262144` minimum.
3. Installer les dépendances: `python3 -m pip install -r requirements-dev.txt`.
4. Exécuter `make preflight`, puis `make bootstrap`.

Le bootstrap est idempotent: il conserve `.env` et ajoute seulement les nouveaux
secrets requis. Pour une rotation, arrêter le lab, sauvegarder les preuves,
renommer manuellement `.env` et `runtime/config`, puis relancer le bootstrap.

## 2. Démarrer par paliers

```bash
make up PROFILE=core
make health PROFILE=core

make up PROFILE=core,network
make health PROFILE=core,network

# Uniquement sur une machine disposant d'environ 32 Go de RAM
make up PROFILE=core,network,cases
make health PROFILE=core,network,cases
```

Le premier `make up` génère les certificats Wazuh avec l'image officielle. Le
démarrage de l'indexeur peut prendre plusieurs minutes.

## 3. Vérifier le pipeline

1. Ouvrir Wazuh sur <https://127.0.0.1:8443>.
2. Vérifier que `finance-workstation-01` est `Active`.
3. Exécuter `make simulate SCENARIO=ssh-bruteforce`.
4. Rechercher `rule.id:100100` ou `data.srcip:198.51.100.23`.
5. Exécuter `web-recon`, puis rechercher les règles `100110`, `100120` et `100140`.
6. Exécuter `persistence-artifact`, puis rechercher `100130`.
7. Générer le cas: `make case SCENARIO=<slug>`.

## 4. Triage rapide

Pour chaque alerte, consigner:

- timestamp UTC et règle;
- agent/interface et source de log;
- IP, URI, utilisateur ou fichier observé;
- correspondance entre événement brut et description de règle;
- verdict `true-positive-simulation`, `false-positive` ou `inconclusive`;
- action de confinement qui aurait été appliquée en entreprise.

## 5. Ajouter un endpoint réel

Le conteneur agent ne surveille pas l'hôte. Pour une VM Linux/Windows:

1. Conserver la VM sur un réseau de lab isolé.
2. Publier 1514/1515 uniquement sur l'interface de ce réseau via un override
   Compose local non versionné.
3. Installer l'agent Wazuh officiel dans la VM et utiliser l'adresse du host lab.
4. Créer un groupe d'agents distinct et une politique minimale.
5. Ne jamais réutiliser le secret d'enrôlement dans une organisation réelle.

## 6. Diagnostic

```bash
docker compose --project-name enterprise-soc-lab ps
docker compose --project-name enterprise-soc-lab logs --tail=200 wazuh-indexer
docker compose --project-name enterprise-soc-lab logs --tail=200 wazuh-manager
docker compose --project-name enterprise-soc-lab logs --tail=200 suricata zeek
```

| Symptôme | Cause probable | Action |
|---|---|---|
| Docker inaccessible | intégration WSL désactivée | activer WSL Integration et redémarrer Docker Desktop |
| Indexer boucle/restart | `vm.max_map_count` trop bas | appliquer le sysctl puis recréer le conteneur |
| Dashboard 503 | indexer/manager encore en démarrage | consulter health/logs, attendre le délai borné |
| Agent absent | secret/certificat ou enrôlement précédent | vérifier manager/agent logs; ne pas supprimer les volumes à l'aveugle |
| Pas d'EVE/Zeek | profil `network` absent ou capteur arrêté | vérifier profiles, fichiers runtime et logs capteur |
| TheHive ne démarre pas | RAM insuffisante ou dépendance non saine | arrêter `cases`, inspecter Cassandra/Elasticsearch |

## 7. Arrêt, preuves et sauvegarde

`make down` conserve volumes et preuves. Avant un nettoyage complet, copier
`runtime/evidence/` vers un emplacement choisi par l'opérateur et exporter les
captures d'écran. `make destroy CONFIRM_DESTROY=yes` supprime les volumes Docker
et n'est pas récupérable sans sauvegarde.

## 8. Mise à jour contrôlée

1. Lire les release notes officielles et vérifier compatibilités.
2. Modifier une seule famille d'images à la fois.
3. Lancer `make bootstrap`, `make validate`, `make test`, `make config`.
4. Démarrer `core`, rejouer les trois scénarios et comparer les règles attendues.
5. Mettre à jour `NOTICE.md`, le threat model et la preuve de vérification.
