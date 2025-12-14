from flask import Blueprint

logout = Blueprint("logout", __name__, template_folder="../../templates/user")


@logout.route("/logout")
def logout():
    session.clear()
    return redirect("/")