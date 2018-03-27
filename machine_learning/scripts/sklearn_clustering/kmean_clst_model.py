from sklearn.cluster import KMeans
from sklearn import metrics
import numpy as np
from PIL import Image

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
        image = self.load_image(image_path)

    # Reshape the image to be a list of pixels
        image_array = image.reshape((image.shape[0] * image.shape[1], 3))
        #print(image_array)
   
    # Clusters the pixels
        # clt = KMeans(n_clusters = 3)
        # clt.fit(image_array)

        clt = KMeans(n_clusters=2)
        clt.fit(image_array)

        hist = self.centroid_histogram(clt)
        zipped = list(zip(hist, clt.cluster_centers_))
        
        sorted(zipped, key=lambda x: x[0])
        #zipped.sort(reverse=True, key=lambda x: x[0])

        hist, clt.cluster_centers = zip(*zipped)
        clt_centers = np.array(clt.cluster_centers_)


        #print(self.check_clt(clt_centers))
        category = self.check_clt(clt_centers)
        confidence = 1
        return (category, confidence)



    def load_image(self, infilename ):
        img = Image.open( infilename )
        img.load()
        # Resize it
        h, w = img.size
        w_new = int(64 * w / max(w, h) )
        h_new = int(64 * h / max(w, h) )
        size = w_new, h_new
        img = img.resize(size)
        data = np.asarray( img, dtype="int32" )
        return data

    def centroid_histogram(self, clt):
    # grab the number of different clusters and create a histogram
    # based on the number of pixels assigned to each cluster
        numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
        (hist, _) = np.histogram(clt.labels_, bins = numLabels)

    # normalize the histogram, such that it sums to one
        hist = hist.astype("float")
        hist /= hist.sum()

    # return the histogram
        return hist

    def check_clt(self,centers):
        if all(i >= 50 and i<155  for i in centers[0]):
            return self.colour_id(centers[1])
        else:
            return self.colour_id(centers[0])

    def colour_id(self, center):
        max_col = np.argmax(center)
        if max_col==0:
            return "RED"
        if max_col==1:
            return "GREEN"
        if max_col==2:
            return "BLUE"



	