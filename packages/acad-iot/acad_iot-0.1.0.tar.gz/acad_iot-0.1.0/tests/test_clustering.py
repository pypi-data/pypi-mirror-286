import unittest
import numpy as np
from acad_iot.clustering import AdaptiveKMeans

class TestAdaptiveKMeans(unittest.TestCase):
    def test_clustering(self):
        X = np.random.rand(100, 2)
        kmeans = AdaptiveKMeans(n_clusters=3)
        labels = kmeans.fit(X)
        self.assertEqual(len(labels), 100)

if __name__ == '__main__':
    unittest.main()
