"""
This module contains the configuration environments for the flask app
"""

# The next line disables specific pylint checking
# pylint: disable=W0223
# pylint: disable=W0511
# TODO: Remove previous lines when config file attributes and methods are fully implemented


import os
import configparser

from src.utils.config_tools import CONFIG_FILE_NAME, generate_secrets, create_empty_config

BASEDIR = os.path.abspath(os.path.dirname(__file__))

# Try to read the synbrowser.config file
_CFG = configparser.ConfigParser(allow_no_value=True)
_CFG_READ = _CFG.read(CONFIG_FILE_NAME)

# If nothing read, create it
if not _CFG_READ:
    create_empty_config()
    _CFG.read(CONFIG_FILE_NAME)

# Create secrets if not present
if not _CFG.get('MAIN', 'FLASK_SECRET') or not _CFG.get('MAIN', 'JWT_SECRET'):
    generate_secrets()
    _CFG.read(CONFIG_FILE_NAME)


class Config:
    """ This is the base config that's used by all other configs """
    SECRET_KEY = _CFG.get('MAIN', 'FLASK_SECRET')
    JWT_SECRET_KEY = _CFG.get('MAIN', 'JWT_SECRET')
    DEBUG = False

    ERROR_404_HELP = False
    RESTPLUS_MASK_SWAGGER = False

    # TODO: Fill in celery config
    # Celery
    CELERY_BROKER_URL = _CFG.get('CELERY', 'CELERY_BROKER_URL')
    CELERY_RESULT_BACKEND = _CFG.get('CELERY', 'CELERY_RESULT_BACKEND')
    CELERY_TRACK_STARTED = True

    # TODO: Fill in LDAP info
    # LDAP Config
    LDAP = {
        'PW': _CFG.get('LDAP', 'PASSWORD'),
        'USER': _CFG.get('LDAP', 'USER'),
        'HOST': 'ldap://ldap.jax.org:389',
        'BASE': 'DC=jax,DC=org',
        'USER_DOMAIN': 'jax.org',
        'SEARCH_FILTER': '(&(sAMAccountName={})(memberOf=CN={},OU=Unix,OU=Groups,DC=jax,DC=org))',
        'SEARCH_TIMEOUT': 10
    }

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
                              os.path.join(BASEDIR,
                                           '../synteny.db?check_same_thread=False')


class DevelopmentConfig(Config):
    """ Development Specific Config """
    DEBUG = True


class TestingConfig(Config):
    """ Testing Specific Config """
    DEBUG = True
    TESTING = True

    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
                              os.path.join(BASEDIR,
                                           '../synbrowser.test.db')


class ProductionConfig(Config):
    """ Production Config. WARNING: BE CAREFUL """
    DEBUG = False

    # TODO: Use a production quality database in production
    # TODO: Uncomment when using production. Valid credentials required for proper use
    # SQLALCHEMY_DATABASE_URI = f"{_CFG.get('DATABASE', 'DIALECT')}://" \
    #     f"{_CFG.get('DATABASE', 'USERNAME')}:" \
    #     f"{_CFG.get('DATABASE', 'PASSWORD')}@" \
    #     f"{_CFG.get('DATABASE', 'HOST')}:" \
    #     f"{_CFG.get('DATABASE', 'PORT')}/" \
    #     f"{_CFG.get('DATABASE', 'DATABASE')}"


DEFAULT_CONFIG = DevelopmentConfig  # pylint: disable=C0103

CONFIG_BY_NAME = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

KEY = Config.SECRET_KEY
