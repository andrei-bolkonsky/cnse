from flask import Flask, render_template, session, redirect, url_for, flash
from weather_utils import get_current_conditions, get_hourly_conditions
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, TextAreaField, PasswordField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hardtoguesskey'

moment = Moment(app)


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


@app.route('/')
def index():
    weather_data = get_current_conditions()
    data = get_hourly_conditions()
    return render_template('index.html', weather_data=weather_data, data=data)


@app.route('/test')
def test():
    data = get_hourly_conditions()
    return render_template('test.html', data=data)


@app.route('/admin', methods=['GET', 'POST'])
def create_article():
    form = ArticleForm()
    if form.validate_on_submit():
        session['article_title'] = form.title.data
        session['article_descr'] = form.quick_description.data
        session['article_content'] = form.content.data
        form.title.data = ''
        form.content.data = ''
        form.quick_description.data = ''
        return redirect(url_for('create_article'))
    return render_template('article_creation.html',
                           form=form,
                           article_title=session.get('article_title'),
                           article_descr=session.get('article_descr'),
                           article_content=session.get('article_content'))

@app.route('/login', methods=['GET', 'POST'])
def connection():
    form = ConnectionForm()
    if form.validate_on_submit():
        old_username = session.get('username')
        if old_username is not None and old_username != form.username.data:
            flash(f'Looks like you are not {old_username} anymore!')
        session['username'] = form.username.data
        session['password'] = form.password.data
        form.username.data = ''
        form.password.data = ''
        return redirect(url_for('connection'))
    return render_template('login.html',
                           form=form,
                           username=session.get('username'),
                           password=session.get('password'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
