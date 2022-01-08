from dataclasses import dataclass, field
from detector import DetectorBase, LevelCorrectedPeakDetector, LevelDetector, PeakDetector, RMSDetector, SmoothPeakDetector
from effect import Effect
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
        self.detector = self.detector_class(self.sample_rate, self.attack_msec/1000, self.release_msec/1000)
        self.linear_makeup_gain = 10**(self.makeup_gain_db/20)
    
    def envelope(self, data: np.ndarray):
        return self.detector.apply_effect(data)
    
    def _compute_compressor_gain_sample(self, input_envelope):
        xg = np.log10(input_envelope + 0.000001)*20
        if xg < self.knee_start_db:
            yg = xg
        elif self.knee_start_db < xg <= self.knee_end_db:
            yg = xg + (self.iratio - 1) * (xg - self.threshold_db + self.knee_db/2)**2 / (2 * self.knee_db)
        else:
            yg = self.threshold_db + (xg - self.threshold_db) * self.iratio
        return 10**((yg - xg)/20)
    
    def compute_compressor_gain(self, envelope: np.ndarray):
        # Computer the gain from the envelope and return the array of gains
        vector_func = np.vectorize(self._compute_compressor_gain_sample)
        return vector_func(envelope)
    
    def apply_effect(self, data: np.ndarray) -> np.ndarray:
        envelope = self.envelope(data)
        gain = self.gain(envelope)
        return gain * data * self.linear_makeup_gain
    
    def info_str(self) -> str:
        return 'Mono Compressor'


class StereoCompressor(MonoCompressor):

    LEFT = 0
    RIGHT = 1

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
        self.detector_class = self.detector_type.get_detector()
        self.detector = [self.detector_class(self.sample_rate, self.attack_msec/1000, self.release_msec/1000) for i in range(2)]
        self.linear_makeup_gain = 10**(self.makeup_gain_db/20)
    
    def apply_detector_channel(self, data: np.ndarray, channel: int):
        # apply the detector to the channel
        envelope = self.detector[channel].apply_effect(data)
        return envelope

    def apply_effect(self, data: np.ndarray) -> np.ndarray:
        # check if the data is stereo
        if len(data.shape) != 2:
            raise ValueError("Data must be stereo")
        # create a pool of workers
        pool = mp.Pool(2)
        # apply the effect to each channel using the pool of workers asynchronously
        results = pool.starmap(self.apply_detector_channel, [(data[:,i], i) for i in range(2)])
        # get the max of the left and right envelopes
        envelope = np.maximum(results[StereoCompressor.LEFT], results[StereoCompressor.RIGHT])
        gain = self.compute_compressor_gain(envelope) * self.linear_makeup_gain
        # make a gain a single dimension array
        gain = np.reshape(gain, (len(gain), 1))
        return gain * data

    def info_str(self) -> str:
        return "Stereo Compressor"