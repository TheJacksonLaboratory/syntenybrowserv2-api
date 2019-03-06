import unittest
import requests
from src.application import app
from src.config import config_by_name
from flask_testing import LiveServerTestCase
from flask import url_for


class AuthTest(LiveServerTestCase):

    def create_app(self):
        app.config.from_object(config_by_name['test'])
        app.config['LIVESERVER_TIMEOUT'] = 10
        return app

    def test_auth_returns_access_and_refresh(self):
        uri = self.get_server_url() + url_for('api.auth_user_login')
        response = requests.post(uri, json={"username": "test_user", "password": "fake_password"})
        self.assertEqual(['access_token', 'refresh_token'], list(response.json().keys()))

    def test_access_token_works(self):
        auth_uri = self.get_server_url() + url_for('api.auth_user_login')
        auth_response = requests.post(auth_uri, json={"username": "test_user", "password": "fake_password"})
        access_token = auth_response.json()['access_token']

        protected_uri = self.get_server_url() + url_for('api.hello_protected_hello_world')
        protected_response = requests.get(protected_uri, headers={'Authorization': 'Bearer {}'.format(access_token)})
        self.assertEqual({"message": "Hello World!"}, protected_response.json())

    def test_refresh_token_works(self):
        auth_uri = self.get_server_url() + url_for('api.auth_user_login')
        auth_response = requests.post(auth_uri, json={"username": "test_user", "password": "fake_password"})
        refresh_token = auth_response.json()['refresh_token']

        refresh_uri = self.get_server_url() + url_for('api.auth_user_refresh')
        refresh_response = requests.post(refresh_uri, headers={'Authorization': 'Bearer {}'.format(refresh_token)})
        self.assertEqual(['access_token'], list(refresh_response.json().keys()))

if __name__ == '__main__':
    unittest.main()