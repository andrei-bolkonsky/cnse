from .weather_utils import get_current_conditions, get_hourly_conditions
from flask import render_template, session, redirect, url_for
from flask_login import login_required
from .forms import ArticleForm
from ..models import Post
from . import main


@main.route('/')
def index():
    weather_data = get_current_conditions()
    data = get_hourly_conditions()
    articles = Post.query.all()
    return render_template('index.html', weather_data=weather_data, data=data, articles=articles)


@main.route('/test')
@login_required
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
