import numpy as np
from effect import Effect

class DetectorBase(Effect):

    def __init__(self, sample_rate) -> None:
        self.sample_rate = sample_rate
        self.prev_data = 0
    
    def apply_effect(self, data):
        pass


# A level detector class which inherits from the base class
class LevelDetector(DetectorBase):

    # override the __init__ method
    def __init__(self, sample_rate, time_constant) -> None:
        super().__init__(sample_rate)
        self.time_constant = time_constant
    
    # a property called alpha
    @property
    def alpha(self):
        return np.exp(-1 / (self.time_constant * self.sample_rate))

    #override the apply_effect method
    def apply_effect(self, data: np.ndarray):
        output = np.zeros_like(data)
        for i, sample in enumerate(data):
            # rectify the signal
            sample = abs(sample)
            output[i] = self.alpha * self.prev_data + (1 - self.alpha) * sample
            self.prev_data = output[i]
        return output


class RMSDetector(DetectorBase):

    def __init__(self, sample_rate, time_constant) -> None:
        super().__init__(sample_rate)
        self.time_constant = time_constant
    
    @property
    def alpha(self):
        return np.exp(-1 / (self.time_constant * self.sample_rate))

    def apply_effect(self, data: np.ndarray):
        output = np.zeros_like(data)
        for i, sample in enumerate(data):
            output[i] = self.alpha * self.prev_data + (1 - self.alpha) * sample**2
            self.prev_data = output[i]
        return output


class PeakDetector(DetectorBase):

    def __init__(self, sample_rate, attack_time, release_time) -> None:
        super().__init__(sample_rate)
        self.attack_time = attack_time
        self.release_time = release_time
    
    @property
    def attack_constant(self):
        return np.exp(-1 / (self.attack_time * self.sample_rate))
    
    @property
    def release_constant(self):
        return np.exp(-1 / (self.release_time * self.sample_rate))
    
    def apply_effect(self, data: np.ndarray):
        output = np.zeros_like(data)
        for i, sample in enumerate(data):
            # rectify the signal
            sample = abs(sample)
            output[i] = self.release_constant * self.prev_data + (1 -self.attack_constant)*np.max(sample - self.prev_data, 0)
            self.prev_data = output[i]
        return output
    
class LevelCorrectedPeakDetector(DetectorBase):

    def __init__(self, sample_rate, attack_time, release_time) -> None:
        super().__init__(sample_rate)
        self.attack_time = attack_time
        self.release_time = release_time
    
    @property
    def attack_constant(self):
        return np.exp(-1 / (self.attack_time * self.sample_rate))
    
    @property
    def release_constant(self):
        return np.exp(-1 / (self.release_time * self.sample_rate))
    
    def apply_effect(self, data: np.ndarray):
        output = np.zeros_like(data)
        for i, sample in enumerate(data):
            # rectify the signal
            sample = abs(sample)
            if sample > self.prev_data:
                output[i] = self.attack_constant*self.prev_data + (1 - self.attack_constant)*sample
            else:
                output[i] = self.release_constant*self.prev_data
            self.prev_data = output[i]
        return output


class SmoothPeakDetector(DetectorBase):

    def __init__(self, sample_rate, attack_time, release_time) -> None:
        super().__init__(sample_rate)
        self.attack_time = attack_time
        self.release_time = release_time
    
    @property
    def attack_constant(self):
        return 1 - np.exp(-1 / (self.attack_time * self.sample_rate))
    
    @property
    def release_constant(self):
        return 1 - np.exp(-1 / (self.release_time * self.sample_rate))
    
    def apply_effect(self, data: np.ndarray):
        output = np.zeros_like(data)
        for i in range(len(data)):
            # rectify the signal
            diff = abs(data[i]) - self.prev_data
            if diff > 0:
                self.prev_data += self.attack_constant*diff
            else:
                self.prev_data += self.release_constant*diff
            output[i] = self.prev_data
        return output


# a function to generate a square wave and return the data with a given sample rate and frequency
def generate_square_wave(sample_rate, frequency, duration = 1):
    # generate the time
    time = np.linspace(0, duration, sample_rate*duration)
    # Generate an input square wave with a frequency of 10 Hz
    data = (np.sin(2 * np.pi * frequency * time) > 0)
    # scale the data to be between -1 and 1
    data = data * 2 - 1
    return data

# a function to generate a sine wave and return the data with a given sample rate and frequency
def generate_sine_wave(sample_rate, frequency, duration):
    # generate the time
    time = np.linspace(0, duration, sample_rate*duration)
    # Generate an input sine wave with a frequency of 10 Hz
    data = np.sin(2 * np.pi * frequency * time)
    return data


# A function called main
def main():
    from matplotlib import pyplot as plt
    # set attack and release times
    attack_time = 0.001
    release_time = 0.25
    # time T is 1 second
    T = 1
    # set the sample rate
    sample_rate = 44100
    # generate the time
    time = np.linspace(0, T, sample_rate*T)
    # Generate an input square wave with a frequency of 10 Hz
    data = generate_sine_wave(sample_rate, 10, T)
    # mutiply half of the data by 0.001
    half_data_index = int(len(data)/2)
    data[-half_data_index:] = data[-half_data_index:] * 0.1
    # create a level detector object
    level_detector = LevelDetector(sample_rate, attack_time)
    # apply_effect the level detector to the data
    level_data = level_detector.apply_effect(data)
    # create a rms detector object
    rms_detector = RMSDetector(sample_rate, attack_time)
    # apply_effect the rms detector to the data
    rms_data = rms_detector.apply_effect(data)
    # create a peak detector object
    peak_detector = PeakDetector(sample_rate, attack_time, release_time)
    # apply_effect the peak detector to the data
    peak_data = peak_detector.apply_effect(data)
    # create a level corrected peak detector object
    level_corrected_peak_detector = LevelCorrectedPeakDetector(sample_rate, attack_time, release_time)
    # apply_effect the level corrected peak detector to the data
    level_corrected_peak_data = level_corrected_peak_detector.apply_effect(data)
    # create a smooth peak detector object
    smooth_peak_detector = SmoothPeakDetector(sample_rate, attack_time, release_time)
    # apply_effect the smooth peak detector to the data
    smooth_peak_data = smooth_peak_detector.apply_effect(data)
    # plot the data
    plt.plot(time, data, label='Input')
    plt.plot(time, level_data, label='Level')
    plt.plot(time, rms_data, label='RMS')
    plt.plot(time, peak_data, label='Peak')
    plt.plot(time, level_corrected_peak_data, label='Level Corrected Peak')
    plt.plot(time, smooth_peak_data, label='Smooth Peak')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    main()
