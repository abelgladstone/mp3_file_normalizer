from dataclasses import dataclass, field
from detector import DetectorBase, LevelCorrectedPeakDetector, LevelDetector, PeakDetector, RMSDetector, SmoothPeakDetector
from effect import Effect
import numpy as np
from enum import Enum

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
class Compressor(Effect):

    attack_msec: float
    release_msec: float
    threshold_db: float
    ratio: int
    knee_db: int
    detector_type: DetectorType = DetectorType.SMOOTH_PEAK
    sample_rate: int = 44100
    prev_data: float = field(init=False)

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
    
    def envelope(self, data: np.ndarray):
        return self.detector.apply(data)
    
    def gain(self, envelope: np.ndarray):
        # Computer the gain from the envelope and return the array of gains
        output = np.zeros_like(envelope)
        for i, sample in enumerate(envelope):
            xg = np.log10(sample + 0.000001)*20
            # see if we are below the knee
            if xg < self.knee_start_db:
                yg = xg
            elif self.knee_start_db < xg <= self.knee_end_db:
                yg = xg + (self.iratio - 1) * (xg - self.threshold_db + self.knee_db/2)**2 / (2 * self.knee_db)
            else:
                yg = self.threshold_db + (xg - self.threshold_db) * self.iratio
            output[i] = 10**((yg - xg)/20)
        return output
    
    def apply_effect(self, data: np.ndarray) -> np.ndarray:
        envelope = self.envelope(data)
        gain = self.gain(envelope)
        return gain * data
