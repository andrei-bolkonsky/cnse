import os
from flask import Flask, render_template, session, redirect, url_for, flash
from weather_utils import get_current_conditions, get_hourly_conditions
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, TextAreaField, PasswordField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hardtoguesskey'
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
moment = Moment(app)


# FORMS
#######
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


# DB
####
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)


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
        session['username'] = form.username.data
        session['password'] = form.password.data
        form.username.data = ''
        form.password.data = ''
        if old_username is not None and old_username != session['username']:
            flash(f"On dirait que vous n'êtes plus {old_username} !")
        known_user = User.query.filter_by(username=session['username']).first()
        if known_user is None:
            new_user = User(username=session['username'])
            db.session.add(new_user)
            db.session.commit()
            session['known'] = False
        else:
            session['known'] = True
        return redirect(url_for('connection'))
    return render_template('login.html',
                           form=form,
                           username=session.get('username'),
                           password=session.get('password'),
                           known=session.get('known', False))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
