import numpy as np
from sklearn.decomposition import PCA as SKPCA

class PCA:
    def __init__(self, n_components: int):
        self.n_components = n_components
        self.model = SKPCA(n_components=n_components)
    
    def fit_transform(self, data: np.ndarray) -> np.ndarray:
        return self.model.fit_transform(data)
    
    def transform(self, data: np.ndarray) -> np.ndarray:
        return self.model.transform(data)
