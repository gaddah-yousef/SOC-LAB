# Formulations CV et profil

N'utilisez que les formulations correspondant à une démonstration que vous avez
réellement exécutée. Remplacez les métriques après vos propres mesures.

## Français

### Projet

**Enterprise SOC Lab — Detection Engineering & Incident Response**

- Conçu une architecture SOC Docker segmentée intégrant Wazuh SIEM/HIDS,
  Suricata, Zeek, une cible OWASP et TheHive optionnel.
- Développé six règles de détection versionnées et trois scénarios MITRE ATT&CK
  reproductibles couvrant credential access, reconnaissance et persistance.
- Automatisé génération de secrets, certificats, contrôles de santé, validation
  de politiques, collecte de preuves et création de bundles d'incident.
- Appliqué le moindre privilège: réseaux internes, services administratifs sur
  loopback, simulateur sans capabilities, aucun montage du socket Docker.
- Rédigé threat model, runbooks et playbooks de réponse avec hypothèses de faux
  positifs, critères d'escalade et limites production.

### Compétences associées

`Wazuh` · `SIEM` · `EDR/HIDS` · `Suricata` · `Zeek` · `Docker Compose` ·
`MITRE ATT&CK` · `Detection Engineering` · `Incident Response` · `Threat Modeling`

## English

**Enterprise SOC Lab — Detection Engineering & Incident Response**

- Designed a segmented Docker SOC architecture integrating Wazuh SIEM/HIDS,
  Suricata, Zeek, an OWASP target and an optional TheHive case layer.
- Built six version-controlled detections and three reproducible MITRE ATT&CK
  simulations across credential access, reconnaissance and persistence.
- Automated secret/certificate bootstrap, health checks, policy validation,
  evidence capture and analyst-ready incident bundles.
- Enforced least privilege with internal networks, loopback-bound admin services,
  capability-free attack simulation and no Docker socket mounts.
- Produced a repository-grounded threat model, operations runbook and incident
  playbooks with escalation criteria and production limitations.

## Pitch de 30 secondes

« Ce projet ne se limite pas à lancer Wazuh. J'ai construit un chemin de preuve
complet: scénario ATT&CK confiné, télémétrie endpoint et réseau, détection testée,
triage et dossier d'incident. J'ai aussi traité le lab comme une vraie plateforme:
secrets, frontières de confiance, contrôles CI, runbooks et limites explicites. »

## Preuves à lier sur GitHub

- diagramme d'architecture;
- fichier de règles et catalogue de détections;
- résultats CI;
- capture d'une alerte et d'un cas sans secret;
- courte vidéo de la démo;
- threat model et choix de ne pas exposer le socket Docker.
