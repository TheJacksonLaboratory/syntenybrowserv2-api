"""
Utilities to help manage the 'synbrowser.config' configuration file
"""
import logging
import secrets
import configparser
from src.utils.logging import MODULE_HANDLER

CONFIG_FILE_NAME = 'synbrowser.config'

EXAMPLE_CELERY_URI = 'amqp://<USER>:<PASS>@<BROKER_URL>:<PORT>/<VHOST>'

LOGGER = logging.getLogger('config.generate_secrets')
LOGGER.addHandler(MODULE_HANDLER)

def generate_secrets():
    """
    Write secret keys to fields in CONFIG_FILE_NAME
    :return:
    """
    config_dict = configparser.ConfigParser(allow_no_value=True)
    config_dict.read(CONFIG_FILE_NAME)

    if not config_dict.get('MAIN', 'FLASK_SECRET'):
        LOGGER.warning("Flask secret not found, GENERATING NEW SECRET")
        config_dict['MAIN']['FLASK_SECRET'] = secrets.token_hex(32)
    if not config_dict.get('MAIN', 'JWT_SECRET'):
        LOGGER.warning("JWT secret not found, GENERATING NEW SECRET")
        config_dict['MAIN']['JWT_SECRET'] = secrets.token_hex(32)

    with open(CONFIG_FILE_NAME, 'w') as configfile:
        config_dict.write(configfile)


def create_empty_config():
    """
    Creates an empty config file for the user to fill out
    :return:
    """
    # TODO: Include user prompts
    config_dict = configparser.ConfigParser(allow_no_value=True)
    config_dict['MAIN'] = {'FLASK_SECRET': '', 'JWT_SECRET': '', 'ADMIN_NAME': ''}
    config_dict['CELERY'] = {'CELERY_BROKER_URL': EXAMPLE_CELERY_URI,
                             'CELERY_RESULT_BACKEND': EXAMPLE_CELERY_URI}
    config_dict['LDAP'] = {'PASSWORD': '', 'USER': ''}
    config_dict['DATABASE'] = {
        'DIALECT': 'postgres',
        'USERNAME': '',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '5432',
        'DATABASE': ''
    }

    with open(CONFIG_FILE_NAME, 'w') as configfile:
        config_dict.write(configfile)
