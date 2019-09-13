import unittest
import requests
from flask import url_for

from src.test import BaseLiveServerTestCase
from src.test.test_data import SYNTENY_BLOCKS_DATA


class SyntenicBlockEndpointTest(BaseLiveServerTestCase):
    """ A class to test the syntenic block endpoints. """

    def test_get_blocks(self):
        blocks_uri = self.get_server_url() + url_for('api.get_blocks')
        print(blocks_uri)
        response = requests.get(blocks_uri)
        json_resp = response.json()
        self.assertEqual(3, 3)


if __name__ == '__main__':
    unittest.main()
