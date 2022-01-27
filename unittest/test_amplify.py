import unittest
from audio_effects.amplify import Amplify
import numpy as np


class Test_amplify(unittest.TestCase):
    def test_amplify(self):
        # create a random array of floats between -1 and 1
        data = np.random.rand(10) * 2 - 1
        # calculate the rms of the data
        rms_data = np.sqrt(np.mean(data ** 2))
        # calculate the rms in dB for rms_data
        rms_db = 20 * np.log10(rms_data)
        # create an amplifier object
        amplifier = Amplify(gain_dB=10)
        # apply_effect the amplifier to the data
        amplified_data = amplifier.apply_effect(data)
        # calculate the rms of the data
        amplified_rms_data = np.sqrt(np.mean(amplified_data ** 2))
        # calculate the rms in dB for rms_data
        amplified_rms_db = 20 * np.log10(amplified_rms_data)
        # check if the rms is increased by almost 10 dB
        self.assertAlmostEqual(rms_db + 10, amplified_rms_db, delta=0.1)
        # create 4 input channels
        data = np.random.rand(10, 4) * 2 - 1
        # calculate the rms of the data for each channel
        rms_data = np.sqrt(np.mean(data ** 2, axis=0))
        # calculate the rms in dB for rms_data
        rms_db = 20 * np.log10(rms_data)
        # apply_effect the amplifier to the data
        amplified_data = amplifier.apply_effect(data)
        # calculate the rms of the data for each channel
        amplified_rms_data = np.sqrt(np.mean(amplified_data ** 2, axis=0))
        # calculate the rms in dB for rms_data
        amplified_rms_db = 20 * np.log10(amplified_rms_data)
        # check if the rms is increased by almost 10 dB for each channel
        for i in range(4):
            self.assertAlmostEqual(rms_db[i] + 10, amplified_rms_db[i], delta=0.1)
