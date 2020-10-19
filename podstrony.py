from flask import Blueprint, url_for, render_template, request, jsonify, make_response
from bazadanych import cursor, mysql
from werkzeug.utils import redirect
from forms import ConctactForms

podstronny_blueprint = Blueprint('podstronny_blueprint', __name__)

@podstronny_blueprint.route('/omnie')
def About():
    url_for('static', filename='style.css')
    return render_template("about.html", name="about")

@podstronny_blueprint.route('/kontakt',  methods=['GET', 'POST'])
def Kontakt():
    form = ConctactForms()
    wszystko_ok = False
    if request.method == "POST":
        req =request.form
        print(f'Values={req}')
        name = req["Imię"]
        email = req["E-mail"]
        sumbnit = req["Tytuł"]
        wiadomosc = req["Wiadomość"]
        missing = list()
        for key, value in req.items():
            if value == "":
                print(req.items())
                missing.append(key)
            if missing:
                print(bool(missing))
                feedback = f"Brakujące pola dla {', '.join(missing)}"
                wszystko_ok = False
                return render_template("kontakt.html", feedback=feedback)
            else:
                wszystko_ok = True
        if wszystko_ok == True:
            print("Dodawanie do bazy danych")
            conn = mysql.connect()
            cursor = conn.cursor()
            to_db = (name, sumbnit, wiadomosc, email)
            cursor.execute("INSERT INTO forms VALUES (%s, %s, %s, %s)", to_db)
            conn.commit()
            cursor.close()
            cursor = mysql.connect().cursor()
            cursor.execute("SELECT * from posty")
            data = cursor.fetchall()
            cursor.close()
        return redirect(request.url)
    return render_template("kontakt.html", form=form)