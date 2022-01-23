from .effect import Effect
import numpy as np


class HardClip(Effect):

    def apply_effect(self, data: np.ndarray) -> np.ndarray:
        return np.clip(data, -1, 1)
    
    def __str__(self) -> str:
        return "Hard Clip"
    
    def info_str(self) -> str:
        return "Hard Clip"


class SoftClip(Effect):

    def apply_effect(self, sound_data: np.ndarray) -> np.ndarray:
        sound_data = self.reshape_to_2d_array(sound_data)
        output = np.zeros_like(sound_data)
        num_channels = sound_data.shape[1]
        for channel in range(num_channels):
            # replace all the values in data >= 1 with 2/3
            output[np.where(sound_data[:, channel] >= 1), channel] = 2/3
            # replace all the values in data <= -1 with -2/3
            output[np.where(sound_data[:, channel] <= -1), channel] = -2/3
            # find the indices where the data is between -1 and 1
            indices = np.where(np.logical_and(sound_data[:, channel] > -1, sound_data[:, channel] < 1))
            # apply the cubic function the data between -1 and 1
            output[indices, channel] = sound_data[indices, channel] - (1/3)*np.power(sound_data[indices, channel], 3)
        return output

    def info_str(self) -> str:
        return "SoftClip"


class FullScaleSoftClip(Effect):
    """ Imspired by the radius of smooth knee of a compressor
    Here we assume that the ratio is infinity"""

    def __init__(self, smoothing_radius = 0.1) -> None:
        super().__init__()
        self.smoothing_radius = smoothing_radius
        # raise a value error if the smoothing radius is not between 0 and 1
        if not (0 <= self.smoothing_radius <= 1):
            raise ValueError("The smoothing radius must be between 0 and 1")

    def apply_effect(self, sound_data: np.ndarray) -> np.ndarray:
        T = 1
        width = self.smoothing_radius
        # reshape the data to a 2D array
        sound_data = self.reshape_to_2d_array(sound_data)
        output = np.copy(sound_data)
        num_channels = sound_data.shape[1]
        # iterate over the channels
        for channel in range(num_channels):
            output[np.where(sound_data[:, channel] > (width/2 + T)), channel] = 1
            output[np.where(sound_data[:, channel] < (-width/2 - T)), channel] = -1
            # find the indices where the data is between (-width/2 + T) and (width/2 + T)
            indices = np.where(np.logical_and(sound_data[:, channel] >= (-width/2 + T), sound_data[:, channel] <= (width/2 + T)))
            # apply the second order interpolation function to the data between (-width/2 + T) and (width/2 + T)
            output[indices, channel] = sound_data[indices, channel] - ((sound_data[indices, channel] - T + width/2)**2)/(2*width)
            # find the indices where the data is between (-width/2 - T) and (-width/2 + T)
            indices = np.where(np.logical_and(-sound_data[:, channel] >= (-width/2 + T), -sound_data[:, channel] <= (width/2 + T)))
            # apply the second order interpolation function to the data between (-width/2 - T) and (-width/2 + T)
            output[indices, channel] = sound_data[indices, channel] + ((sound_data[indices, channel] + T - width/2)**2)/(2*width)
        return output
    
    def info_str(self) -> str:
        return "Full Scale Soft Clip"
