from flask import Flask
app = Flask(__name__)


@app.route('/test')
def index():
    return "OK"


if __name__ == '__main__':
    app.run(debug=True)
