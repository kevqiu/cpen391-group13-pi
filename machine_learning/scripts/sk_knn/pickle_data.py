import pickle
import re
import numpy as np


def pickle_data(data_file, output_file):
    """
    Parse and pickles xkcd colour recognition data with
    X as the rgb points and y as the corresponding label

    Args:
        data_file: the text file containing the data
        output_file: the name of the output file
    """
    p = re.compile(r'^\[(\d+),.?(\d+),.?(\d+)\]\s?(\w+)')
    # Find dataset size
    n = 0
    with open(data_file) as data:
        n = sum(1 for line in data)
    
    X = np.zeros((n, 3))
    y = [] # plain ol' array?
    with open(data_file) as data:
        for i, x in enumerate(data):
            res = p.match(x)
            X[i] = res.groups()[0:3]
            y.append(res.groups()[3])

    cucumber = {'X': X, 'y':y}
    with open('rgb_label_dataset.pickle', 'wb') as handle:
        pickle.dump(cucumber, handle, protocol=pickle.HIGHEST_PROTOCOL)


def read_pickle(data_file):
    """ 
    Test function to test the integrity of pickled data
    """
    with open(data_file, 'rb') as data:
        dataset = pickle.load(data)
        X = dataset['X']
        y = dataset['y']
        n = 0
        for i, x in enumerate(X):
            n += 1
            print(str(x) + ' : ' + str(y[i]))
        print(n)


if __name__ == "__main__":
    pickle_data('rgb_label_dataset.txt', 'rgb_label_dataset.pickle')
    read_pickle('rgb_label_dataset.pickle')
    

