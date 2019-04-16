"""
Starts the dev server
"""

from flask_script import Command

from src import APP


class RunCommand(Command):
    """
    The main entrypoint to running the app
    :return: None
    """

    def run(self):  # pylint: disable=E0202
        """ invoked by the command """
        APP.run()
