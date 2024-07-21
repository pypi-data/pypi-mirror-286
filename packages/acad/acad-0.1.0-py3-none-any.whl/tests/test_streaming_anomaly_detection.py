import numpy as np
from acad.streaming_anomaly_detection import StreamingAnomalyDetector

def test_streaming_anomaly_detector():
    data_batch_1 = np.random.rand(50, 10)
    data_batch_2 = np.random.rand(50, 10)
    
    streaming_anomaly_detector = StreamingAnomalyDetector(n_clusters=3, n_components=2, n_estimators=50, contamination=0.1)
    
    streaming_anomaly_detector.partial_fit(data_batch_1)
    predictions_batch_1 = streaming_anomaly_detector.predict(data_batch_1)
    assert len(set(predictions_batch_1)) == 2
    
    streaming_anomaly_detector.partial_fit(data_batch_2)
    predictions_batch_2 = streaming_anomaly_detector.predict(data_batch_2)
    assert len(set(predictions_batch_2)) == 2
