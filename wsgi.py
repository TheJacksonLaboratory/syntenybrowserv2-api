# -*- coding: utf-8 -*-
"""
    wsgi
    ~~~~

    synbrowser wsgi module
"""

from werkzeug.serving import run_simple
from werkzeug.wsgi import DispatcherMiddleware

from src.app import create_app

app = create_app('prod')
application = DispatcherMiddleware(app)

try:
    import uwsgi

    def postfork():
        app.config['db_engine'].dispose()
    uwsgi.post_fork_hook = postfork
except ImportError:
    pass

if __name__ == "__main__":
    run_simple('localhost', 5000, application, use_reloader=True, use_debugger=True)
