from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask

def create_app(config_object=None):
    app = Flask(__name__, template_folder="templates", static_folder="static")

    if config_object:
        app.config.from_object(config_object)

    # existing project blueprints
    from app.routes.main_routes import main
    from app.api.api_routes import api

    # your converted blueprint
    from app.views import views_bp

    app.register_blueprint(main)
    app.register_blueprint(api, url_prefix="/api")
    app.register_blueprint(views_bp)  # <-- your routes: /, /books, /book/<id>, /dashboard

    return app
    