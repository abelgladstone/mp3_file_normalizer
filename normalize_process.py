from numpy.core.fromnumeric import nonzero
from scipy.io import wavfile
import numpy as np

from effect import Effect


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
        # get the maximum absolute value of the data in a numpy array
        max_abs_data = np.max(np.abs(data))
        # normalize the data to the target volume
        return data / max_abs_data * self._linear_gain
    
    def info_str(self) -> str:
        return str(self)


# class to trim the audio data in the wave file that has zeros at the beginning and end
class Trim(Effect):

    def apply_effect(self, data: np.ndarray) -> np.ndarray:
        # find the number of channels in the data
        num_channels = data.shape[1]
        # find the index of the first non-zero value in the data in each channel
        start_index = data.shape[0]
        end_index = 0
        for channel in range(num_channels):
            # find the index of the first non-zero value in the data in each channel
            start_index = min(start_index, nonzero(data[:, channel])[0][0])
            # find the index of the last non-zero value in the data in each channel
            end_index = max(end_index, nonzero(data[:, channel])[0][-1])
        # trim the data to the start and end index
        return data[start_index:end_index + 1, :]
    
    def info_str(self) -> str:
        return 'Trim'


