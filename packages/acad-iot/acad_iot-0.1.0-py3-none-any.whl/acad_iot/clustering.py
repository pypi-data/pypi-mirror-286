from sklearn.cluster import KMeans
import numpy as np

class AdaptiveKMeans:
    def __init__(self, n_clusters=3):
        self.n_clusters = n_clusters
        self.model = KMeans(n_clusters=self.n_clusters)
    
    def fit(self, X):
        self.model.fit(X)
        return self.model.labels_

    def predict(self, X):
        return self.model.predict(X)
