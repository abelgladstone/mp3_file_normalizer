from .effect import Effect
import numpy as np


class Amplify(Effect):
    def __init__(self, gain_dB=0) -> None:
        self.gain_dB = gain_dB
        super().__init__()

    def apply_effect(self, data: np.ndarray) -> np.ndarray:
        return data * (10 ** (self.gain_dB / 20))

    def info_str(self) -> str:
        return f"Amplify {self.gain_dB} dBFS"
