# Playbook — artefact de persistance surveillé

**Détection:** Wazuh FIM `554` et règle `100130`

**ATT&CK:** T1546 Event Triggered Execution

**Sévérité initiale:** moyenne

## Qualification

1. Confirmer chemin, hash, propriétaire, permissions et heure de création.
2. Établir si le changement provient d'un déploiement approuvé.
3. Vérifier si le contenu est exécutable ou seulement une configuration inerte.

## Investigation

- Rechercher processus parent, commandes, connexions et modifications voisines.
- Comparer le hash à une baseline et chercher le même artefact sur d'autres hôtes.
- Corréler avec événements d'authentification et alertes réseau.

## Containment simulé

- En entreprise: isoler l'hôte, neutraliser le mécanisme après collecte, révoquer
  les identifiants associés et rechercher la cause racine.
- Dans le lab: préserver le fichier jusqu'à création du bundle de cas, puis le
  supprimer manuellement si la démonstration doit être rejouée.

## Clôture

Documenter provenance, hash, comportement attendu, étendue, remédiation et besoin
de tuning. Ne jamais supprimer une preuve réelle avant acquisition forensique.
