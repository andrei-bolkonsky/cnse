from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import DataRequired


class ArticleForm(FlaskForm):
    title = StringField("", validators=[DataRequired()], render_kw={'placeholder': "Titre de l'article"})
    # image = FileField()
    quick_description = TextAreaField("", validators=[DataRequired()], render_kw={'placeholder': "Description"})
    content = TextAreaField("", validators=[DataRequired()], render_kw={'placeholder': "Contenu"})
    submit = SubmitField('Valider')
