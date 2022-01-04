import abc
from typing import Protocol
import numpy as np

# an abstract class for effects
class Effect(abc.ABC):
    
    @abc.abstractmethod
    def apply_effect(self, data: np.ndarray) -> np.ndarray:
        ...