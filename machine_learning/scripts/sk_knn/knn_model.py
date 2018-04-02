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

        if config.ML_KNN_N_CLUSTERS is None:
            config.ML_KNN_N_CLUSTERS = 2
        
        if config.ML_KNN_N_NEIGHBOURS is None:
            config.ML_KNN_N_NEIGHBOURS = 4
        
        if config.ML_KNN_NEIGHBOUR_SAMPLE_SKIP_STEP is None:
            config.ML_KNN_NEIGHBOUR_SAMPLE_SKIP_STEP = 1

        if config.ML_KNN_IMAGE_SAMPLE_SKIP_STEP is None:
            config.ML_KNN_IMAGE_SAMPLE_SKIP_STEP = 1

        if config.ML_KNN_RGB_ONLY is None:
            config.ML_KNN_RGB_ONLY = False

        if config.ML_VERBOSE is None:
            config.ML_VERBOSE = False

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
        self._image_skip_step = config.ML_KNN_IMAGE_SAMPLE_SKIP_STEP
        self._rgb_only = config.ML_KNN_RGB_ONLY

        self._verbose = config.ML_VERBOSE

        if (self._rgb_only):
            self._colour_mapper = {
                'pink': 'red',
                'red': 'red',
                'brown': 'black',
                'sky': 'blue',
                'gold': 'red',
                'purple': 'blue',
                'olive': 'green',
                'mustard': 'red',
                'lime': 'green',
                'green': 'green',
                'orange': 'red',
                'maroon': 'red',
                'navy': 'blue',
                'dark': 'black',
                'yellow': 'red',
                'teal': 'green',
                'light': 'black',
                'magenta': 'red',
                'black': 'black',
                'cyan': 'black',
                'blue': 'blue'
            }

    
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
        sample = dataset[1::self._image_skip_step]

        # Obtain the kmeans of the sample and the cluster of each
        # element in the sample
        clusters = self._cluster_model.fit(sample).cluster_centers_
        cluster_size = self._cluster_model.labels_

        # Determine the RGB colour of each cluster
        cluster_colours = self._neighbour_model.predict(clusters)

        # The number of pixels in each category
        if (self._verbose):
            unique, counts = np.unique(cluster_size, return_counts=True)
            unique = [cluster_colours[x] for x in unique]
            print(dict(zip(unique, counts)))

        cluster_colours = cluster_colours.tolist()

        # map and mode
        confidence = 1
        if (self._rgb_only):
            cluster_colours = [self._colour_mapper[x]  
                            for x in cluster_colours 
                            if (self._colour_mapper[x] != 'black')]
            if (self._verbose):
                print('Mapping to RGB:')
                print(cluster_colours)

        if len(cluster_colours) == 0: 
            colour_mode = 'black'
            confidence = 0
            return colour_mode, confidence

        colour_mode = max(set(cluster_colours), key=cluster_colours.count)
        confidence = cluster_colours.count(colour_mode) / len(cluster_colours)
        if (self._verbose):
            print('Mode: {0} | Confidence: {1}'.format(colour_mode, confidence))
        return colour_mode, confidence


class MockConfig:
    ML_KNN_N_CLUSTERS = 3
    ML_KNN_N_NEIGHBOURS = 4
    ML_KNN_NEIGHBOUR_SAMPLE_SKIP_STEP = 10
    ML_KNN_IMAGE_SAMPLE_SKIP_STEP = 100
    ML_KNN_RGB_ONLY = True
    ML_VERBOSE = True
    ML_KNN_COLOUR_DATASET = '../../data_files/rgb_label_dataset.pickle'

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

    

