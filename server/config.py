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
    UPLOAD_FOLDER = IMG_PATH

    # extension configs
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #  Machine learning configs
    ML_MODEL_TO_USE = 'knn'
    ML_DIR = 'machine_learning'
    MODEL_DIR =  'data_files'
    ML_VERBOSE = True

    # CNN configs
    ML_CNN_MODEL_FILE = path.abspath(
        path.join(PROJECT_DIR, ML_DIR, MODEL_DIR, 'colour_detect.pb')
    )
    ML_CNN_LABEL_FILE = path.abspath(
        path.join(PROJECT_DIR, ML_DIR, MODEL_DIR, 'colour_detect.txt')
    )

    # KNN configs
    ML_KNN_COLOUR_DATASET = path.abspath(
        path.join(PROJECT_DIR, ML_DIR, MODEL_DIR, 'rgb_label_dataset.pickle')
    )
    ML_KNN_N_CLUSTERS = 10
    ML_KNN_N_NEIGHBOURS = 100
    ML_KNN_NEIGHBOUR_SAMPLE_SKIP_STEP = 100
    ML_KNN_IMAGE_SAMPLE_SKIP_STEP = 100
    ML_KNN_RGB_ONLY = True
    


class DevConfig(Config):
    """Dev config."""

    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(Config.DB_PATH)

    FCM_API_KEY = "sUp3r_s3cReT_aP1_k3Y"


class ProdConfig(Config):
    """Prod config. To be used on the Raspberry Pi"""

    SQLALCHEMY_DATABASE_URI = 'sqlite:////{0}'.format(Config.DB_PATH)

