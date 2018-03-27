from os import path


class Config(object):
    """Base config."""

    # directory configs
    PROJECT_DIR = path.dirname(path.dirname(path.abspath(__file__)))
    DB_DIR = 'db'
    DB_FILE = 'database.db'
    DB_PATH = path.abspath(path.join(PROJECT_DIR, DB_DIR, DB_FILE))
    IMG_DIR = 'images'
    IMG_PATH = path.abspath(path.join(PROJECT_DIR, IMG_DIR))

    # extension configs
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #  Machine learning configs
    ML_MODEL_TO_USE = 'cnn'

    ML_DIR = 'machine_learning'

    # CNN configs
    MODEL_DIR =  'data_files'
    ML_CNN_MODEL_FILE = path.abspath(
        path.join(PROJECT_DIR, ML_DIR, MODEL_DIR, 'colour_detect.pb')
    )
    ML_CNN_LABEL_FILE = path.abspath(
        path.join(PROJECT_DIR, ML_DIR, MODEL_DIR, 'colour_detect.txt')
    )


class DevConfig(Config):
    """Dev config."""

    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(Config.DB_PATH)

    FCM_API_KEY = "sUp3r_s3cReT_aP1_k3Y"


class ProdConfig(Config):
    """Prod config. To be used on the Raspberry Pi"""

    SQLALCHEMY_DATABASE_URI = 'sqlite:////{0}'.format(Config.DB_PATH)

