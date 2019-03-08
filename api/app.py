from flask import Flask
from blueprints.test import test_blueprint
app = Flask(__name__)
app.register_blueprint(test_blueprint, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)
