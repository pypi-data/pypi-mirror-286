import numpy as np
from acad.pca import PCA

def test_pca():
    data = np.random.rand(100, 10)
    pca = PCA(n_components=2)
    transformed_data = pca.fit_transform(data)
    assert transformed_data.shape == (100, 2)
