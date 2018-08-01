"""Set up environment specific configurations
    this is important in determining the verbosity of the app

    usage
            `export APP_SETTINGS="testing"`
            `export SECRET="OwnDarkSecret"`
            # where APP_SETTINGS can be testing, production or development

"""

import os


class Config(object):
    """Parent Configurations"""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')


class Development(Config):
    """Configuration for development environment
    inherits the defaults from Config
    """
    DEBUG = True
    APP_SETTINGS = "development"


class Testing(Config):
    """Configuration for testing environment
    inherits the defaults from Config
    """
    TESTING = True
    DEBUG = True
    APP_SETTINGS = "testing"
    DATABASE_NAME = os.getenv("DATABASE_TESTS")


class Production(Config):
    """Configuration for production environment
    inherits the defaults from Config
    """
    DEBUG = False
    TESTING = False


config_app = {
    'development': Development,
    'testing': Testing,
    'production': Production,
}
