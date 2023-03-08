import unittest
import logisticRegression
import numpy as np


class Tests(unittest.TestCase):

    def test_initialize_weights_and_bias(self):
        w, b = logisticRegression.initialize_weights_and_bias(5)
        testAnsVal = np.full((5, 1), 0.01)
        ans = True

        for index in range(5):
            if (testAnsVal[index] != w[index]):
                ans = False
                break;
        
        self.assertEqual(ans, True)
        self.assertEqual(b, 0.0)

    def test_sigmoid(self):
        self.assertEqual(logisticRegression.sigmoid(9), 0.9998766054240137)

unittest.main(argv=[''], exit=False)
