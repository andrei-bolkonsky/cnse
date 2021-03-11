from flask import Flask, render_template, request
from weather_utils import get_current_conditions, get_hourly_conditions
from flask_moment import Moment 
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, TextAreaField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hardtoguesskey'

moment = Moment(app)

class ArticleForm(FlaskForm):
    title = StringField("", validators=[DataRequired()], render_kw={'placeholder':"Titre de l'article"})
    # image = FileField()
    content = TextAreaField("", validators=[DataRequired()], render_kw={'placeholder':"Contenu"})
    submit = SubmitField('Valider')

@app.route('/')
def index():
    weather_data = get_current_conditions()
    data = get_hourly_conditions()
    return render_template('index.html', weather_data = weather_data, data = data)

@app.route('/test')
def test():
    data = get_hourly_conditions()
    return render_template('test.html', data = data)

@app.route('/admin', methods=['GET', 'POST'])
def create_article():
    article_title = None
    article_content = None
    form = ArticleForm()
    if form.validate_on_submit():
        article_title = form.title.data
        article_content = form.content.data
        form.title.data = ''
        form.content.data = ''
    return render_template('article_creation.html', 
                           form = form, 
                           article_title = article_title,
                           article_content = article_content)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000, debug = True)
