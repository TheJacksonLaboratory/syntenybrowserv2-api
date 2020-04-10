"""
This is the manager entrypoint to the application
"""

import sys
import unittest
import logging

from xmlrunner import XMLTestRunner
from flask_script import Command


class RunTestsCommand(Command):
    """ Run unit test """
    def run(self):  # pylint: disable=E0202
        """ invoked by the command """
        logging.basicConfig(stream=sys.stderr)
        tests = unittest.TestLoader().discover('src/test', pattern='test*.py')
        result = unittest.TextTestRunner(verbosity=2).run(tests)
        if result.wasSuccessful():
            return 0
        return 1


class RunTestsXMLCommand(Command):
    """ Runs the unit test specifically for bamboo CI/CD """

    def run(self): # pylint: disable=E0202
        """ invoked by the command """
        tests = unittest.TestLoader().discover('src/test', pattern='test*.py')
        result = XMLTestRunner(output='test-reports').run(tests)
        if result.wasSuccessful():
            return 0
        return 1
