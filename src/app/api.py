from flask import Blueprint, jsonify

api = Blueprint('api', __name__, template_folder="api")

@api.route('/ping')
def ping():
    return jsonify({"message": "pong"})
