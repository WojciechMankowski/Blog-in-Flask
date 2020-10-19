from flask import render_template, request, Blueprint
from bazadanych import mysql

posty_blueprint = Blueprint('posty_blueprint', __name__)

@posty_blueprint.route("/posty", methods=['POST', 'GET'])
def database_posts():
    if request.method == 'POST':
        name = request.form['tytul']
        print(name)
        author = request.form['autor']
        data = request.form['data']
        zaj = request.form['zaj']
        content = request.form['tresc']
        img = request.form['img']
        conn = mysql.connect()
        cursor = conn.cursor()
        to_db = (name, author, data , zaj, content, img)
        cursor.execute("INSERT INTO posty VALUES (%s, %s, %s, %s,  %s, %s)", to_db)
        conn.commit()
        cursor.close()
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT * from posty")
    data = cursor.fetchall()
    cursor.close()
    return render_template('dodawanie_wpsiu.html', data = data)



