import os, sys


class Config(object):
    """Base config."""

    # directory configs
    DB_DIR = '\\db\\database.db'
    DB_PATH = os.path.abspath(os.path.dirname(sys.modules['__main__'].__file__) + DB_DIR)

    # extension configs
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):
    """Dev config."""

    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(Config.DB_PATH)


class ProdConfig(Config):
    """Prod config. To be used on the Raspberry Pi"""

    SQLALCHEMY_DATABASE_URI = 'sqlite:////{0}'.format(Config.DB_PATH)

