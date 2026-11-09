# Spécification — Enterprise SOC Lab

## Objectif

Construire un laboratoire SOC d'entreprise avancé, reproductible avec Docker
Compose, destiné à démontrer sur un CV et en entretien des compétences de
SOC analyst, detection engineer, incident responder et security engineer.

Le laboratoire doit permettre à un recruteur ou à un évaluateur de lancer une
pile minimale, de générer des événements d'attaque confinés, d'observer leur
détection, de créer un incident et de suivre une réponse documentée.

### Utilisateurs cibles

- Candidat cybersécurité qui présente le projet dans son portfolio.
- Analyste SOC L1/L2 qui investigue les alertes et enrichit les incidents.
- Detection engineer qui écrit, teste et versionne des règles.
- Incident responder qui exécute des playbooks et collecte des preuves.

### Parcours démontrable

1. Démarrer le profil SOC principal.
2. Vérifier la santé de tous les services.
3. Exécuter un scénario d'attaque ATT&CK autorisé et confiné.
4. Observer les événements endpoint et réseau dans le SIEM.
5. Qualifier l'alerte, créer un cas et exécuter le playbook associé.
6. Produire un rapport contenant chronologie, preuves, décision et remédiation.

## Hypothèses et périmètre

- Hôte supporté : Linux x86_64 ou Docker Desktop avec WSL2.
- Ressources : 16 Go de RAM minimum pour `core`; 32 Go recommandés pour
  `enterprise`; 50 Go d'espace disque disponible.
- Les endpoints Linux sont conteneurisés. Un endpoint Windows est décrit comme
  extension VM, sans prétendre exécuter Windows dans un conteneur Linux.
- Wazuh assure le SIEM et le HIDS/EDR du lab; Suricata assure la détection
  réseau et un mode IPS optionnel; Zeek fournit les métadonnées réseau.
- TheHive/Cortex assurent la gestion de cas et l'enrichissement; MISP fournit
  la threat intelligence. Les composants lourds sont activés par profils.
- Les techniques offensives sont uniquement des émulations locales contre les
  cibles du lab. Le routage vers le LAN et Internet est interdit par défaut aux
  réseaux d'attaque.
- Ce projet est pédagogique et portfolio-ready; ce n'est pas une plateforme
  de production ni un remplacement d'un audit d'architecture.

## Architecture et stack

| Domaine | Composant | Rôle |
|---|---|---|
| SIEM | Wazuh manager, indexer, dashboard | collecte, corrélation, recherche et visualisation |
| EDR/HIDS | Wazuh agents | FIM, inventaire, logs, détection endpoint et active response contrôlée |
| NDR/IDS | Suricata | inspection réseau et événements EVE JSON |
| Network visibility | Zeek | métadonnées DNS, HTTP, TLS et connexions |
| IPS | Suricata inline | profil optionnel, désactivé par défaut et limité au lab |
| Case management | TheHive | incidents, observables, tâches et timeline |
| Enrichment | Cortex | analyseurs locaux et enrichissement d'observables |
| Threat intelligence | feed MISP-compatible + CDB Wazuh | IOC du lab; serveur MISP externe en extension |
| Attack emulation | scripts et conteneur dédié | scénarios ATT&CK reproductibles et non destructifs |
| Targets | Linux endpoint + application web volontairement vulnérable | génération de télémétrie endpoint, web et réseau |
| Quality gates | ShellCheck, yamllint, Compose validation, pytest | validation statique et tests d'intégration légers |

Les images seront épinglées à des versions explicites et documentées. Aucun
tag `latest` ne sera accepté dans le chemin de démonstration.

## Profils de déploiement

- `core` : Wazuh, endpoint Linux, cible web, générateur de télémétrie.
- `network` : Suricata et Zeek.
- `cases` : TheHive et Cortex.
- `intel` : feed MISP-compatible léger; serveur MISP complet en extension externe.
- `attack` : émulateur d'attaque, lancé à la demande et jamais en daemon.
- `enterprise` : agrégation documentée de tous les profils compatibles.
- `ips` : mode inline expérimental, opt-in, avec garde-fous explicites.

## Commandes contractuelles

```bash
# Préparer une configuration locale sans secret versionné
make bootstrap

# Valider la configuration, les scripts et les règles
make validate
make test

# Démarrer et contrôler le profil minimal
make up PROFILE=core
make health PROFILE=core

# Ajouter la visibilité réseau et la gestion de cas
make up PROFILE=core,network,cases

# Exécuter une émulation précise, jamais toutes implicitement
make simulate SCENARIO=ssh-bruteforce

# Arrêter sans effacer les preuves
make down

# Effacement complet, explicite et documenté
make destroy
```

## Structure du projet

```text
compose/                 fichiers Compose par domaine et profils
config/                  configurations versionnées des produits
detections/              règles Wazuh, Suricata, Sigma et tests associés
scenarios/               scénarios ATT&CK et assertions de détection
scripts/                 bootstrap, santé, simulation et collecte de preuves
tests/                   tests statiques et d'intégration légers
docs/
  architecture/          diagrammes, flux de données et trust boundaries
  runbooks/               procédures d'exploitation
  playbooks/              réponse à incident par cas d'usage
  portfolio/              guide de démo, captures attendues et récit CV
tasks/                   plan et backlog d'implémentation
.env.example             variables publiques et placeholders uniquement
Makefile                 interface d'exploitation stable
```

## Style de code et de configuration

- Bash en mode strict, fonctions courtes, variables citées et erreurs utiles.
- YAML à deux espaces, clés stables, noms de service en `kebab-case`.
- Python réservé aux tests et outils où il apporte une valeur claire; type
  hints et fonctions pures privilégiées.
- Les IDs de scénario suivent `LAB-<domaine>-<numéro>` et chaque scénario
  référence au moins une technique MITRE ATT&CK.

```bash
#!/usr/bin/env bash
set -Eeuo pipefail

readonly scenario_id="${1:?scenario id is required}"
validate_scenario_id "$scenario_id"
run_confined_scenario "$scenario_id"
```

## Stratégie de test

### Statique

- `docker compose config` pour chaque combinaison de profils supportée.
- `shellcheck` pour tous les scripts Bash.
- `yamllint` pour Compose, configurations et règles YAML.
- Recherche automatisée de secrets, de tags `latest`, de ports exposés sans
  justification et de capacités Linux dangereuses non documentées.

### Fonctionnel

- Tests de santé HTTP/TCP avec délais bornés.
- Injection d'un événement bénin connu et assertion de sa présence dans le
  pipeline attendu.
- Tests des règles de détection sur des fixtures versionnées.
- Un smoke test du scénario principal sans dépendre d'une attaque externe.

### Manuel guidé

- Checklist de démonstration de 15 minutes.
- Captures attendues du dashboard, de l'alerte, du cas et de la timeline.
- Vérification des garde-fous réseau avant tout scénario d'émulation.

## Limites et règles d'autorisation

### Toujours faire

- Épingler les versions, vérifier les checksums quand un artefact est téléchargé.
- Garder les réseaux offensifs internes et appliquer le moindre privilège.
- Générer les secrets localement et fournir uniquement `.env.example`.
- Associer chaque détection et scénario à ATT&CK, une preuve et une procédure.
- Valider la santé et conserver les logs utiles après chaque démonstration.

### Demander avant

- Exposer un service sur une interface autre que loopback.
- Activer un IPS inline sur l'interface de l'hôte ou modifier son pare-feu.
- Télécharger/exécuter une charge offensive tierce non incluse dans le dépôt.
- Déployer hors de la machine locale ou publier des images/artefacts.
- Effacer les volumes, indices, cas ou preuves du lab.

### Ne jamais faire

- Versionner mots de passe, clés, jetons, certificats privés ou données réelles.
- Scanner Internet, le LAN, un domaine tiers ou une cible non explicitement
  autorisée.
- Exécuter un malware réel, un ransomware réel ou une persistance sur l'hôte.
- Monter `/var/run/docker.sock`, `/`, ou un répertoire sensible dans un
  conteneur d'attaque.
- Présenter le mode IPS expérimental comme un contrôle de production.

## Critères de réussite

- `make bootstrap`, `make validate` et `make test` sont documentés et
  reproductibles sur un dépôt neuf.
- Le profil `core` a une configuration Compose valide et une procédure de santé.
- Les profils lourds peuvent être activés indépendamment sans modifier les
  fichiers suivis par Git.
- Au moins trois scénarios couvrent endpoint, réseau et application web, avec
  mapping ATT&CK, événements attendus et playbook de réponse.
- Au moins cinq détections personnalisées possèdent des fixtures ou tests.
- Les secrets sont absents du dépôt et les services d'administration écoutent
  sur loopback par défaut.
- Le projet contient un diagramme d'architecture, un modèle de menace, un guide
  d'exploitation, un guide de démonstration et des formulations CV vérifiables.
- Le démarrage, l'arrêt et la collecte de preuves sont accessibles via le
  `Makefile` sans mémoriser les commandes internes.
- La documentation distingue clairement ce qui est testé automatiquement, ce
  qui nécessite des ressources élevées et ce qui reste une extension.

## Hors périmètre initial

- Haute disponibilité multi-hôte et Kubernetes.
- Ingestion de données d'entreprise réelles.
- Exploits zero-day, malware réel et tests sur des systèmes tiers.
- Garantie de performance ou de conformité pour un environnement de production.
- Endpoint Windows conteneurisé; seule l'intégration d'une VM est documentée.

## Questions à valider

1. Le nom public proposé `Enterprise SOC Lab` convient-il, ou souhaitez-vous
   une marque de portfolio particulière ?
2. Votre machine dispose-t-elle de 16 Go ou 32 Go de RAM ?
3. Préférez-vous les documents principaux en français, en anglais, ou bilingues ?
4. Validez-vous Wazuh comme SIEM/EDR central et TheHive/Cortex/MISP comme couche
   d'investigation optionnelle ?
