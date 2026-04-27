from flask import Blueprint,render_template

user_profile = Blueprint("profile",__name__)

@user_profile.route("/profile")
def profile():
    return render_template("profile.html")
