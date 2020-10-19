from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class ConctactForms(FlaskForm):
    Imie = StringField(
        "Twoje imię", validators=[DataRequired("Podaj swoje imię")]
    )
    Email = StringField("Twoje e-mail", validators=[DataRequired()])
    submits = StringField("Tytuł wiadomości", validators=[DataRequired()])
    messege = StringField("Wiadomość", validators=[DataRequired()])


class Log(FlaskForm):
    Login = StringField(
        "Twoje imię", validators=[DataRequired("Podaj swoje imię")]
    )
    Passsword = StringField("Twoje e-mail", validators=[DataRequired()])
