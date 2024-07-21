import numpy as np
from .pca import PCA
from .kmeans import KMeans
from .isolation_forest import AdaptiveIsolationForest

class StreamingAnomalyDetector:
    def __init__(self, n_clusters: int, n_components: int, n_estimators: int = 100, contamination: float = 0.1):
        self.pca = PCA(n_components)
        self.kmeans = KMeans(n_clusters)
        self.isolation_forest = AdaptiveIsolationForest(n_estimators, contamination)
        self.fitted = False

    def partial_fit(self, data: np.ndarray):
        if not self.fitted:
            reduced_data = self.pca.fit_transform(data)
            self.kmeans.fit_predict(reduced_data)
            self.isolation_forest.fit(reduced_data)
            self.fitted = True
        else:
            reduced_data = self.pca.transform(data)
            self.kmeans.partial_fit(reduced_data)
            self.isolation_forest.model.fit(reduced_data, sample_weight=None)
    
    def predict(self, data: np.ndarray) -> np.ndarray:
        if not self.fitted:
            raise RuntimeError("Model must be fitted before prediction.")
        reduced_data = self.pca.transform(data)
        return self.isolation_forest.predict(reduced_data)
    
    def anomaly_score(self, data: np.ndarray) -> np.ndarray:
        if not self.fitted:
            raise RuntimeError("Model must be fitted before computing anomaly scores.")
        reduced_data = self.pca.transform(data)
        return self.isolation_forest.anomaly_score(reduced_data)
