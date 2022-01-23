import numpy as np

# class to trim the audio data in the wave file that has zeros at the beginning and end
class Trim:

    def apply_effect(self, data: np.ndarray) -> np.ndarray:
        if len(data.shape) == 1:
            data = data.reshape(-1, 1)
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


