import numpy as np
from sklearn.cluster import MiniBatchKMeans

class KMeans:
    def __init__(self, n_clusters: int):
        self.n_clusters = n_clusters
        self.model = MiniBatchKMeans(n_clusters=n_clusters)
    
    def fit_predict(self, data: np.ndarray) -> np.ndarray:
        return self.model.fit_predict(data)
    
    def predict(self, data: np.ndarray) -> np.ndarray:
        return self.model.predict(data)

    def partial_fit(self, data: np.ndarray):
        self.model.partial_fit(data)
