from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, TextAreaField, PasswordField
from wtforms.validators import DataRequired


class ArticleForm(FlaskForm):
    title = StringField("", validators=[DataRequired()], render_kw={'placeholder': "Titre de l'article"})
    # image = FileField()
    quick_description = TextAreaField("", validators=[DataRequired()], render_kw={'placeholder': "Description"})
    content = TextAreaField("", validators=[DataRequired()], render_kw={'placeholder': "Contenu"})
    submit = SubmitField('Valider')


class ConnectionForm(FlaskForm):
    username = StringField("Nom d'utilisateur", validators=[DataRequired()], render_kw={'placeholder': "username"})
    password = PasswordField("Mot de passe", validators=[DataRequired()], render_kw={'placeholder': "password"})
    submit = SubmitField('Valider')
