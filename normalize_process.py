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

    def __init__(self, target_volume_db=-3, output_format='float32'):
        self.target_volume_db = target_volume_db
        self._linear_gain = 10 ** (self.target_volume_db / 20)
        self.output_format = output_format
    
    def __str__(self):
        return f"Normalize({self.target_volume_db} dbFS {self.output_format})"

    # a method to convert the input data to the output format from float32 to int16 or int32
    def convert_to_output_data(self, data: np.ndarray) -> np.ndarray:
        if self.output_format == 'int16':
            return np.int16(data * 32768)
        elif self.output_format == 'int32':
            return np.int32(data * 2147483648)
        else:
            return data

    # a method to convert the input data to the output format from int16 to float32
    def int16_to_float32(self, data: np.ndarray) -> np.ndarray:
        return np.float32(data) / 32768
    
    # a method to convert the input data to the output format from int32 to float32
    def int32_to_float32(self, data: np.ndarray) -> np.ndarray:
        return np.float32(data) / 2147483648

    def apply_effect(self, data: np.ndarray) -> np.ndarray:
        # convert the data to float32 if it is not already float32
        if data.dtype == np.int16:
            data = self.int16_to_float32(data)
        elif data.dtype == np.int32:
            data = self.int32_to_float32(data)
        # normalize the data
        normalized_data = data / np.max(np.abs(data)) * self._linear_gain
        # saturate the data to the range [-1, 1]
        normalized_data = np.clip(normalized_data, -1, 1)
        # convert the data to the output format
        return self.convert_to_output_data(normalized_data)

