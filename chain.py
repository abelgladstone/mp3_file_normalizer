from compressor import StereoCompressor
from normalize_process import Normalize, Trim
from mp3tools import convert_mp3_to_wav, convert_wav_to_mp3
from clip import HardClip, SoftClip
from wavetools import BufferedWaveReader, BufferedWaveWriter
from audioformat import Float64
import time
import os


# dictionary to create compressor objects
compressor_config = {
    'attack_msec': 10,
    'release_msec': 200,
    'threshold_db': -10,
    'ratio': 3,
    'knee_db': 3,
    'makeup_gain_db': 4,
    'sample_rate': 44100,
}

normalize_config = {
    'target_db': -3,
}

# function to apply the effects to a wave file
def apply_effects(input_wavefile, output_wavefile):
    reader = BufferedWaveReader(input_wavefile)
    compressor_config['sample_rate'] = reader.sample_rate()
    operators = [Float64(), Trim(), StereoCompressor(**compressor_config), Normalize(**normalize_config), HardClip()]
    writer = BufferedWaveWriter(output_wavefile, reader.sample_rate())
    data = reader.data
    for operator in operators:
        # store the time before the operator
        start_time = time.time()
        data = operator.apply_effect(data)
        # store the time after the operator
        end_time = time.time()
        print(f'{operator.info_str()} Time: {end_time - start_time:.2f} seconds')
    writer.append(data)
    writer.write()

# a function called main to run the program
def main():
    # convert the mp3 file to a wav file
    convert_mp3_to_wav('GT2021-12-20.mp3', 'test.wav')
    # apply the effects to the wav file
    apply_effects('test.wav', 'test_out.wav')
    # convert the wav file back to an mp3 file
    convert_wav_to_mp3('test_out.wav', 'test_out.mp3')
    # delete the wav file
    os.remove('test.wav')
    os.remove('test_out.wav')



if __name__ == '__main__':
    main()
    