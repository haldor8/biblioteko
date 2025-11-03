from flask import Blueprint, jsonify, request

api = Blueprint("api", __name__)

@api.route("/ping")
def ping():
    return jsonify({"status": "ok", "message": "pong"})

@api.route("/echo", methods=["POST"])
def echo():
    data = request.get_json(silent=True) or {}
    return jsonify({"received": data})
