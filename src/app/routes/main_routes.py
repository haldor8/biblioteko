from flask import Blueprint, render_template

main = Blueprint("main", __name__, template_folder="../templates")

@main.route("/")
def index():
    return render_template("index.html")

@main.route("/hello/<name>")
def hello(name):
    return f"Bonjour, {name}!"
