from flask import Blueprint, session, redirect

logout = Blueprint("logout", __name__, template_folder="../../templates/user")


@logout.route("/")
def logout_page():
    session.clear()
    return redirect("/")