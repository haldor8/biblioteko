from flask import Blueprint, render_template
main = Blueprint("main", __name__, template_folder="../templates")


@main.route("/")
def index():
    return render_template("index.html")

@main.route("/hello/<name>")
def hello(name):
    return f"Bonjour, {name}!"

from app.routes.upload.routes import upload
main.register_blueprint(upload, url_prefix="/upload")
from app.routes.user.login import login
from app.routes.user.register import register
from app.routes.user.logout import logout
main.register_blueprint(login, url_prefix="/login")
main.register_blueprint(register, url_prefix="/register")
main.register_blueprint(logout, url_prefix="/logout")
