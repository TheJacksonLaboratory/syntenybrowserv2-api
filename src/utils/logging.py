"""
Utilities to help with logging
"""

import logging

from flask.logging import wsgi_errors_stream

MODULE_FORMATTER = logging.Formatter(
    '[%(asctime)s] %(name)s %(levelname)s in %(module)s (l:%(lineno)d): %(message)s'
)

# We want a handler just like flask's but which shows more useful information for non-flask code
MODULE_HANDLER = logging.StreamHandler(wsgi_errors_stream)
MODULE_HANDLER.setFormatter(MODULE_FORMATTER)
