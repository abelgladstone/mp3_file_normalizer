from effect import Effect
import numpy as np
import multiprocessing as mp

class HardClip(Effect):

    def apply_effect(self, data: np.ndarray) -> np.ndarray:
        return np.clip(data, -1, 1)
    
    def __str__(self) -> str:
        return self.info_str()


class SoftClip(Effect):

    MAX_SAMPLE = 2/3
    MIN_SAMPLE = -2/3

    # a method to apply the effect to the data
    @staticmethod
    def apply_sample(sample: float) -> float:
        #apply the cubic function for each sample
        if sample < -1:
            return SoftClip.MIN_SAMPLE
        elif sample > 1:
            return SoftClip.MAX_SAMPLE
        else:
            return sample - sample**3/3

    def apply_effect(self, data: np.ndarray) -> np.ndarray:
        # make pool of workers
        pool = mp.Pool(mp.cpu_count())
        # apply the effect to each sample
        output = pool.map(SoftClip.apply_sample, data)
        # close the pool
        pool.close()
        # wait for the pool to finish
        pool.join()
        return np.array(output)

    def info_str(self) -> str:
        return "SoftClip"