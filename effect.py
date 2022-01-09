import abc
import numpy as np

# an abstract class for effects
class Effect(abc.ABC):
    
    @abc.abstractmethod
    def apply_effect(self, data: np.ndarray, **kwargs) -> np.ndarray:
        """ Apply the effect to the data """
    
    def info_str(self) -> str:
        """ Returns a string with information about the effect """
        return ''
    
    def update_progress(self) -> float:
        """ Return the progress of the effect between 0 and 1 """
        return 0