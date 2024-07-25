import unittest
import numpy as np
from acad_iot.anomaly_detection import AdaptiveIsolationForest

class TestAdaptiveIsolationForest(unittest.TestCase):
    def test_anomaly_detection(self):
        X = np.random.rand(100, 2)
        isolation_forest = AdaptiveIsolationForest()
        isolation_forest.fit(X)
        predictions = isolation_forest.predict(X)
        self.assertEqual(len(predictions), 100)

if __name__ == '__main__':
    unittest.main()
