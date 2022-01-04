import subprocess

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