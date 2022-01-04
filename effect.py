from typing import Protocol
import numpy as np

# an abstract class for effects
class Effect(Protocol):
    
    def apply_effect(self, data: np.ndarray) -> np.ndarray:
        ...