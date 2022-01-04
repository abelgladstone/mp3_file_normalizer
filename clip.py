from effect import Effect
import numpy as np

class HardClip(Effect):

    def apply_effect(self, data: np.ndarray) -> np.ndarray:
        return np.clip(data, -1, 1)


class SoftClip(Effect):

    def apply_effect(self, data: np.ndarray) -> np.ndarray:
        output = np.zeros_like(data)
        # apply the cubic function for each sample
        for i, sample in enumerate(data):
            if sample < -1:
                output[i] = -2/3
            elif sample > 1:
                output[i] = 2/3
            else:
                output[i] = sample - sample**3/3
        return output
