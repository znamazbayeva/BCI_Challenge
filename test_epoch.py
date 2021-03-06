"""
@author: Yundong Wang

Preprocessing data from Kaggle BCI Challenge.
"""

from generate_epoch import *
import matplotlib.pyplot as plt               # for plotting
from scipy.signal import butter, sosfiltfilt  # for filtering
import numpy as np                            # for dealing with data
import pandas as pd


def butter_bandpass_filter(raw_data, fs, lowcut=1.0, highcut=40.0, order=5):
    '''
    The filter I want to apply to my raw eeg data.
    :raw_data (nparray): data you want to process
    :fs (float): sampling rate
    :lowcut (float, optional): lowest frequency we will pass
    :highcut (float, optional): highest frequency we will pass
    :order (int, optional): order of filter
    '''
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    sos = butter(order, [low, high], analog=False, btype='band', output='sos')
    filted_data = sosfiltfilt(sos, raw_data)
    return filted_data


if __name__ == "__main__":

    channels = ['Fp1', 'Fp2', 'AF7', 'AF3', 'AF4', 'AF8', 'F7', 'F5', 'F3', 'F1',
                'Fz', 'F2', 'F4', 'F6', 'F8', 'FT7', 'FC5', 'FC3', 'FC1', 'FCz',
                'FC2', 'FC4', 'FC6', 'FT8', 'T7', 'C5', 'C3', 'C1', 'Cz', 'C2',
                'C4', 'C6', 'T8', 'TP7', 'CP5', 'CP3', 'CP1', 'CPz', 'CP2', 'CP4',
                'CP6', 'TP8', 'P7', 'P5', 'P3', 'P1', 'Pz', 'P2', 'P4', 'P6', 'P8',
                'PO7', 'POz', 'P08', 'O1', 'O2']

    stimulus_times_csv = pd.read_csv('Time_indices.csv')
    data = generate_epoch('Data_S02_Sess01.csv', channels, 200.0,
                          butter_bandpass_filter, stimulus_times=stimulus_times_csv)
    # should be (60, 56, 300): 60 events, 56 channels, 300 time-stamps
    print('Epoched data shape: ' + str(data.shape))

    # Default parameters for generate_epoch. We need those info for drawing.
    epoch_s = 0
    epoch_e = 700
    fs = 200.0
    dt = int(1000/fs)
    times = range(epoch_s, epoch_e, dt)

    channel = 'Pz'
    channel_idx = channels.index(channel)
    # plt.plot(times, np.mean(data, axis=0)[channel_idx])
    for i in range(int(data.shape[0])):
        plt.plot(times, data[i, channel_idx, :])

    plt.xlabel('Time (ms)')
    plt.ylabel('Amplitude (uV)')
    plt.grid(True)
    plt.title("Subject 2 %s stimulus" % channel)
    plt.savefig('images/Subject_2_%s.png' % channel)
