""" Tests related to the flask server"""

import unittest
import requests
from flask import url_for

from tests import BaseLiveServerTestCase
from src.app.service.colors_service import get_colors


class SmokeTest(BaseLiveServerTestCase):
    """ Is the server turning on and responding? """

    def test_app_turns_on(self):
        """ Does the flask app turn on? """
        response = requests.get(self.get_server_url())
        self.assertEqual(response.status_code, 200)

    def test_colors(self):
        """ Can we reach a known endpoint? """
        uri = self.get_server_url() + url_for('api.color-map_client_colors')
        response = requests.get(uri)
        self.assertEqual(response.json(), get_colors())


if __name__ == '__main__':
    unittest.main()
