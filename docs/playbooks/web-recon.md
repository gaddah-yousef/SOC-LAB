# Playbook — reconnaissance et chemin web sensible

**Détection:** Suricata `900001/900002`, Wazuh `100110/100120`, Zeek `100140`

**ATT&CK:** T1595.002 et T1190

**Sévérité initiale:** moyenne à haute

## Qualification

1. Comparer timestamp, IP, URI, méthode, status et user-agent entre Suricata et Zeek.
2. Confirmer que la destination est `web-target` et que le trafic vient du réseau lab.
3. Distinguer scan autorisé, navigation normale et tentative d'exploitation.

## Investigation

- Examiner séquence d'URI, volume, codes HTTP et téléchargements.
- Chercher erreurs applicatives, création de session et changement d'état.
- Vérifier s'il existe un événement endpoint correspondant.

## Containment simulé

- En entreprise: WAF/rate limit, blocage source, isolation application et capture
  des logs avant rotation.
- Dans le lab: arrêter uniquement le scénario si nécessaire; ne jamais lancer un
  scan sur une URL fournie par l'utilisateur.

## Clôture

Conserver EVE JSON, `http.log`, chronologie, hypothèse d'objectif et recommandation
de tuning. Une preuve d'exécution de code ou d'accès aux données élève la priorité.
