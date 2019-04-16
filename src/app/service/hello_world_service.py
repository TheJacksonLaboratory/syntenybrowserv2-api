"""
A hello world example service
"""
# This next line disables checking that instance of 'scoped_session'
# has no 'commit' or 'bulk_save_objects' members, The members are there,
# pylint just can't tell
#
# pylint: disable=E1101

import logging
import datetime as dt
from src.utils.logging import MODULE_HANDLER

from ..model import SESSION
from ..model.hello_world_model import Hello

# Get the logger
LOGGER = logging.getLogger('service.sayhello')
LOGGER.addHandler(MODULE_HANDLER)

def say_hello(name='World'):
    """
    An example service function that says hello
    :param name: A name to say hello to, defaults to 'World'
    :return: dict {'message': <response>}
    """
    LOGGER.warning("Started saying hello to: {}".format(name))
    SESSION.add(Hello(who=name, when=dt.datetime.now()))
    SESSION.commit()
    LOGGER.warning("Said hello to: %".format(name))
    return {"message": "Hello {}!".format(name if name else "World")}
