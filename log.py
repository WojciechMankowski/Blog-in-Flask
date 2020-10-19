from flask import (
    url_for,
    session,
    redirect,
    Blueprint,
    render_template,
    request,)
from hashlib import md5
from bazadanych import mysql

log_blueprint = Blueprint("log_blueprint", __name__)


@log_blueprint.route("/login", methods=["GET", "POST"])
def login():
    error = None
    error_register = None
    success_register = None

    class ServerError(Exception):
        pass

    if request.method == "POST":
        if request.form["action"] == "login":
            try:
                conn = mysql.connect()
                cur = conn.cursor()
                username_form = request.form["username"]
                rezult = cur.execute(
                    "SELECT * FROM users WHERE login ='" + username_form + "'"
                )
                password_form = request.form["password"]
                print(md5(password_form.encode("utf-8")).hexdigest())
                password_hash = md5(password_form.encode("utf-8")).hexdigest()
                rezult_h = cur.execute(
                    "SELECT * FROM users WHERE pass ='" + password_hash + "'"
                )
                if rezult != 1 and rezult_h != 1:
                    raise ServerError("Błędna nazwa użytkownika lub hasło")
                elif rezult == 1 and rezult_h == 1:
                    session["username"] = request.form["username"]
                    return redirect(url_for("logowanie_blueprint.Panel_admina"))
            except ServerError as e:
                error = str(e)

    return render_template("log.html", error=error)
