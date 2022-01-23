from numpy.core.fromnumeric import nonzero
from scipy.io import wavfile
import numpy as np

from .effect import Effect


#function to export a wave file with a given numpy array, filename and sample rate using scipy
def export_wave(wave_array, file_name, sample_rate):
    wavfile.write(file_name, sample_rate, wave_array)

# a function to read a wave file using scipy and convert it to a numpy array as a float data type
def read_wave(file_name):
    sample_rate, wave_array = wavfile.read(file_name)
    return sample_rate, wave_array

# function to normalize a wave file using scipy, to a given volume below 0 dbFS
# write the normalized wave file to a new file with the same name as the original 
# file but with _norm.wav appended to the end
def normalize_wavefile(input_wavefile, target_volume_db=-3):
    fs, data = read_wave(input_wavefile)
    normalized_data = data / np.max(np.abs(data)) * 10 ** (target_volume_db / 20)
    #saturate the data to the range [-1, 1]
    normalized_data = np.clip(normalized_data, -1, 1)
    # create the new normalized wave file name
    new_file_name = input_wavefile.split('.')[0] + '_norm.wav'
    export_wave(normalized_data, new_file_name, fs)
    return new_file_name


class Normalize(Effect):

    def __init__(self, target_db=-3):
        self.target_db = target_db
        self._linear_gain = 10 ** (self.target_db / 20)
    
    def __str__(self):
        return f"Normalize({self.target_db} dbFS)"

    def apply_effect(self, data: np.ndarray) -> np.ndarray:
        # reshae the data to be a 2D array
        data = self.reshape_to_2d_array(data)
        # get the max value of the data from each channel
        max_values = np.max(np.abs(data), axis=1)
        # get the max value from max_values
        max_value = np.max(max_values)
        # normalize the data by the max value
        normalized_data = data / max_value * self._linear_gain
        # return the normalized data
        return normalized_data
    
    def info_str(self) -> str:
        return str(self)
