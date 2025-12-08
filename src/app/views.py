# src/app/views.py

import os
from pathlib import Path
from flask import Blueprint, render_template, abort, current_app

views_bp = Blueprint("views", __name__, template_folder="templates")

# -----------------------
# helper directory locators
# -----------------------

def _package_dir() -> Path:
    return Path(__file__).resolve().parent

def _books_dir() -> Path:
    # locate book md files flexibly
    repo_root = Path(current_app.root_path).parent  # /repo/src/app -> /repo

    # common directories where your books may be saved
    candidates = [
        repo_root / "data" / "books",
        repo_root / "data" / "scans",
        _package_dir() / "books",
    ]

    for c in candidates:
        if c.exists():
            return c

    return _package_dir() / "books"


def _read_lines(path):
    try:
        with open(path, encoding="utf-8") as f:
            return f.readlines()
    except Exception:
        return []


# -----------------------
# BOOK LOADER
# -----------------------

def getAllBooks():
    books_dir = _books_dir()
    books = []

    if not books_dir.exists():
        return books

    for idx, folder in enumerate(sorted(os.listdir(books_dir)), start=1):
        folder_path = books_dir / folder
        if folder_path.is_dir():
            md_files = [f for f in os.listdir(folder_path) if f.endswith(".md")]

            preview = ""
            page_count = len(md_files)

            if md_files:
                first_md_path = folder_path / sorted(md_files)[0]
                lines = _read_lines(first_md_path)

                delimiter = 0
                content_lines = []

                for line in lines:
                    if line.strip() == "---":
                        delimiter += 1
                        continue
                    if delimiter >= 2:
                        content_lines.append(line.strip())

                preview = " ".join([l for l in content_lines if l][:3])

            books.append({
                "book_id": idx,
                "title": folder,
                "preview": preview,
                "page_count": page_count,
                "pdf_file": f"/books/{folder}/{folder}.pdf"
            })

    return books


# -----------------------
# ROUTES
# -----------------------

@views_bp.route("/")
def home_view():
    books = getAllBooks()
    return render_template("home.html", books_list=books)


@views_bp.route("/books")
def books_view():
    books = getAllBooks()
    return render_template("books.html", books_list=books)


@views_bp.route("/book/<int:book_id>")
def book_detail_view(book_id):
    books = getAllBooks()
    book = next((b for b in books if b["book_id"] == book_id), None)

    if not book:
        abort(404)

    folder = book["title"]
    folder_path = _books_dir() / folder
    pages = []

    if folder_path.exists():
        md_files = sorted([f for f in os.listdir(folder_path) if f.endswith(".md")])

        for md in md_files:
            md_path = folder_path / md
            lines = _read_lines(md_path)

            delimiter = 0
            output_lines = []

            for line in lines:
                if line.strip() == "---":
                    delimiter += 1
                    continue
                if delimiter >= 2:
                    output_lines.append(line.rstrip())

            pages.append({
                "filename": md,
                "content": "\n".join(output_lines).strip()
            })

    book["pages"] = pages
    full_text = "\n\n".join(p["content"] for p in pages)

    return render_template("bookdetails.html", book=book, folder=folder, full_text=full_text)


@views_bp.route("/dashboard")
def dashboard_view():
    users = [
        {"displayed_username": "shubham", "email": "shubam.rbhattarai@gmail.com", "role": "admin", "reputation": 120},
        {"displayed_username": "bob", "email": "bob@example.com", "role": "user", "reputation": 45},
    ]

    permanent_scans = [
        {
            "book_id": 101,
            "title": "Invoice_2024.pdf",
            "mtime": "2025-01-10 12:34",
            "folder": "/scans/permanent",
            "preview": "First lines of OCR text...",
            "pages": [
                {"filename": "page001.png", "content": "Page 1 text..."},
                {"filename": "page002.png", "content": "Page 2 text..."},
            ],
        }
    ]

    temp_scans = [
        {
            "id": 201,
            "filename": "upload_tmp_1.pdf",
            "mtime": "2025-12-01 09:00",
            "preview": "Temporary scan preview...",
            "sections": [
                ("Sec 1", "Content A"),
                ("Sec 2", "Content B")
            ],
        }
    ]

    stats = {
        "user_count": len(users),
        "perm_count": len(permanent_scans),
        "temp_count": len(temp_scans),
    }

    return render_template(
        "dashboard.html",
        stats=stats,
        users=users,
        permanent_scans=permanent_scans,
        temp_scans=temp_scans,
    )
