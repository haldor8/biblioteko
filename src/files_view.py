# src/app/files_view.py
import json
import re
from pathlib import Path
from datetime import datetime
from flask import Blueprint, current_app, render_template, abort

files_bp = Blueprint("files", __name__, template_folder="templates")

# Helpers that compute repo base at runtime (works whether data is at repo root or inside package)
def _repo_base() -> Path:
    # current_app.root_path -> .../path/to/src/app
    # repo root assumed to be one level above src (project root)
    return Path(current_app.root_path).parent

def _users_dir() -> Path:
    return _repo_base() / "data" / "userdat"

def _scans_perm_dir() -> Path:
    return _repo_base() / "data" / "sequestre" / "scans"

def _scans_temp_dir() -> Path:
    return _repo_base() / "data" / "temp"

def safe_read_text(p: Path, max_chars=None):
    try:
        txt = p.read_text(encoding="utf-8", errors="ignore")
        return txt if max_chars is None else txt[:max_chars]
    except Exception:
        return ""

def fmt_mtime(p: Path):
    try:
        return datetime.fromtimestamp(p.stat().st_mtime).isoformat(sep=' ', timespec='seconds')
    except Exception:
        return ""

def parse_permanent_scan(raw: str):
    parts = [line for line in raw.splitlines()]
    try:
        separators = [i for i, line in enumerate(parts) if line.strip() == '---']
        if len(separators) >= 2:
            meta_lines = parts[separators[0]+1:separators[1]]
            content_lines = parts[separators[1]+1:]
            meta = {}
            for ln in meta_lines:
                if ':' in ln:
                    k, v = ln.split(':', 1)
                    meta[k.strip()] = v.strip()
            content = "\n".join(content_lines).strip()
            return meta, content
    except Exception:
        pass
    return {}, raw.strip()

def parse_temp_scan(raw: str):
    sections = {}
    current = None
    buff = []
    for line in raw.splitlines():
        s = line.strip()
        if s.startswith('[') and s.endswith(']'):
            if current:
                sections[current] = "\n".join(buff).strip()
            current = s.strip('[]')
            buff = []
        else:
            if current:
                buff.append(line)
    if current:
        sections[current] = "\n".join(buff).strip()
    return sections

def slugify_id(value: str) -> str:
    return re.sub(r'[^A-Za-z0-9_-]', '_', value)

def read_users():
    users = []
    USERS_DIR = _users_dir()
    if not USERS_DIR.exists():
        return users
    for p in sorted(USERS_DIR.iterdir()):
        if p.suffix.lower() != '.json':
            continue
        raw = safe_read_text(p)
        try:
            parsed = json.loads(raw)
        except Exception:
            continue
        arr = parsed if isinstance(parsed, list) else [parsed]
        for u in arr:
            users.append({
                "displayed_username": u.get("displayed_username", ""),
                "email": u.get("email", ""),
                "role": u.get("role", ""),
                "reputation": u.get("reputation", 0),
            })
    return users

def group_permanent_by_book():
    books = []
    SCANS_PERM_DIR = _scans_perm_dir()
    if not SCANS_PERM_DIR.exists():
        return books
    for folder in sorted([d for d in SCANS_PERM_DIR.iterdir() if d.is_dir()]):
        pages = []
        for p in sorted(folder.iterdir()):
            if not p.is_file():
                continue
            raw = safe_read_text(p, max_chars=200_000)
            meta, content = parse_permanent_scan(raw)
            pages.append({"filename": p.name, "metadata": meta, "content": content})
        title = pages[0]["metadata"].get("title") if pages and pages[0]["metadata"] else folder.name
        preview_text = ""
        if pages:
            preview_text = "\n".join(pages[0]["content"].splitlines()[:30])
        books.append({
            "book_id": slugify_id(folder.name),
            "folder": folder.name,
            "title": title,
            "pages": pages,
            "preview": preview_text,
            "mtime": fmt_mtime(folder),
        })
    return books

def read_temp_scans():
    list_ = []
    SCANS_TEMP_DIR = _scans_temp_dir()
    if not SCANS_TEMP_DIR.exists():
        return list_
    for p in sorted(SCANS_TEMP_DIR.iterdir()):
        if not p.is_file():
            continue
        raw = safe_read_text(p, max_chars=200_000)
        sections = parse_temp_scan(raw)
        preview = sections.get("TEXT") or sections.get("Text") or sections.get("text") or ""
        sections_items = list(sections.items())
        list_.append({
            "filename": p.name,
            "id": slugify_id(p.name),
            "sections": sections_items,
            "preview": "\n".join(preview.splitlines()[:30]),
            "mtime": fmt_mtime(p),
            "size": p.stat().st_size,
        })
    return list_

# Routes (Flask versions of the Pyramid view_config endpoints)

@files_bp.route("/dashboard")
def dashboard_view():
    users = read_users()
    permanent = group_permanent_by_book()
    temp = read_temp_scans()
    stats = {
        "user_count": len(users),
        "perm_count": len(permanent),
        "temp_count": len(temp),
    }
    # pass json so templates can call json.dumps if needed
    return render_template("dashboard.html",
                           users=users,
                           permanent_scans=permanent,
                           temp_scans=temp,
                           stats=stats,
                           json=json)

@files_bp.route("/")
def home_view():
    books = group_permanent_by_book()
    sample = books[:3]
    return render_template("home.html", books_sample=sample)

@files_bp.route("/books")
def books_list_view():
    books = group_permanent_by_book()
    return render_template("books_list.html", books=books)

@files_bp.route("/books/<book_id>")
def book_detail_view(book_id):
    books = group_permanent_by_book()
    book = next((b for b in books if b["book_id"] == book_id), None)
    if not book:
        abort(404)
    full_text = "\n\n".join(p["content"] for p in book["pages"])
    return render_template("book_detail.html", book=book, full_text=full_text)
