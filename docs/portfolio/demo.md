# Démonstration portfolio — 15 minutes

## Avant l'entretien

- Démarrer `core,network` et confirmer `make health`.
- Exécuter une fois les scénarios pour vérifier les règles attendues.
- Nettoyer uniquement les artefacts de démonstration choisis, pas les volumes.
- Préparer quatre captures: architecture, agent actif, alerte corrélée, cas final.
- Masquer `.env`, clés, noms d'utilisateur locaux et informations machine.

## Script oral

### 0–2 min — problème et architecture

« J'ai construit un SOC lab reproductible qui démontre le cycle complet: une
activité contrôlée génère de la télémétrie endpoint/réseau, Wazuh la corrèle, puis
l'analyste qualifie et transforme la preuve en incident. J'ai séparé le réseau
SOC, la cible et la gestion de cas pour rendre les frontières de confiance visibles. »

Montrer le diagramme de `docs/architecture/architecture.md` et les profils.

### 2–5 min — contrôles engineering

Montrer `compose.yaml`, sans parcourir chaque ligne:

- ports loopback;
- réseaux `internal`;
- images versionnées;
- simulateur read-only, sans capabilities ni Docker socket;
- bootstrap idempotent et secrets ignorés par Git.

Puis lancer:

```bash
make validate
make test
```

### 5–9 min — scénario réseau

```bash
make simulate SCENARIO=web-recon
```

Dans Wazuh, afficher les règles `100110/100120/100140`, puis expliquer la
corrélation Suricata (signature) + Zeek (contexte HTTP). Montrer l'événement brut,
le mapping ATT&CK et un faux positif possible.

### 9–12 min — endpoint et réponse

```bash
make simulate SCENARIO=ssh-bruteforce
make case SCENARIO=ssh-bruteforce
```

Afficher `100100`, la fenêtre de fréquence et le bundle de cas. Décrire le
playbook: qualification, recherche d'un succès, containment hypothétique et tuning.

### 12–15 min — décisions senior et limites

- L'agent conteneur est une simulation, pas un EDR de l'hôte.
- Suricata est IDS passif; l'IPS inline exige un design réseau différent.
- Cortex est omis car le socket Docker violerait le modèle de menace.
- Docker n'ayant pas été disponible dans l'environnement de construction initial,
  la validation runtime doit être présentée uniquement après exécution locale.
- Prochaine amélioration: digests/Cosign, VM Windows, retention et dashboard KPI.

## Captures attendues

1. Agent `finance-workstation-01` actif.
2. Alerte web avec signature, URI et ATT&CK.
3. Corrélation SSH `100100` avec source `198.51.100.23`.
4. Timeline/cas contenant preuves, verdict et tâches.

## Questions d'entretien à anticiper

- Pourquoi Wazuh plutôt qu'Elastic Security/Splunk?
- Pourquoi un namespace réseau partagé pour les capteurs?
- Comment réduiriez-vous les faux positifs?
- Que changeriez-vous pour une production multi-tenant?
- Comment protéger et faire tourner les secrets?
- Pourquoi ne pas monter le socket Docker pour Cortex?
