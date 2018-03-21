from sklearn.cluster import KMeans
from sklearn import metrics
import numpy as np
import cv2

class ClusterModel:

    def __init__(self, config):
        pass

    def predict(self, image_path):
        """
        Takes in an image and returns a tuple with its
        categorization and a confidence level

        Args:
          image_path: the path to the image file (jpg)
        """
    # Load the image
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Resize it
        h, w, _ = image.shape
        w_new = int(100 * w / max(w, h) )
        h_new = int(100 * h / max(w, h) )
        image = cv2.resize(image, (w_new, h_new));


# Reshape the image to be a list of pixels
        image_array = image.reshape((image.shape[0] * image.shape[1], 3))
#print image_array
# Clusters the pixels
        clt = KMeans(n_clusters = 3)
        clt.fit(image_array)



        clt = KMeans(n_clusters=2)
        clt.fit(image_array)

        hist = centroid_histogram(clt)
        zipped = zip(hist, clt.cluster_centers_)
        zipped.sort(reverse=True, key=lambda x: x[0])

        hist, clt.cluster_centers = zip(*zipped)
        clt_centers = np.array(clt.cluster_centers_)


# print (clt_centers)
        print( check_clt(clt_centers))



    def centroid_histogram(clt):
# grab the number of different clusters and create a histogram
# based on the number of pixels assigned to each cluster
        numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
        (hist, _) = np.histogram(clt.labels_, bins = numLabels)

# normalize the histogram, such that it sums to one
        hist = hist.astype("float")
        hist /= hist.sum()

# return the histogram
        return hist

    def check_clt(centers):
        if all(i >= 50 and i<155  for i in centers[0]):
            return colour_id(centers[1])
        else:
            return colour_id(centers[0])

    def colour_id(center):
        max_col = np.argmax(center)
        if max_col==0:
            return "RED"
        if max_col==1:
            return "GREEN"
        if max_col==2:
            return "BLUE"


# # Finds how many pixels are in each cluster
# hist = centroid_histogram(clt)

# # Sort the clusters according to how many pixel they have
# zipped = zip (hist, clt.cluster_centers_)
# zipped.sort(reverse=True, key=lambda x : x[0])
# hist, clt.cluster_centers = zip(*zipped)

# # By Adrian Rosebrock
# import numpy as np
# import cv2

# bestSilhouette = -1
# bestClusters = 0;

# for clusters in range(2, 10):
#     # Cluster colours
#     clt = KMeans(n_clusters = clusters)
#     clt.fit(image_array)

#     # Validate clustering result
#     silhouette = metrics.silhouette_score(image_array, clt.labels_, metric='euclidean')

#     # Find the best one
#     if silhouette > bestSilhouette:
#         bestSilhouette = silhouette;
#         bestClusters = clusters;

# print (clt.cluster_centers_)
# print bestSilhouette
# print bestClusters
	