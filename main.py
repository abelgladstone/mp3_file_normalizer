import numpy as np
import scipy.io.wavfile
import subprocess
import argparse
import datetime

#function to export a wave file with a given numpy array, filename and sample rate using scipy
def export_wave(wave_array, file_name, sample_rate):
    scipy.io.wavfile.write(file_name, sample_rate, wave_array)

# a function to read a wave file using scipy and convert it to a numpy array as a float data type
def read_wave(file_name):
    sample_rate, wave_array = scipy.io.wavfile.read(file_name)
    return sample_rate, wave_array

# function to normalize a wave file using scipy, to a given volume below 0 dbFS
# write the normalized wave file to a new file with the same name as the original 
# file but with _norm.wav appended to the end
def normalize_wavefile(wave_file_name, target_volume=-3):
    fs, data = read_wave(wave_file_name)
    normalized_data = data / np.max(np.abs(data)) * 10 ** (target_volume / 20)
    #saturate the data to the range [-1, 1]
    normalized_data = np.clip(normalized_data, -1, 1)
    # create the new normalized wave file name
    new_file_name = wave_file_name.split('.')[0] + '_norm.wav'
    export_wave(normalized_data, new_file_name, fs)
    return new_file_name

#function to open a subprocess to convert an mp3 file to a wav file using ffmpeg
def convert_mp3_to_wav(mp3_file_name, output_file_name=None):
    # create the new wav file name
    new_file_name = output_file_name if output_file_name else mp3_file_name.split('.')[0] + '.wav'
    # open the subprocess
    process = subprocess.Popen(['ffmpeg/bin/ffmpeg.exe', '-i', mp3_file_name, new_file_name, '-hide_banner', '-loglevel', 'panic', '-y'])
    # wait for the subprocess to finish
    process.wait()
    # return the new wav file name
    return new_file_name

def convert_wav_to_mp3(wav_file_name, output_file_name=None):
    # create the new mp3 file name 
    new_file_name = output_file_name if output_file_name else wav_file_name.split('.')[0] + '.mp3'
    # open the subprocess
    process = subprocess.Popen(['ffmpeg/bin/ffmpeg.exe', '-i', wav_file_name, new_file_name, '-hide_banner', '-loglevel', 'panic', '-y'])
    # wait for the subprocess to finish
    process.wait()
    # return the new mp3 file name
    return new_file_name

def get_monday_string():
    # get the date of the next monday from the current date
    today = datetime.date.today()
    monday = today + datetime.timedelta(days=(7 - today.weekday()))
    # return the monday as a string in yymmdd format
    return monday.strftime('%y%m%d')


if __name__ == '__main__':
    # read the mp3 file from argparse 
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file_name', '-i', help='the name of the mp3 file to be converted')
    parser.add_argument('--output_file_name', '-o', help='the name of the wav file to be created', required=False, default=None)
    args = parser.parse_args()
    input_file_name = args.input_file_name
    # prepend the next_monday to the output file name if any was given otherwise use the input file name use f string
    output_file_name = args.output_file_name if args.output_file_name else f'{get_monday_string()}_{input_file_name}'
    #convert_mp3_to_wav
    wave_file = convert_mp3_to_wav(input_file_name, 'temp.wav')
    #normalize_wavefile
    normalized_wave_file = normalize_wavefile(wave_file)
    #convert_wav_to_mp3
    convert_wav_to_mp3(normalized_wave_file, output_file_name)
    # remove the temporary wav files
    subprocess.Popen(['rm', wave_file])
    subprocess.Popen(['rm', normalized_wave_file])
    # print the output file name
    print(f'The output file is {output_file_name}')

