import numpy as np
from audio_effects.compressor import StereoCompressor
from audio_effects.normalize import Normalize, read_wave
from audio_effects.trim import Trim
from mp3tools import convert_mp3_to_wav, convert_wav_to_mp3
from audio_effects.clip import SoftClip
from wavetools import BufferedWaveReader, BufferedWaveWriter
from audio_effects.audioformat import Float32, Float64, Int32
import time


# dictionary to create compressor objects
compressor_config = {
    'attack_msec': 10,
    'release_msec': 1000,
    'threshold_db': -12.04,
    'ratio': float('inf'),
    'knee_db': 1,
    'makeup_gain_db': 0,
    'sample_rate': 44100,
}

normalize_config = {
    'target_db': -3,
}

# function to apply the effects to a wave file
def apply_effects(input_wavefile, output_wavefile):
    reader = BufferedWaveReader(input_wavefile)
    compressor_config['sample_rate'] = reader.sample_rate()
    operators = (Float64(), 
                Trim(), 
                StereoCompressor(**compressor_config), 
                Normalize(**normalize_config), 
                SoftClip(),
                Int32())
    writer = BufferedWaveWriter(output_wavefile, reader.sample_rate())
    data = reader.data
    for operator in operators:
        # store the time before the operator
        start_time = time.time()
        data = operator.apply_effect(data)
        # store the time after the operator
        end_time = time.time()
        print(f'{operator.info_str()} took {end_time - start_time:.2f} seconds')
    writer.append(data)
    writer.write()

# a function called main to run the program
def main():
    # convert the mp3 file to a wav file
    convert_mp3_to_wav('GT2021-12-20.mp3', 'test.wav')
    # apply the effects to the wav file
    apply_effects('test.wav', 'test_out.wav')
    # convert the wav file back to an mp3 file
    #convert_wav_to_mp3('test_out.wav', 'test_out.mp3')
    # delete the wav file
    #os.remove('test.wav')
    #os.remove('test_out.wav')

# a function to prepare a wave data by downsampling by a given factor
def downsample_wave(data, factor):
    # use the numpy array method reshape to downsample the data
    data = Float64().apply_effect(data)
    # by the given factor
    len = data.shape[0]
    # remove the last elements if the length is not divisible by the factor
    if len % factor != 0:
        data = data[:-(len % factor)]
    # reshape the data to a 2D array
    data = data.reshape((len // factor, factor))
    # take the mean of each row to get the downsampled data
    data = np.mean(data, axis=1)
    # make the data in the range [-1, 1]
    return data


import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go

app = dash.Dash(__name__)
# combobo box to select the input file
input_file_options = [
    {'label': 'Input', 'value': 'test.wav'},
    {'label': 'Output', 'value': 'test_out.wav'},
]
# set the layout of app with a combobox and a plot
app.layout = html.Div([
    html.H1('Wave plotter'),
    dcc.Dropdown(
        id='input-file',
        options=input_file_options,
        value='test.wav',
        style={'width': '50%'}
    ),
    dcc.Graph(id='wave-plot')
])
    
# function to update the plot
@app.callback(
    Output('wave-plot', 'figure'),
    [Input('input-file', 'value')]
)
def update_wave_plot(input_file):
    # read the wave file
    fs, data = read_wave(input_file)
    # downsample the wave file by a factor of 48
    data = downsample_wave(data[:,0], 48)
    # create the figure
    fig = go.Figure()
    # create the time axis
    time = np.arange(0, len(data)) / fs / 48
    # plot the wave file
    fig.add_trace(go.Scatter(x=time, y=data))
    # set the layout
    fig.update_layout(
        title='Wave plot',
        xaxis_title='Time (s)',
        yaxis_title='Amplitude (V)',
        showlegend=False
    )
    # return the figure
    return fig

    


if __name__ == '__main__':
    #main()
    # start the dash app
    app.run_server(debug=True)
    