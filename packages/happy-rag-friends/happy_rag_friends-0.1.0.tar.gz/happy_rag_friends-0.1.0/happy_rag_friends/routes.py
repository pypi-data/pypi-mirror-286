from flask import Blueprint, render_template

bp = Blueprint("routes", __name__)


@bp.route("/")
@bp.route("/index")
def home():
    return render_template("pages/home.html")


@bp.route("/about")
def about():
    return render_template("pages/about.html")


@bp.route("/advisor-settings")
def advisor_settings():
    return render_template("pages/advisor-settings.html")


@bp.route("/ask-a-question")
def ask_a_question():
    return render_template("pages/ask-a-question.html")


@bp.route("/general-settings")
def general_settings():
    return render_template("pages/general-settings.html")
