from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')
@app.route('/<name>')
def index(name = None):
    user_agent = request.headers.get('User-Agent')
    return render_template('index.html', user = name, agent = user_agent)

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000, debug = True)
