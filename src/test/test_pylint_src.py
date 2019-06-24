"""
Tests the various configuration environments
"""

import unittest
from pylint import epylint as lint

from src.test import BaseTestCase


def lint_module(module_path, options='--disable=W0511 -E'):
    """ helper function to enable drying the lint tests """
    stdout, _ = lint.py_run(f'{module_path} {options}', return_std=True)
    stdout_string = stdout.getvalue()
    code_passes = 'Your code has been rated at 10.00/10' in stdout_string
    return code_passes, stdout_string


class TestLintCode(BaseTestCase):
    """ Perform linting analysis on the source code """

    # TODO source code should pass lint tests
    @unittest.skip("Code is known to fail lint error checking")
    def test_lint_src(self):
        """ Lint the entire source and check for problems """
        code_passes, stdout = lint_module('src/')
        self.assertTrue(code_passes, stdout)


if __name__ == '__main__':
    unittest.main()
