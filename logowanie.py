from hashlib import md5

from flask import render_template, url_for, session, request, Blueprint
from werkzeug.utils import redirect
from forms import ConctactForms
from bazadanych import mysql

admin_blueprint = Blueprint('logowanie_blueprint', __name__)

@admin_blueprint.route("/admin", methods=['GET', 'POST'])
@admin_blueprint.route('/post/dodawanie', methods=['GET', 'POST'])
def Add_post():
    url_for('static', filename='style.css')
    form = ConctactForms()
    wszystko_ok = False
    if request.method == "POST":
        req =request.form
        title = req["Tytuł"]
        autor = req["Autor"]
        data = req["Data"]
        zajawka = req["Zajawka"]
        body_post = req["Treść"]
        img = req["IMG"]
        missing = list()
        for key, value in req.items():
            if value == "":
                missing.append(key)
            if missing:
                feedback = f"Brakujące pola dla {', '.join(missing)}"
                wszystko_ok = False
                return render_template("kontakt.html", feedback=feedback)
            else:
                wszystko_ok = True
        if wszystko_ok == True:
            print("Dodawanie do bazy danych")
            conn = mysql.connect()
            cursor = conn.cursor()
            to_db = (title, autor, data, zajawka, body_post, img)
            print(len(to_db))
            cursor.execute("INSERT INTO posty VALUES (%s, %s, %s, %s, %s, %s)", to_db)
            conn.commit()
        return redirect(request.url)
    return render_template("dodawanie_wpsiu.html")

@admin_blueprint.route('/paneladmina', methods=['GET', 'POST'])
def Panel_admina():
    conn = mysql.connect()
    cursor = conn.cursor()
    if request.method == "POST":
        title = request.form["dalet_title"]
        cursor.execute("DELETE from posty where title='" + title + "'")
    cursor.execute("SELECT * from posty")
    data = cursor.fetchall()
    conn.commit()
    cursor.close()
    return render_template("userHome.html", data=data)

@admin_blueprint.route("/paneladmina/users", methods=['GET', 'POST'] )
def Add_users():
    if request.method == 'POST':
        class ServerError(Exception):pass
        if request.form["action"] == "register":
            try:
                conn = mysql.connect()
                cur = conn.cursor()
                name_form = request.form['name']
                username_form = request.form['user']
                password_form = request.form['pass']
                hash_password = md5(password_form.encode('utf-8')).hexdigest()
                to_db = ("", username_form, password_form, name_form)
                cur.execute("SELECT COUNT(1) FROM users WHERE login = '" + username_form + "'")
                if cur.fetchone()[0]:
                    name_error = ('Nazwa uzytkownika zajęta')
                    return render_template("add_user.html", error_register=name_error, success_register=success_register)

                else:
                    cur.execute("INSERT INTO users VALUES (%s, %s, %s, %s)", to_db)
                    conn.commit()
                    success_register = "Zarejestrowałeś się!"

            except ServerError as e:
                error_register = str(e)
    return render_template("add_user.html")
@admin_blueprint.route("/paneladmina/forms", methods=['GET', 'POST'] )
def Forms_kontatkt():
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT * from forms")
    data = cursor.fetchall()
    return render_template("forms_kontakt.html", data=data)