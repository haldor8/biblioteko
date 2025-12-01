from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.upload.api import save_uploaded_file

upload = Blueprint(
    "upload",
    __name__,
    template_folder="../../templates/upload"
)

@upload.route("/", methods=["GET"])
def upload_form():
    return render_template("upload_form.html")


@upload.route("/submit", methods=["POST"])
def upload_submit():
    if "file" not in request.files:
        flash("Aucun fichier reçu.", "error")
        return redirect(request.url)

    file = request.files["file"]

    try:
        filepath, filename = save_uploaded_file(file)
        flash(f"Fichier '{filename}' uploadé avec succès !", "success")
        return redirect(url_for("upload.upload_form"))

    except Exception as e:
        flash(str(e), "error")
        return redirect(url_for("upload.upload_form"))
