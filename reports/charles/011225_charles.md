# Répartitions des tâches

Nous avons commencé à nous répartir le travail.

Nous avons identifié 3 grands axes majeurs : l'interface (UI), la gestion d'utilisateur et la gestion des fichiers.

# Architecture

Pour l'architecture, nous avons divisé le back en API et en routes (pour le HTML).

Nous avons choisit de séparer les routes dans des sous-fichiers et sous-dossiers et de les garder simple (grand max un appel de fonction, un retour de données style json/html et à la limite un try/catch).

Le plus gros du code doit être dans des sous-fichiers/dossiers et doivent être résumés par une fonction "interface".

# Gestion des fichiers

Pour la gestion des fichiers, étant donné que nous utilisons git, nous avons choisi de stocker les mots de passe hashés dans un fichier quelconque et d'ajouter un salt par la suite dans le .env pour renforcer la sécurité.

Pour les mots de passe, j'ai recommandé argon2id pour le rapport performance/qualité du hash et d'absolument éviter le md5 comme la peste.

## Structure des fichiers

Pour développer en parallèle, nous avons décidé de prendre une structure de fichiers précise.

La liste des utilisateurs sera un gros json stocké dans `data/userdat/`. Nous devons nous baser sur franceconnect (stockage des informations décentralisé) mais pour un MVP on fait juste un login simple.
```json
[
  {
    "displayed_username": "...",
    "email" : "...",            // Must be unique
    "hashed_password": "...",
    "role" : "...",
    "reputation" : 0123456789
  },
  {
    "displayed_username": "...",
    "email" : "...",            // Must be unique
    "hashed_password": "...",
    "role" : "...",
    "reputation" : 0123456789
  }
]
```

Ensuite nous avons la structure des scans.

Les scans "permanents" dans `data/sequestre/scans/<un dossier par oeuvre>/page<1-2-3-4-...>`

Avec ce contenu :
```
---
METADATAS
---
CONTENT
```

Et les fichiers temporaires (output brut de l'OCR) dans `data/temp`

Avec ce contenu :
```
[METADATAS]
...

[TEXT]
...
```

# Travail réalisé

Pour ma part j'ai commencé l'upload de fichiers et j'ai commencé à fouiller où mettre les points de tests pour vérifier les droits d'auteur etc.

# Travail à faire

Créer un formulaire pour lancer l'OCR et l'export en markdown depuis un LLM.