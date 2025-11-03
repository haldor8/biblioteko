from flask import Flask

def create_app():
    app = Flask(__name__)

    # Import des Blueprints
    from app.routes.main_routes import main
    from app.api.api_routes import api

    # Enregistrement des Blueprints
    app.register_blueprint(main)
    app.register_blueprint(api, url_prefix="/api")

    return app
