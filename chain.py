from audio_effects.trim import Trim
from mp3tools import convert_mp3_to_wav, convert_wav_to_mp3
from audio_effects.normalize import Normalize
from audio_effects.clip import HardClip, SoftClip
from audio_effects.amplify import Amplify
from wavetools import BufferedWaveReader, BufferedWaveWriter
from audio_effects.audioformat import Float64, Int16
import time
import os
import json


# function to apply the effects to a wave file
def apply_effects(input_wavefile, output_wavefile):
    with open("config.json", "r") as f:
        config = json.load(f)
    # get the normalize key from the config
    normalize_config = config["normalize"]
    # get the clip type from the config
    if "soft" in str(config["clip_type"]).lower():
        clip_type = SoftClip
    else:
        clip_type = HardClip
    # get the amplify config from the config
    amplify_config = config["amplify"]

    reader = BufferedWaveReader(input_wavefile)
    operators = (
        Float64(),
        Trim(),
        Amplify(**amplify_config),
        clip_type(),
        Normalize(**normalize_config),
        Int16(),
    )
    writer = BufferedWaveWriter(output_wavefile, reader.sample_rate())
    data = reader.data
    for operator in operators:
        # store the time before the operator
        start_time = time.time()
        data = operator.apply_effect(data)
        # store the time after the operator
        end_time = time.time()
        print(f"{operator.info_str()} took {end_time - start_time:.2f} seconds")
    writer.append(data)
    writer.write()


# a function called main to run the program
def main(input_file: str, output_file: str = "test_output.mp3"):
    # convert the mp3 file to a wav file
    convert_mp3_to_wav(input_file, "test.wav")
    # apply the effects to the wav file
    apply_effects("test.wav", "test_out.wav")
    # convert the wav file back to an mp3 file
    convert_wav_to_mp3("test_out.wav", output_file)
    # delete the wav file
    os.remove("test.wav")
    os.remove("test_out.wav")


def get_monday_string():
    import datetime

    # get the date of the next monday from the current date
    today = datetime.date.today()
    monday = today + datetime.timedelta(days=(7 - today.weekday()))
    # return the monday as a string in yymmdd format
    return monday.strftime("%y%m%d")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Apply effects to an audio file")
    parser.add_argument(
        "-i", "--input_file", help="the input file", type=str, required=True
    )
    parser.add_argument(
        "-o", "--output_file", help="the output file", type=str, default=""
    )
    args = parser.parse_args()
    if args.output_file == "":
        args.output_file = f"{get_monday_string()}_{args.input_file}"
    main(args.input_file, args.output_file)
