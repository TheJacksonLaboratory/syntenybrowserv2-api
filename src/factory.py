"""
Factories for the falsk app and the celery app
"""

from celery import Celery
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate

from src.config import CONFIG_BY_NAME, DEFAULT_CONFIG
from src.app.model import MA, init_db, BASE


def create_app(config_name=None, app=None, config_object=None):
    """
    Create an instance of a flask app
    :param config_name: the name of the config to use
    :param app: existing app if initialized
    :param config_object: Config object that will override config name
    :return:
    """
    app = app or Flask(__name__, static_url_path='/static', static_folder='static')
    conf = config_object or CONFIG_BY_NAME.get(config_name, DEFAULT_CONFIG)
    app.config.from_object(conf)
    app.app_context().push()
    with app.app_context():
        Migrate(app, BASE)
        MA.init_app(app)
        app.config['db_engine'] = init_db(app)
        CORS(app)

    return app


def make_celery(app=None):
    """
    Create the celery instance from an existing app, or from a new app
    :param app: Flask app if created
    :return:
    """
    app = app or create_app('dev')
    celery = Celery(__name__, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task # pylint: disable=C0103

    class ContextTask(TaskBase):  # pylint: disable=R0903
        """ Inject flask context into the celery object """
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery
