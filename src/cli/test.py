"""
This is the manager entrypoint to the application
"""

import sys
import unittest
import logging

from xmlrunner import XMLTestRunner
from flask_script import Command


class RunTestsCommand(Command):
    """ Run unit tests """
    def run(self):  # pylint: disable=E0202
        """ invoked by the command """
        logging.basicConfig(stream=sys.stderr)
        tests = unittest.TestLoader().discover('src/tests', pattern='tests*.py')
        result = unittest.TextTestRunner(verbosity=2).run(tests)
        if result.wasSuccessful():
            return 0
        return 1


class RunTestsXMLCommand(Command):
    """ Runs the unit tests specifically for bamboo CI/CD """

    def run(self): # pylint: disable=E0202
        """ invoked by the command """
        tests = unittest.TestLoader().discover('src/tests', pattern='tests*.py')
        result = XMLTestRunner(output='tests-reports').run(tests)
        if result.wasSuccessful():
            return 0
        return 1
