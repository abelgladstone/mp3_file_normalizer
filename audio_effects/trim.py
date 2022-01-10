import numpy as np
from .effect import Effect

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
            start_index = min(start_index, np.nonzero(data[:, channel])[0][0])
            # find the index of the last non-zero value in the data in each channel
            end_index = max(end_index, np.nonzero(data[:, channel])[0][-1])
        # trim the data to the start and end index
        return data[start_index:end_index + 1, :]
    
    def info_str(self) -> str:
        return 'Trim'


