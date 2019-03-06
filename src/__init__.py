from flask import Flask
from flask_marshmallow import Marshmallow
from src.config import config_by_name

ma = Marshmallow()


def app_factory(config_name):
    app = Flask(__name__, static_url_path='/static', static_folder='static')
    app.config.from_object(config_by_name[config_name])

    with app.app_context():
        ma.init_app(app)

    return app
