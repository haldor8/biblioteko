# upload_handler.py
import os
from werkzeug.utils import secure_filename
from app.upload.metadata_extractor import MetadataExtractor
from app.upload.pdf_utils import pdf_to_images
from cli.moderate import check_book_copyright
# from admin_module import flag_book_for_review

import subprocess
import sys

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]  # src/
CLI_DIR = BASE_DIR / "cli"

OCR_SCRIPT = CLI_DIR / "ocr.py"
EXPORT_MD_SCRIPT = CLI_DIR / "export_md.py"

RAW_OCR_FILES_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../../data/uploads/temp")
)

BASE_UPLOAD_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../../data/uploads/raw_files")
)

os.makedirs(BASE_UPLOAD_DIR, exist_ok=True)

ALLOWED_PDF_EXT = {".pdf"}
ALLOWED_IMG_EXT = {".jpg", ".jpeg", ".png", ".webp"}


def save_uploaded_file(file):
    if file.filename == "":
        raise ValueError("Aucun fichier sélectionné.")

    filename = secure_filename(file.filename)
    ext = os.path.splitext(filename)[1].lower()

    # Read bytes BEFORE saving
    file_bytes = file.read()
    file.seek(0)

    # -------------------------
    # Handle PDF → split pages
    # -------------------------
    if ext in ALLOWED_PDF_EXT:
        pages_images = pdf_to_images(file_bytes, max_pages=5)

        if not pages_images:
            raise ValueError("Impossible de lire les pages PDF.")

        # Extract metadata from first pages
        metadata_extractor = MetadataExtractor()
        book_metadata = metadata_extractor.extract_metadata(pages_images)

    # -------------------------
    # Handle regular images
    # -------------------------
    elif ext in ALLOWED_IMG_EXT:
        metadata_extractor = MetadataExtractor()
        book_metadata = metadata_extractor.extract_metadata([file_bytes])

    else:
        raise ValueError("Format non supporté (PDF ou image seulement).")

    if not isinstance(book_metadata, dict):
        raise ValueError("Impossible d'extraire les métadonnées du livre.")

    # Ensure required fields exist
    if not book_metadata.get("title"):
        raise ValueError("Aucun titre détecté dans les métadonnées.")

    # ------------------------------------
    # Copyright check
    # ------------------------------------
    is_copyrighted = check_book_copyright(book_metadata)

    if is_copyrighted:
        return None, f"Book '{book_metadata['title']}' flagged for admin review (copyrighted)."

    # ------------------------------------
    # Save file to disk
    # ------------------------------------
    filepath = os.path.join(BASE_UPLOAD_DIR, filename)
    file.save(filepath)

    if not is_copyrighted:
    # Begin text extraction and stuff
        subprocess.run(
            [
                sys.executable,
                str(OCR_SCRIPT),
                filepath,          # PDF ou image uploadée
                "--limit", "5",
                "--engine", "gemini",
            ],
            check=True
        )

        subprocess.run(
            [
                sys.executable,
                str(EXPORT_MD_SCRIPT),
                "--folder",
                RAW_OCR_FILES_DIR,
            ],
            check=True
        )



    return filepath, filename
