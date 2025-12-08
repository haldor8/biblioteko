from flask import Blueprint, render_template, request, redirect, url_for, session
import json
import os
from argon2 import PasswordHasher, exceptions

login = Blueprint("login", __name__, template_folder="../../templates/user")

def load_users():
    """Charge le fichier JSON contenant les utilisateurs."""
    file_path = os.path.join(os.path.dirname(__file__), "users.json")

    with open(file_path, "r") as f:
        data = json.load(f)

    return data["users"]

@login.route("/" , methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        ph = PasswordHasher()
        username = request.form.get("username")
        password = request.form.get("password")
        users = load_users()
        # Vérification
        for user in users:
            if user["username"] == username:
                stored_hash = user["password"]

                try:
                    ph.verify(stored_hash, password)
                    session['user_id'] = user["id"]
                    session['username'] = user['username']
                    return f"Bienvenue {username} — authentification réussie !"
                except exceptions.VerifyMismatchError:
                    return render_template("login.html", error="Mot de passe incorrect.")
                except Exception as e:
                    return render_template("login.html", error="Erreur : hash invalide.")

        # Utilisateur inconnu
        return render_template("login.html", error="Utilisateur introuvable.")

    return render_template("login.html")