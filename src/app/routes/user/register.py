import json
import os
from pathlib import Path
from flask import Flask, request, jsonify, Blueprint, render_template, session
from datetime import datetime
from argon2 import PasswordHasher, exceptions

register = Blueprint("register", __name__, template_folder="../../templates/user")

USERS_FILE = Path(__file__).parent / "users.json"

def load_users():
    if not USERS_FILE.exists():
        return {"users": []}
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_users(data):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


@register.route("/", methods=["GET", "POST"])
def register_page():
    if request.method == "POST":
        data = request.get_json()
        ph = PasswordHasher()
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if not username or not email or not password:
            return jsonify({"error": "Champs manquants"}), 400

        users_data = load_users()

        for user in users_data["users"]:
            if user["username"] == username or user["email"] == email:
                return jsonify({"error": "Utilisateur déjà existant"}), 409

        try:
            hashed_password = ph.hash(password)
        except exceptions.HashingError:
            return jsonify({"error": "Erreur lors du hash du mot de passe"}), 500

        new_user = {
            "id": len(users_data["users"]) + 1,
            "username": username,
            "email": email,
            "password": hashed_password,
            "role": "user",
            "createdAt": datetime.utcnow().isoformat() + "Z",
            "active": True
        }

        users_data["users"].append(new_user)
        save_users(users_data)

        return jsonify({"message": "Utilisateur créé avec succès"}), 201
    return render_template("register.html")