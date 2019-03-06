import os
import secrets

basedir = os.path.abspath(os.path.dirname(__file__))

flask_secret_default = secrets.token_hex(32)
jwt_secret_default = secrets.token_hex(32)

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', flask_secret_default)
    JWT_SECRET_KEY =  os.getenv('JWT_SECRET_KEY', jwt_secret_default)
    DEBUG = False

    TASKS = ['Short task', 'Long task', 'Task raises error']
    MAX_TIME_TO_WAIT = 10
    REDIS_URL = 'redis://redis:6379/0'
    QUEUES = ['default']

    ERROR_404_HELP = False
    RESTPLUS_MASK_SWAGGER = False

    # LDAP Config
    LDAP = {
        'PW': 'CHANGEME',
        'USER': 'CHANGEME',
        'HOST': 'ldap://ldap.jax.org:389',
        'BASE': 'DC=jax,DC=org',
        'USER_DOMAIN': 'jax.org',
        'SEARCH_FILTER': '(&(sAMAccountName={})(memberOf=CN={},OU=Unix,OU=Groups,DC=jax,DC=org))',
        'SEARCH_TIMEOUT': 10
    }

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'service.dev.sqlite.db')


class TestingConfig(Config):
    DEBUG = True
    TESTING = True

    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'service.test.sqlite.db')


class ProductionConfig(Config):
    DEBUG = False


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY
