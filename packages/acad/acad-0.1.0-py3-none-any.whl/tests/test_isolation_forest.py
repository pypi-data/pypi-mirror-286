import numpy as np
from acad.isolation_forest import AdaptiveIsolationForest

def test_isolation_forest():
    data = np.random.rand(100, 2)
    isolation_forest = AdaptiveIsolationForest(n_estimators=50, contamination=0.1)
    isolation_forest.fit(data)
    predictions = isolation_forest.predict(data)
    assert len(set(predictions)) == 2
