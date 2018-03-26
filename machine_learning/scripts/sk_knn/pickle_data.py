import pickle
import re
import numpy as np

def pickle_data(data_file):
    p = re.compile('^\[(\d+),.?(\d+),.?(\d+)\]\s?(\w+)')

    # Find dataset size
    n = 0
    with open(data_file) as file:
        n = sum(1 for line in file)
    
    X = np.zeros((n, 3))
    y = [] # plain ol' array?
    with open(data_file) as file:
        for i, x in enumerate(file):
            res = p.match(x)
            X[i] = res.groups()[0:3]
            y.append(res.groups()[3])

    cucumber = {'X': X, 'y':y}
    with open('rgb_label_dataset.pickle', 'wb') as handle:
        pickle.dump(cucumber, handle, protocol=pickle.HIGHEST_PROTOCOL)

def read_pickle(data_file):
    with open(data_file, 'rb') as file:
        data = pickle.load(file)
        X = data['X']
        y = data['y']
        n = 0
        for i, x in enumerate(X):
            n += 1
            print(str(x) + ' : ' + str(y[i]))
        print(n)

if __name__ == "__main__":
    pickle_data('rgb_label_dataset.txt')
    read_pickle('rgb_label_dataset.pickle')
    

