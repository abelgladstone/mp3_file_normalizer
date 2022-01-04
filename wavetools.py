import pathlib
from scipy.io import wavfile
import numpy as np


class BufferedWaveReader:

    def __init__(self, wave_file: pathlib.Path, chunk_size: int = None) -> None:
        self.wave_file = wave_file
        self.data = self.read_data()
        self.chunk_size = chunk_size if chunk_size else len(self)
        # check that the file exists and is a wave file
        if not wave_file.exists():
            raise FileNotFoundError(f"{wave_file} does not exist")
        if wave_file.suffix != ".wav":
            raise ValueError(f"{wave_file} is not a wave file")
    
    # a method to return the sample rate
    def sample_rate(self):
        return wavfile.read(self.wave_file)[0]
    
    def read_data(self):
        _, data = wavfile.read(self.wave_file)
        # convert the data to float32 if it is not already float32
        if data.dtype == np.int16:
            data = self.int16_to_float32(data)
        elif data.dtype == np.int32:
            data = self.int32_to_float32(data)
        self.data = data
    
    ## Override the iterator protocol to provide a generator that yields chunks of data
    def __iter__(self):
        start = 0
        while start < len(self):
            end = min(start + self.chunk_size, len(self))
            yield self.data[start:end]
            start = end
    
    # a method to convert the numpy array from int16 to float32
    def int16_to_float32(self, data: np.ndarray) -> np.ndarray:
        return data.astype(np.float32) / 32768.0
    
    # a method to convert the numpy array from int32 to float32
    def int32_to_float32(self, data: np.ndarray) -> np.ndarray:
        return data.astype(np.float32) / 2147483648.0

    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, index):
        return self.data[index]

    def __str__(self):
        return f"BufferedWaveReader({self.wave_file})"


class BufferedWaveWriter:

    def __init__(self, wave_file: str, sample_rate: int, output_format: str = 'float32') -> None:
        self.wave_file = wave_file
        self.sample_rate = sample_rate
        self.output_format = output_format
        # Initialize the data as a empty np array
        self.data = np.array([])

    def write(self):
        data = np.concatenate(self.data)
        wavfile.write(self.wave_file, self.sample_rate, data)
        self.data = []
    
    def append(self, data: np.ndarray):
        self.data = np.append(self.data, data)
    
    # a method to convert the numpy array to output_format
    def convert_to_output_format(self, data: np.ndarray) -> np.ndarray:
        if self.output_format == 'int16':
            return data.astype(np.int16)
        elif self.output_format == 'int32':
            return data.astype(np.int32)
        elif self.output_format == 'float32':
            return data.astype(np.float32)
        else:
            raise ValueError(f"{self.output_format} is not a valid output format")
    
    def __str__(self):
        return f"BufferedWaveWriter({self.wave_file})"
