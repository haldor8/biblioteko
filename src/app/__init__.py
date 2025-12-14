from flask import Flask
import os

def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    # Import des Blueprints
    
    from app.api.api_routes import api
    from app.views import views_bp   # <-- your converted code
    from app.routes.main_routes import main
    # Enregistrement des Blueprints
    
    app.register_blueprint(main, url_prefix="/home")
    app.register_blueprint(api, url_prefix="/api")
    app.register_blueprint(views_bp)  # <-- register your Pyramid features

    return app
