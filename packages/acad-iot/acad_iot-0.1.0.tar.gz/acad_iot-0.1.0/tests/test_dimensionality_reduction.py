import unittest
import numpy as np
from acad_iot.dimensionality_reduction import PCAWrapper

class TestPCAWrapper(unittest.TestCase):
    def test_pca(self):
        X = np.random.rand(100, 5)
        pca = PCAWrapper(n_components=2)
        X_transformed = pca.fit_transform(X)
        self.assertEqual(X_transformed.shape[1], 2)

if __name__ == '__main__':
    unittest.main()
