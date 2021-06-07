from .weather_utils import get_current_conditions, get_hourly_conditions
from flask import render_template, session, redirect, url_for, flash
from .forms import ArticleForm, ConnectionForm
from ..models import User, Role
from . import main
from .. import db


@main.route('/')
def index():
    weather_data = get_current_conditions()
    data = get_hourly_conditions()
    return render_template('index.html', weather_data=weather_data, data=data)


@main.route('/test')
def test():
    data = get_hourly_conditions()
    return render_template('test.html', data=data)


@main.route('/admin', methods=['GET', 'POST'])
def create_article():
    form = ArticleForm()
    if form.validate_on_submit():
        session['article_title'] = form.title.data
        session['article_descr'] = form.quick_description.data
        session['article_content'] = form.content.data
        form.title.data = ''
        form.content.data = ''
        form.quick_description.data = ''
        return redirect(url_for('main.create_article'))
    return render_template('article_creation.html',
                           form=form,
                           article_title=session.get('article_title'),
                           article_descr=session.get('article_descr'),
                           article_content=session.get('article_content'))


@main.route('/login', methods=['GET', 'POST'])
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
            # if app.config['CNSE_ADMIN']:
            #     send_email(app.config['CNSE_ADMIN'], 'New User', 'mail/new_user', user=known_user)
        else:
            session['known'] = True
        return redirect(url_for('main.connection'))
    return render_template('login.html',
                           form=form,
                           username=session.get('username'),
                           password=session.get('password'),
                           known=session.get('known', False))