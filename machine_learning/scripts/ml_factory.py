from machine_learning.scripts.tf_cnn.cnn_model import CNNModel
<<<<<<< HEAD
from machine_learning.scripts.sklearn_clustering.kmean_clst_model import ClusterModel
from machine_learning.scripts.sk_knn.knn_model import KNNModel

class MLFactory():

    def __init__(self):
        self.model = None

    """
    Instantiates a machine learning model depending on the
    configuration set

    :param config: The config files which specifies the model
                    to instantiate
    :return: a machine learning model
    """
    def init_model(self, config):
        model_str = config.ML_MODEL_TO_USE
        if model_str == 'cnn':
            self.model = CNNModel(config)

        elif model_str == 'clst':
            self.model = ClusterModel(config)

        else:
            raise ValueError('No matching model found, currently'
                             'supports: cnn and clustering')
        elif model_str == 'knn':
            self.model = KNNModel(config)
        else:
            raise ValueError('No matching model found, currently'
                             'supports: cnn, knn')


    def predict(self, image):
        if not self.model:
            raise EnvironmentError('Please initialize the model before predicting')
        return self.model.predict(image)
