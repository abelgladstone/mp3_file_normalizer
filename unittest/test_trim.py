import unittest
from audio_effects.trim import Trim
import numpy as np

class TestTrim(unittest.TestCase):

    def test_trim(self):
        # create a random array of floats between -0.5 and 0.5
        test_data = (np.random.random(10) - 0.5) * 2
        # make sure that the first and last values are not 0
        test_data[0] = 1
        test_data[-1] = 1
        # append 400 zeros to the beginning and end of the data
        data = np.append(np.zeros(400), test_data)
        data = np.append(data, np.zeros(400))
        # create a trim object
        trim_obj = Trim()
        # apply the trim audio effect to the data
        trim_data = trim_obj.apply_effect(data).reshape(test_data.shape)
        # check that the trimmed data is the same as the original data except for the last value
        self.assertTrue(np.all(trim_data.reshape(test_data.shape) == test_data))
    
    def test_trim_multichan(self):
        # create a random array of floats between -0.5 and 0.5 for 4 channels
        test_data = (np.random.random((10, 4)) - 0.5) * 2
        # make sure that the first and last values are not 0
        test_data[0] = 1
        test_data[-1] = 1
        # append 400 zeros to the beginning and end of the data
        data = np.append(np.zeros((400, 4)), test_data, axis=0)
        data = np.append(data, np.zeros((400, 4)), axis=0)
        # create a trim object
        trim_obj = Trim()
        # apply the trim audio effect to the data
        trim_data = trim_obj.apply_effect(data).reshape(test_data.shape)
        # check that the trimmed data is the same as the original data except for the last value
        self.assertTrue(np.all(trim_data.reshape(test_data.shape) == test_data))

if __name__ == '__main__':
    unittest.main()