from effect import Effect
import numpy as np


class HardClip(Effect):

    def apply_effect(self, data: np.ndarray) -> np.ndarray:
        return np.clip(data, -1, 1)
    
    def __str__(self) -> str:
        return "Hard Clip"
    
    def info_str(self) -> str:
        return "Hard Clip"


class SoftClip(Effect):

    def apply_effect(self, data: np.ndarray) -> np.ndarray:
        # Hard clip the data
        clipped_data = HardClip().apply_effect(data)
        # apply the cubic function to smooth the clipped data
        clipped_data = clipped_data - (clipped_data**3)/3
        # return the rescaled clipped data
        return clipped_data * 1.5   

    def info_str(self) -> str:
        return "SoftClip"