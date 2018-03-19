from machine_learning.scripts.tf_cnn.cnn_model import CNNModel

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
        else:
            raise ValueError('No matching model found, currently'
                             'supports: cnn')

    def predict(self, image):
        if not self.model:
            raise EnvironmentError('Please initialize the model before predicting')
        return self.model.predict(image)
