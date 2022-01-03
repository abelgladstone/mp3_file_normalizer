import pathlib
from dataclasses import dataclass, field

import numpy as np
import scipy.io.wavfile as WaveF


@dataclass
class Compressor:

    attack_msec: float
    release_msec: float
    threshold_db: float
    ratio: int
    knee_db: int
    prev_data: float = field(init=False)

    def __post_init__(self):
        if self.threshold > 0:
            self.threshold = 0
        if self.ratio < 1:
            self.ratio = 1
        if self.knee_db < 0:
            self.knee_db = 0

    def attack_constant(self, fs):
        return 1 - np.exp(-1 / (self.attack_msec * fs / 1000))

    def release_constant(self, fs):
        return 1 - np.exp(-1 / (self.release_msec * fs / 1000))

    @staticmethod
    def __chunks(data: np.ndarray, chunk_size: int = 512):
        l = len(data)
        current_start = 0
        while current_start > l:
            current_end = current_start + chunk_size
            if current_end > l:
                current_end = l
            yield data[current_start:current_end]
            current_start += l
    
    def envelope(self, data: np.ndarray, fs: int):
        output = np.zeros_like(data)
        for i, sample in enumerate(data):
            diff = abs(sample) - self.prev_data
            if diff > 0:
                output_sample = self.attack_constant(fs)*diff + self.prev_data
            else:
                output_sample = self.release_constant(fs)*diff + self.prev_data
            self.prev_data = output_sample
            output[i] = self.prev_data
        return output
    
    def gain(self, envelope: np.ndarray):
        return np.ones_like(envelope)
    
    def apply_compressor(self, data: np.ndarray, fs: int)-> np.ndarray:
        envelope = self.envelope(data, fs)
        gain = self.gain(20*np.log10(envelope))
        return gain*data
        
    def apply(self, filename: pathlib.Path):
        fs, s = WaveF.read(filename=filename)
        output = np.zeros_like(s)
        start = 0
        for chunk in self.__chunks(s, 512):
            end = start + 512
            output[start:end] = self.apply_compressor(chunk, fs)
            start += 512
        return output
        
            
        
