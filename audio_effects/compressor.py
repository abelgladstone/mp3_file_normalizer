from dataclasses import dataclass, field
from .detector import DetectorBase, LevelCorrectedPeakDetector, LevelDetector, PeakDetector, RMSDetector, SmoothPeakDetector
from .effect import Effect
import numpy as np
from enum import Enum
import multiprocessing as mp

# and enum for different types of detectors
class DetectorType(Enum):
    LEVEL = 0
    PEAK = 1
    RMS = 2
    SMOOTH_PEAK = 3
    LEVEL_CORRECTED_PEAK = 4

    # a method to return the detector class
    def get_detector(self) -> DetectorBase:
        if self == DetectorType.LEVEL:
            return LevelDetector
        elif self == DetectorType.PEAK:
            return PeakDetector
        elif self == DetectorType.RMS:
            return RMSDetector
        elif self == DetectorType.SMOOTH_PEAK:
            return SmoothPeakDetector
        elif self == DetectorType.LEVEL_CORRECTED_PEAK:
            return LevelCorrectedPeakDetector
        else:
            return None 


@dataclass
class MonoCompressor(Effect):

    attack_msec: float
    release_msec: float
    threshold_db: float
    ratio: int
    knee_db: float
    makeup_gain_db:float = 0
    sample_rate: int = 44100
    detector_type: DetectorType = DetectorType.SMOOTH_PEAK

    def __post_init__(self):
        if self.threshold_db > 0:
            self.threshold_db = 0
        if self.ratio < 1:
            self.ratio = 1
        if self.knee_db < 0:
            self.knee_db = 0
        self.iratio = 1 / self.ratio
        self.knee_start_db = -self.knee_db/2 + self.threshold_db
        self.knee_end_db = self.knee_db/2 + self.threshold_db
        # get the detector class from the detector type
        self.detector_class = self.detector_type.get_detector()
        self.detector = [self.detector_class(self.sample_rate, self.attack_msec/1000, self.release_msec/1000)]
    
    def envelope(self, data: np.ndarray):
        return self.detector[0].apply_effect(data)
    
    # a function to return the gain of the compressor in the knee region
    def gain_knee_region(self, xg):
        return xg + (self.iratio - 1) * (xg - self.threshold_db + self.knee_db/2)**2 / (2 * self.knee_db)
    
    # a function to return the gain of the compressor in the compression region
    def gain_compression_region(self, xg):
        return self.threshold_db + (xg - self.threshold_db) * self.iratio

    def compute_compressor_gain(self, envelope: np.ndarray):
        xg = np.log10(envelope + 0.000001)*20
        yg = xg
        # use numpy where to compute the gain
        compression_indices = np.argwhere(xg > self.knee_end_db)
        knee_indices = np.argwhere( (self.knee_start_db < xg) & (xg <= self.knee_end_db))
        yg[compression_indices] = self.gain_compression_region(xg[compression_indices])
        yg[knee_indices] = self.gain_knee_region(xg[knee_indices])
        return 10**((yg - xg + self.makeup_gain_db) / 20)
    
    def apply_effect(self, data: np.ndarray) -> np.ndarray:
        envelope = self.envelope(data)
        gain = self.gain(envelope)
        return gain * data
    
    def info_str(self) -> str:
        return 'Mono Compressor'


class StereoCompressor(MonoCompressor):

    LEFT = 0
    RIGHT = 1

    def __post_init__(self):
        super().__post_init__()
        self.detector.append(self.detector_class(self.sample_rate, self.attack_msec/1000, self.release_msec/1000))
    
    def apply_detector_channel(self, data: np.ndarray, channel: int):
        # apply the detector to the channel
        return self.detector[channel].apply_effect(data)

    def apply_effect(self, data: np.ndarray) -> np.ndarray:
        # check if the data is stereo
        if len(data.shape) != 2:
            raise ValueError("Data must be stereo")
        # create a pool of workers
        pool = mp.Pool(2)
        # apply the effect to each channel using the pool of workers asynchronously
        results = pool.starmap(self.apply_detector_channel, [(data[:,i], i) for i in range(2)])
        # close the pool of workers
        pool.close()
        # join the pool of workers
        pool.join()
        # get the max of the left and right envelopes
        envelope = np.maximum(results[StereoCompressor.LEFT], results[StereoCompressor.RIGHT])
        gain = self.compute_compressor_gain(envelope)
        # make a gain a single dimension array
        gain = np.reshape(gain, (len(gain), 1))
        return gain * data

    def info_str(self) -> str:
        return "Stereo Compressor"