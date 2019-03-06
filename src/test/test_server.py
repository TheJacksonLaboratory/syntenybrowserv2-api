import unittest
import requests
from src.application import app
from src.config import config_by_name
from flask_testing import LiveServerTestCase
from flask import url_for


class SmokeTest(LiveServerTestCase):

    def create_app(self):
        app.config.from_object(config_by_name['test'])
        app.config['LIVESERVER_TIMEOUT'] = 10
        return app

    def test_app_turns_on(self):
        response = requests.get(self.get_server_url())
        self.assertEqual(response.status_code, 200)
    
    def test_hello(self):
        uri = self.get_server_url() + url_for('api.hello_hello_world')
        response = requests.get(uri)
        self.assertEquals(response.json(), dict(message="Hello World!"))
    


if __name__ == '__main__':
    unittest.main()
