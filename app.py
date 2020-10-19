from flask import Flask, render_template, url_for, session, request
from werkzeug.utils import redirect
from bazadanych import mysql
from podstrony import podstronny_blueprint
from dodawanie_wpisów import posty_blueprint
from logowanie import admin_blueprint
from log import log_blueprint

app = Flask(__name__)
app.secret_key = "development key"


@app.route("/")
def Home():
    url_for("static", filename="style.css")
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT * from posty")
    data = cursor.fetchall()
    cursor.close()
    return render_template("index.html", name="index", data=data)


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("Home"))


@app.route("/wpis/<pk>")
def Post(pk):
    pk = pk
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT * from posty")
    data = cursor.fetchall()
    cursor.close()
    return render_template("post.html", pk=pk, data=data)


app.register_blueprint(podstronny_blueprint)
app.register_blueprint(posty_blueprint)
app.register_blueprint(admin_blueprint)
app.register_blueprint(log_blueprint)

if __name__ == "__main__":
    app.run(debug=True)
