import numpy as np
from acad.anomaly_detection import AnomalyDetector

def test_anomaly_detector():
    data = np.random.rand(100, 10)
    anomaly_detector = AnomalyDetector(n_clusters=3, n_components=2, n_estimators=50, contamination=0.1)
    anomaly_detector.fit(data)
    predictions = anomaly_detector.predict(data)
    assert len(set(predictions)) == 2
