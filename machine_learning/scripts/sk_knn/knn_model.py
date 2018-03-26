from sklearn.cluster import KMeans
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
import pickle
from PIL import Image
import argparse
import time

class KNNModel:

    def __init__(self, X, y):
        self.X = X
        self.y = y
        self._model = KMeans(n_clusters=2, random_state=0).fit(self.X)
        # with open('rgb_label_dataset.pickle', 'rb') as data: 
        #     dataset = pickle.load(data)
        # X = dataset['X']
        # y = dataset['y']
     

def main(args):
    image = Image.open(args.image_file).convert('RGB')
    img_matrix = np.array(image)
    num_pixels = img_matrix.shape[0] * img_matrix.shape[1]
    dataset = img_matrix.reshape((num_pixels, 3))
    # Sample every 500th pixel
    sample = dataset[1::500]
    model = KMeans(n_clusters=4, random_state=0).fit(sample)
    clusters = model.cluster_centers_


    load_start = time.time()
    with open('rgb_label_dataset.pickle', 'rb') as data: 
        dataset = pickle.load(data)
    X = dataset['X']
    y = dataset['y']
    print('%s for load time' % round(time.time() - load_start, 2))

    kneighbours_start = time.time()
    X_sample = X[1::10]
    y_sample = y[1::10]
    knn_model = KNeighborsClassifier(n_neighbors=4, algorithm='kd_tree').fit(X_sample, y_sample)
    y_hat = knn_model.predict(clusters)
    print('%s for load time' % round(time.time() - kneighbours_start, 2))
    print(y_hat)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--image_file',
        type=str,
        default='',
        help='Location of image file to analyze'
    )
    args, unparsed = parser.parse_known_args()
    start_time = time.time()
    main(args)
    print('%s seconds' % round(time.time() - start_time, 2))

    

