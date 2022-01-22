import unittest
from audio_effects.clip import SoftClip, HardClip, FullScaleSoftClip
import numpy as np

class TestHardClip(unittest.TestCase):

    def test_hardclip(self):
        # create a random array of floats between -8 and 8
        data = (np.random.random(10000) - 0.5) * 16
        # create a hard clip object
        clip_obj = HardClip()
        # apply the hard clip audio effect to the data
        clip_data = clip_obj.apply_effect(data)
        # check that the data is between -1 and 1
        self.assertTrue(np.all(np.abs(clip_data) <= 1))
        # check that the data is not all zeros
        self.assertFalse(np.all(clip_data == 0))
    

class TestSoftClip(unittest.TestCase):

    def test_softclip(self):
        # create a random array of floats between -8 and 8
        data = (np.random.random(10000) - 0.5) * 16
        # create a soft clip object
        clip_obj = SoftClip()
        # apply the soft clip audio effect to the data
        clip_data = clip_obj.apply_effect(data)
        # check that the data is between -2/3 and 2/3
        self.assertTrue(np.all(np.abs(clip_data) <= 2/3))
        # check that the data is not all zeros
        self.assertFalse(np.all(clip_data == 0))
        # create a square wave of frequency 1 and sample rate of 100 and duty cycle of 0.5
        square_wave = np.sin(np.linspace(0, 1, 1000))
        # apply the soft clip audio effect to the square wave
        clip_data = clip_obj.apply_effect(square_wave)
        # check that the data is between -2/3 and 2/3
        self.assertTrue(np.all(np.abs(clip_data) <= 2/3))
        # check that the data is not all zeros
        self.assertFalse(np.all(clip_data == 0))
        # get the data from the clip_data where the data is greater than 0 and less than 1
        clip_data = clip_data[np.where(np.logical_and(clip_data > 0, clip_data < 1))]
        # check that there are some values in the data
        self.assertTrue(len(clip_data) > 0)
    
class TestFullScaleSoftClip(unittest.TestCase):

    def test_fullscale_softclip(self):
        # create a random array of floats between -8 and 8
        data = (np.random.random(10000) - 0.5) * 16
        # create a full scale soft clip object
        clip_obj = FullScaleSoftClip()
        # apply the full scale soft clip audio effect to the data
        clip_data = clip_obj.apply_effect(data)
        # check that the data is between -1 and 1
        self.assertTrue(np.all(np.abs(clip_data) <= 1))
        # check that the data is not all zeros
        self.assertFalse(np.all(clip_data == 0))
        # find the data where the data is greater than clip_obj.smoothing_radius and less than 1
        clip_data = clip_data[np.where(np.logical_and(clip_data > clip_obj.smoothing_radius, clip_data < 1))]
        # check that there are some values in the data
        self.assertTrue(len(clip_data) > 0)


if __name__ == '__main__':
    unittest.main()