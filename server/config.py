from os import path


class Config(object):
    """Base config."""

    # directory configs
    PROJECT_DIR = path.dirname(path.dirname(path.abspath(__file__)))
    DB_DIR = '\\db\\database.db'
    DB_PATH = path.abspath(PROJECT_DIR + DB_DIR)
    IMG_PATH = path.abspath(PROJECT_DIR + '\\images')

    # extension configs
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):
    """Dev config."""

    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(Config.DB_PATH)


class ProdConfig(Config):
    """Prod config. To be used on the Raspberry Pi"""

    SQLALCHEMY_DATABASE_URI = 'sqlite:////{0}'.format(Config.DB_PATH)

