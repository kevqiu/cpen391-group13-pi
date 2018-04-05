from machine_learning.scripts.sklearn_clustering.kmean_clst_model import ClusterModel
from machine_learning.scripts.sk_knn.knn_model import KNNModel

class EnsembleModel:

    def __init__(self, config):
        self.model1=ClusterModel(config)
        self.model2=KNNModel(config)


    def predict(self, image_path):
        (category1, confidence1) = self.model1.predict(image_path)
        (category2, confidence2) = self.model2.predict(image_path)

        clusters = self.model2.cluster_colours

        if confidence2 > 0.8:
            (ensbl_cat,ensbl_conf) = (category2, confidence2)
        elif category1 in clusters:
            (ensbl_cat,ensbl_conf) = (category1, confidence1)
        else:
            ensbl_cat = "OTHER"
            ensbl_conf = (confidence1 + confidence2) // 2

        return (ensbl_cat,ensbl_conf)
        
