import subprocess
import argparse
import datetime


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

