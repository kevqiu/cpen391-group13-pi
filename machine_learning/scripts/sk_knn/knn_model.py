from sklearn.cluster import KMeans
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
import pickle
from PIL import Image
import argparse
import time

class KNNModel:

    def __init__(self, config):
        self.validate_config(config)

        if not config.ML_KNN_N_CLUSTERS:
            config.ML_KNN_N_CLUSTERS = 2
        
        if not config.ML_KNN_N_NEIGHBOURS:
            config.ML_KNN_N_NEIGHBOURS = 4
        
        if not config.ML_KNN_NEIGHBOUR_SAMPLE_SKIP_STEP:
            config.ML_KNN_NEIGHBOUR_SAMPLE_SKIP_STEP = 1

        if not config.ML_KNN_IMAGE_SAMPLE_SKIP_STEP:
            config.ML_KNN_IMAGE_SAMPLE_SKIP_STEP = 1

        # Grab dataset for KNN
        dataset = None
        with open(config.ML_KNN_COLOUR_DATASET, 'rb') as data: 
            dataset = pickle.load(data)
        
        X = dataset['X']
        y = dataset['y']
        X_sample = X[1::config.ML_KNN_NEIGHBOUR_SAMPLE_SKIP_STEP]
        y_sample = y[1::config.ML_KNN_NEIGHBOUR_SAMPLE_SKIP_STEP]

        self._cluster_model = KMeans(n_clusters=config.ML_KNN_N_CLUSTERS, random_state=0)
        self._neighbour_model = KNeighborsClassifier(n_neighbors=config.ML_KNN_N_NEIGHBOURS,
                                                     algorithm='kd_tree').fit(X_sample, y_sample)
        self.image_skip_step = config.ML_KNN_IMAGE_SAMPLE_SKIP_STEP

    
    def validate_config(self, config):
        if not config.ML_KNN_COLOUR_DATASET:
            raise AssertionError('KNN model instantiated with no configuration')
    
    def predict(self, image_path):
        image = Image.open(image_path).convert('RGB')
        img_matrix = np.array(image)
        # Flatten
        num_pixels = img_matrix.shape[0] * img_matrix.shape[1]
        dataset = img_matrix.reshape((num_pixels, 3))
        # Sample every nth pixel
        sample = dataset[1::self.image_skip_step]
        clusters = self._cluster_model.fit(sample).cluster_centers_
        cluster_colours = self._neighbour_model.predict(clusters)
        print(cluster_colours)
        return cluster_colours


class MockConfig:
    ML_KNN_N_CLUSTERS = 2
    ML_KNN_N_NEIGHBOURS = 4
    ML_KNN_NEIGHBOUR_SAMPLE_SKIP_STEP = 10
    ML_KNN_IMAGE_SAMPLE_SKIP_STEP = 100
    ML_KNN_COLOUR_DATASET = 'rgb_label_dataset.pickle'

def main(args):
    model = KNNModel(MockConfig())
    model.predict(args.image_file)

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

    

