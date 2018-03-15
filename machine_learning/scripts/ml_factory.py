from machine_learning.scripts.tf_cnn.cnn_model import CNNModel

def MLFactory(config):
    """
    Instantiates a machine learning model depending on the
    configuration set

    :param config: The config files which specifies the model
                    to instantiate
    :return: a machine learning model
    """

    model = config.ML_MODEL_TO_USE
    if model == 'cnn':
        return CNNModel(config)
    else:
        raise ValueError('No matching model found, currently'
                         'supports: cnn')




