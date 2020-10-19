from flask import Flask
from flaskext.mysql import MySQL


app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'wpisy'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.secret_key = "329743bjshads93982472463246sas"
mysql.init_app(app)
cursor = mysql.connect().cursor()



spr = cursor.execute("SELECT * FROM `posty`")
data = cursor.fetchall()




