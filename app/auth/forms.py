from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField("Nom d'utilisateur", validators=[DataRequired()], render_kw={'placeholder': "Nom d'utilisateur"})
    password = PasswordField("Mot de passe", validators=[DataRequired()], render_kw={'placeholder': "Mot de passe"})
    remember_me = BooleanField('Me garder connecté')
    submit = SubmitField('Connexion')