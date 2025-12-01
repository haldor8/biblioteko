import os
from werkzeug.utils import secure_filename

BASE_UPLOAD_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../../data/uploads/raw_files")
)

# Assure que le dossier existe
os.makedirs(BASE_UPLOAD_DIR, exist_ok=True)

def save_uploaded_file(file):
    """
    Sauvegarde un fichier uploadé dans le dossier data/uploads/raw_files/
    Retourne le chemin final + le nom du fichier.
    """
    if file.filename == "":
        raise ValueError("Aucun fichier sélectionné.")

    filename = secure_filename(file.filename)
    filepath = os.path.join(BASE_UPLOAD_DIR, filename)

    file.save(filepath)

    return filepath, filename
