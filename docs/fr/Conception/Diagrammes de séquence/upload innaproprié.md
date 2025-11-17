sequenceDiagram
    autonumber

    participant U as Utilisateur
    participant UP as Upload
    participant OCR as OCRProcessor
    participant EXT as OCRExtractor
    participant SF as SystemeFiltrageContenu
    participant LOG as Logs
    participant ADM as Administrateur
    participant PM as PanelModeration

    %% 1. Téléversement
    U ->> UP: Téléverse une image numérisée
    UP ->> OCR: Envoie fichier pour traitement
    OCR ->> EXT: Extraction du texte / analyse LLM
    EXT -->> OCR: Retour texte et métadonnées
    OCR -->> UP: Résultat OCR

    %% 2. Filtrage de contenu
    UP ->> SF: Analyse du contenu extrait
    SF ->> SF: Détection contenu explicite / haineux
    SF ->> LOG: Enregistre violation
    SF -->> UP: Téléversement bloqué

    %% 3. Notification administration
    SF ->> PM: Création signalement + extrait contenu
    PM ->> ADM: Notification administrateur
    ADM ->> LOG: Consultation rapport et détails
    ADM -->> PM: Action modération (avertissement / suspension)

    %% 4. Retour utilisateur
    PM ->> U: Avertissement ou suspension selon gravité
