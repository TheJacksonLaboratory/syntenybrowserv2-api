import os
import logging
from flask import redirect

from src import app_factory
from src.app import blueprint, api
from src.app.model import init_db

from flask_cors import CORS
from flask_jwt_extended import JWTManager

app = app_factory(os.getenv('FLASK_CONFIG') or 'dev')
engine = init_db(app)

app.register_blueprint(blueprint, url_prefix='/api/v1')
app.app_context().push()

jwt = JWTManager(app)

# flask-restplus breaks the native flask error handlers used by jwt
# this fixes it.
jwt._set_error_handler_callbacks(api)

CORS(app)

# if we are using uWSGI, make sure each process has its own clean connection
# pool in case uWSGI is not loading the model module lazily. Do this by
# registering a post_fork_hook that calls model.engine.dispose()
# Database connections should not be shared across process boundaries.
try:
    import uwsgi

    def postfork():
        model.engine.dispose()
    uwsgi.post_fork_hook = postfork
except ImportError:
    pass


@app.route('/')
def root():
    return redirect('/api/v1')


if __name__ != "__main__":
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)


if __name__ == "__main__":
    app.run()
