from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_fontawesome import FontAwesome
from weather_utils import get_current_conditions

app = Flask(__name__)
bootstrap = Bootstrap(app)
fa = FontAwesome(app)

@app.route('/')
def index():
    weather_data = get_current_conditions()
    return render_template('index.html', weather_data = weather_data)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000, debug = True)
