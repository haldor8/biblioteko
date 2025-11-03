# Début du back

Mise en place du backend :
- Mise en place du serveur flask
- Séparation des fichiers de routes entre API et routes HTML
- Routes de tests pour les getters, les requêtes post, requêtes json etc

# Diagramme de l'application

Agrandissement du diagramme de façon plus générale pour son utilisation "normale"

Séparation des permissions (hard code) entre un utilisateur authentifié (via franceconnect), un utilisateur lambda et un administrateur.

Détails sur la gestion des logs, signalements etc

Début de réflexion sur l'indexation des fichiers (l'indexation doit être gérée par nous-mêmes étant donné qu'on n'utilise pas de BDR)

Cycle de vie d'un upload qui commence à se dessiner (utilisateur authentifié -> upload -> vérification des droits d'auteur -> met à jour ou bloque l'upload)