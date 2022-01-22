import unittest
from audio_effects.normalize import Normalize
import numpy as np

# class to test the normalize audio effect
class TestNormalize(unittest.TestCase):
    # function to test the normalize audio effect
    def test_normalize(self):
        # create a random array of floats between -0.5 and 0.5
        data = (np.random.random(10000) - 0.5) * 2
        # create a normalize object
        normalize_obj = Normalize(target_db=0)
        # apply the normalize audio effect to the data
        normalize_data = normalize_obj.apply_effect(data)
        # check that the data is between -1 and 1
        self.assertTrue(np.all(np.abs(normalize_data) <= 1))
        # check that the data is not all zeros
        self.assertFalse(np.all(normalize_data == 0))
        # create a new normalize object
        normalize_obj = Normalize(target_db=-10)
        # apply the normalize audio effect to the data
        normalize_data = normalize_obj.apply_effect(data)
        # check that the max data is -10 dBFS
        self.assertTrue(np.max(normalize_data) <= np.exp(-10 / 20))


if __name__ == '__main__':
    unittest.main()

