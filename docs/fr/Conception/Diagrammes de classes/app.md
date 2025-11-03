classDiagram
direction LR

%% --- Acteurs principaux ---
class Utilisateur {
  +id : string
  +nom_utilisateur : string
  +email : string
  +mdp_chiffre : string
  +reputation : int
  +role : string
}

class UtilisateurAuthentifie {
  +franceconnect_id : string
  +connecte : bool
}

class Administrateur {
  +niveau_acces : string
}

UtilisateurAuthentifie --|> Utilisateur
Administrateur --|> UtilisateurAuthentifie

%% --- OCR et extraction ---
class OCRProcessor {
  +chemin_fichiers : string
  +format_entree : string
  +format_sortie : string
}

class OCRExtractor {
  +modele_LLM : string
  +version : string
}

OCRProcessor --> OCRExtractor : "utilise pour extraction de texte"

%% --- Système de filtrage, logs et panel ---
class SystemeFiltrageContenu {
  +liste_noire : list
  +api_externes : list
  +chemin_local_blacklist : string
}

class Logs {
  +chemin_fichier : string
  +type_evenement : string
  +horodatage : datetime
  +details : string
}

class PanelModeration {
  +notifications : list
  +signalements : list
}

SystemeFiltrageContenu --> Logs : "consigne violations"
Administrateur --> SystemeFiltrageContenu : "alimente blacklist"
PanelModeration --> Logs : "affiche signalements"

%% --- Livres et fichiers d'index ---
class Livre {
  +identifiant : string
  +titre_normalise : string
  +auteur : string
  +edition : string
}

class FichierIndexation {
  +titre : string
  +auteur : string
  +edition : string
  +nombre_pages : int
  +sujet : string
  +chemin_dossier : string
}

Livre --> FichierIndexation : "est décrit par"

%% --- Classe Upload ---
class Upload {
  +id : string
  +date_televersement : datetime
  +chemin_temporaire : string
  +statut : string
}

UtilisateurAuthentifie --> Upload : "effectue"
Upload --> SystemeFiltrageContenu : "analyse contenu"
Upload --> Livre : "crée ou met à jour"
OCRProcessor --> Upload : "traite fichiers uploadés"

%% --- Etat du serveur et panel admin ---
class EtatServeur {
  +utilisation_cpu : float
  +utilisation_ram : float
  +espace_disque : float
  +charge_upload : float
  +etat_reseau : string
}

EtatServeur --> PanelModeration : "informe état système"

%% --- Relations utilisateurs / système ---
Utilisateur --> Livre : "lit"
Administrateur --> PanelModeration : "supervise"
Administrateur --> Logs : "consulte"
