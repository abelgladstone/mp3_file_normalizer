import pathlib
from scipy.io import wavfile
import numpy as np


class BufferedWaveReader:

    def __init__(self, wave_file: str, chunk_size: int = None) -> None:
        self.wave_file = wave_file
        self.read_data()
        self.chunk_size = chunk_size if chunk_size else len(self)
        # check that the file exists and is a wave file
        if not pathlib.Path(self.wave_file).exists():
            raise FileNotFoundError(f"{wave_file} does not exist")
        if pathlib.Path(self.wave_file).suffix != ".wav":
            raise ValueError(f"{wave_file} is not a wave file")
    
    # a method to return the sample rate
    def sample_rate(self)->int:
        return wavfile.read(self.wave_file)[0]
    
    def read_data(self):
        _, data = wavfile.read(self.wave_file)
        self.data = data
    
    ## Override the iterator protocol to provide a generator that yields chunks of data
    def __iter__(self):
        start = 0
        while start < len(self):
            end = min(start + self.chunk_size, len(self))
            yield self.data[start:end]
            start = end

    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, index):
        return self.data[index]

    def __str__(self):
        return f"BufferedWaveReader({self.wave_file}, Sample Rate: {self.sample_rate()}, Chunk Size: {self.chunk_size}, Length: {len(self)}, data_type: {self.data.dtype})"


class BufferedWaveWriter:

    def __init__(self, wave_file: str, sample_rate: int) -> None:
        self.wave_file = wave_file
        self.sample_rate = sample_rate
        # Initialize the data as a empty np array
        self.data = np.array([])

    def write(self):
        wavfile.write(self.wave_file, self.sample_rate, self.data)
        self.data = []
    
    def append(self, data: np.ndarray):
        self.data = np.append(self.data, data)
    
    def __str__(self):
        return f"BufferedWaveWriter({self.wave_file}, Sample Rate: {self.sample_rate()})"