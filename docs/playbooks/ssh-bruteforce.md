# Playbook — échecs SSH répétés

**Détection:** règles Wazuh `5710` et `100100`

**ATT&CK:** T1110.001 Password Guessing

**Sévérité initiale:** haute

## Qualification

1. Confirmer au moins cinq échecs depuis la même `srcip` en 60 secondes.
2. Identifier comptes ciblés, agent, première/dernière occurrence et éventuel
   succès postérieur.
3. Vérifier si l'IP appartient à un scanner/outil autorisé.

## Investigation

- Rechercher les événements SSH ±15 minutes autour de l'alerte.
- Corréler avec inventaire, VPN, bastion et logs réseau disponibles.
- Chercher création de compte, élévation, commande distante ou FIM après succès.

## Containment simulé

- En entreprise: bloquer temporairement la source au contrôle d'accès approprié,
  désactiver/réinitialiser le compte compromis et préserver les sessions.
- Dans ce lab: ne modifier aucun pare-feu hôte; documenter l'action hypothétique.

## Clôture

Verdict, périmètre, compte/IP, preuve brute, règle déclenchée, actions et tuning.
Un succès après les échecs augmente la sévérité à critique/high selon le contexte.
