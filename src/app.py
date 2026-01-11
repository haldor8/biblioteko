from app import create_app
from flask import session, redirect, url_for, request
from flask import abort

app = create_app()
app.secret_key = "une_cle_super_secrete"


@app.before_request
def check_authentication():

    PUBLIC_ROUTES = {
        'main.login.login_page',
        'main.register.register_page',
        'static'
    }

    endpoint = request.endpoint

    if endpoint is None:
        return

    if endpoint in PUBLIC_ROUTES or endpoint.startswith('static'):
        return

    if 'user_id' not in session:
        return redirect(url_for('main.login.login_page'))

    if 'admin' in endpoint:
        if session.get('role') != 'admin':
            abort(403)


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
    # from app.views import views_bp

    app.register_blueprint(main)
    app.register_blueprint(api, url_prefix="/api")
    # app.register_blueprint(views_bp)  # <-- your routes: /, /books, /book/<id>, /dashboard

    return app
    