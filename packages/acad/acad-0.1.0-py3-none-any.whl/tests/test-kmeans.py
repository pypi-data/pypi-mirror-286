import numpy as np
from acad.kmeans import KMeans

def test_kmeans():
    data = np.random.rand(100, 2)
    kmeans = KMeans(n_clusters=3)
    labels = kmeans.fit_predict(data)
    assert len(set(labels)) == 3
