import logging
import os

from dotenv import load_dotenv
from pathlib import Path
from flask import Flask, current_app

app_profile = os.getenv("PROFILE", "development")
DEBUG_STATE = {
    True: logging.ERROR,
    False: logging.DEBUG
}


def fill_config_var(target, data, ex=''):
    if app_profile != 'testing' and data is None:
        if bool(ex.strip()):
            raise ValueError(ex)
        else:
            raise ValueError('Couldn\'t fill variable. data is empty')

    if not target:
        target = data
        return target
    elif isinstance(target, int) and target == 0:
        target = data
        return target
    elif isinstance(target, str) and target == '':
        target = data
        return target
    elif isinstance(target, bool) and target is False:
        target = data
        return target
    else:
        raise ValueError('{} is not a empty variable'.format(type(target).__name__))


class Config:
    DEBUG = False
    TESTING = False
    BOTNAME = ""
    TOKEN = ""
    SOURCE_TOKEN = ""
    HOST = ""  # Same FQDN used when generating SSL Cert
    PORT = 0
    CERT = None
    CERT_KEY = ""
    DISABLE_SSL = False
    PERMANENT_CHATS = None  # Comma separated ids wrapped in a string
    OWNER_ID = ""

    # self.DEBUG = int(os.getenv('DEBUG', 0))

    def __init__(self, path=r'..\res\variables.env'):
        # Load .env file
        try:
            env_path = Path(path)
            load_dotenv(env_path)
        except FileExistsError:
            print('Couldn\'t find Environment Variables')

        # Load environment variables
        self.BOTNAME = fill_config_var(self.BOTNAME, os.getenv('BOTNAME'), 'BOTNAME is not set')
        self.TOKEN = fill_config_var(self.TOKEN, os.getenv('TOKEN'), 'TOKEN is not set')
        self.SOURCE_TOKEN = fill_config_var(self.SOURCE_TOKEN, os.getenv('SOURCE_TOKEN', ""))
        self.HOST = fill_config_var(self.HOST, os.getenv('HOST'), 'HOST url is not set')
        self.PORT = fill_config_var(self.PORT, int(os.getenv('PORT', 8443)))
        self.CERT = fill_config_var(self.CERT, os.getenv('CERT'))
        self.CERT_KEY = fill_config_var(self.CERT_KEY, os.getenv('CERT_KEY'))
        self.DISABLE_SSL = fill_config_var(self.DISABLE_SSL, os.getenv('DISABLE_SSL'))
        self.PERMANENT_CHATS = fill_config_var(self.PERMANENT_CHATS, os.getenv('PERMANENT_CHATS'))
        self.OWNER_ID = fill_config_var(self.OWNER_ID, os.getenv('OWNER_ID'))
        # self.DEBUG = fill_config_var(self.DEBUG, int(os.getenv('DEBUG', 0)))

    def create_logger(self, app: Flask):
        # Gunicorn has its own loggers and handlers. need to wire up Flask application to use those handlers
        logger = logging.getLogger('gunicorn.error')
        app.logger.handlers = logger.handlers
        app.logger.setLevel(DEBUG_STATE[self.DEBUG])
        return logger


class ProductionConfig(Config):
    DEBUG = False

    def __init__(self):
        super(ProductionConfig, self).__init__()


class StagingConfig(Config):
    DEBUG = True


class DevelopmentConfig(Config):
    DEBUG = True
    HOST = os.getenv("HOST", "http://127.0.0.1:8000/")
    """
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "postgresql://postgres:@localhost/thb"
    )
    """


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    HOST = os.getenv("HOST", "http://127.0.0.1:8000/")
    # SQLALCHEMY_DATABASE_URI = "sqlite://"
    BOTNAME = "test"
    TOKEN = "123:dummy"


app_config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "staging": StagingConfig,
    "production": ProductionConfig,
}


def active_config_name():
    config_name = None

    if current_app:
        config_name = current_app.config_name

    if not config_name:
        config_name = app_profile

    return config_name


def get_active_config():
    return app_config[active_config_name()]
