from sklearn.cluster import KMeans
import numpy as np

class KNNModel:

    def __init__(self, X, y):
        self.X = X
        self.y = y
        self._model = KMeans(n_clusters=2, random_state=0).fit(self.X)
    



if __name__ == "__main__":


