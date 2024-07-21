import numpy as np
from sklearn.ensemble import IsolationForest

class AdaptiveIsolationForest:
    def __init__(self, n_estimators: int = 100, contamination: float = 0.1):
        self.model = IsolationForest(n_estimators=n_estimators, contamination=contamination)
    
    def fit(self, data: np.ndarray):
        self.model.fit(data)
    
    def predict(self, data: np.ndarray) -> np.ndarray:
        return self.model.predict(data)
    
    def anomaly_score(self, data: np.ndarray) -> np.ndarray:
        return self.model.decision_function(data)
