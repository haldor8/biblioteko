# Biblioteko

Biblioteko is a **Flask-based web application** designed to manage, process, and digitize books using OCR and Large Language Models (LLMs). It provides both a web interface and an API, along with CLI tools for offline processing.

The project focuses on:
- Book file uploads and management
- OCR extraction from scanned books (PDFs/images)
- Post-processing and formatting using LLMs (Gemini, Mistral, etc.)
- Structured storage of book data

---

## Project Structure

```
biblioteko/
│
├── data/
│   └── sequestre/
│       └── scans/
│           └── <book_name>/
│               └── <book_name>_p<number>
│
├── uploads/
│   └── raw_files/
│
├── src/
│   ├── app.py
│   ├── app/
│   │   ├── api/
│   │   ├── domain/
│   │   ├── infra/
│   │   ├── routes/
│   │   │   ├── upload/
│   │   │   └── user/
│   │   ├── templates/
│   │   └── upload/
│   │
│   └── cli/
│       ├── ocr.py
│       ├── export_md.py
│       └── format_small_book.py
│
├── poetry.lock
├── pyproject.toml
└── README.md
```

---

## Data & File Handling

### `uploads/raw_files/`
Temporary storage for **raw uploaded files**:
- PDFs
- Images
- Archives

These files are processed before being structured into the `data/` directory.

### `data/sequestre/scans/`
Stores **processed and extracted book pages**.

Structure:
```
data/sequestre/scans/<book_name>/<book_name>_p<number>
```

- One directory per book
- One file per page
- Used during OCR and post-processing

---

## Flask Application

### Entry Point

The application starts from:

```
src/app.py
```

Key features:
- Flask application factory (`create_app`)
- Blueprint-based routing
- Session-based authentication
- Global authentication guard using `before_request`

Unauthenticated users are redirected to the login page.

### Blueprints

- **Main routes**: Web interface (login, register, uploads, dashboards)
- **API routes**: JSON endpoints under `/api`

---

## CLI Tools

The `src/cli/` directory contains command-line utilities for offline processing.

### `ocr.py`
- Sends scanned book pages to an LLM
- Extracts raw text and metadata

### `export_md.py`
- Converts OCR output into structured Markdown
- Uses an LLM for formatting and cleanup

### `format_small_book.py`
- Image preprocessing utility
- Cropping and zooming to improve OCR quality

---

## Dependencies

Dependencies are managed with **Poetry**.

- https://python-poetry.org/docs/

All dependencies are defined in `pyproject.toml`.

---

## Installation

### Prerequisites

- Python 3.10+ (recommended)
- Poetry

### Setup

Start in the root folder `biblioteko`.

```bash
# Create virtual environment (if not already done)
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# Linux / macOS
source venv/bin/activate

# Install dependencies (must be inside the venv)
poetry install
```

---

## Running the Application

```bash
cd src
python app.py
```

By default, the application runs in **debug mode**.

---

## Authentication

- Session-based authentication
- `user_id` stored in Flask session
- All routes are protected by default except login, register, and static assets