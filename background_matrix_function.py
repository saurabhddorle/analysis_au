# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 10:13:52 2019

@author: sdorle
"""

##################
# Standard imports
from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display
import math


# Importing Audio file
y, sr = librosa.load('Dataset\\Hum Aapke Hain Koun Full Movie 1994  Madhuri '
                     + 'Dixit And Salman Khan 720p.mp3', sr = 1200, duration=540)

y, sr = librosa.load('518149_01.mpg', sr = 1200)#, duration = 540)
duration_sec = librosa.get_duration(y=y, sr=sr)

duration_min = math.floor(duration_sec/60)

arr2 = background_music_matrix(y, duration_min)


def background_music_matrix(audio, dur_min):
    
    #audio = y
    # computung the spectrogram magnitude and phase
    S_full, phase = librosa.magphase(librosa.stft(audio))
    
    #==============================================================================
    # Selcting the duration and converting to frames, plotting the graph
    movie_dur_sec = dur_min * 60
    idx = slice(*librosa.time_to_frames([0, movie_dur_sec], sr=sr))
    plt.figure(figsize=(12, 4))
    librosa.display.specshow(librosa.amplitude_to_db(S_full[:, idx], ref=np.max),
                             y_axis='log', x_axis='time', sr=sr)
    plt.colorbar()
    plt.tight_layout()
    
    #==============================================================================
    
    # Comparing frames using cosine similarity, and aggregate similar frames
    # by taking their (per-frequency) median value  
    S_filter = librosa.decompose.nn_filter(S_full,
                                           aggregate=np.median,
                                           metric='cosine',
                                           width=int(librosa.time_to_frames(2, sr=sr)))
    
    # The output of the filter shouldn't be greater than the input
    # if we assume signals are additive.  Taking the pointwise minimium
    # with the input spectrum forces this.
    S_filter = np.minimum(S_full, S_filter)
    
    #==============================================================================
    
    # We can also use a margin to reduce bleed between the vocals and instrumentation masks.
    # Note: the margins need not be equal for foreground and background separation
    margin_i, margin_v = 2, 10
    power = 2
    
    mask_i = librosa.util.softmask(S_filter,
                                   margin_i * (S_full - S_filter),
                                   power=power)
    
    mask_v = librosa.util.softmask(S_full - S_filter,
                                   margin_v * S_filter,
                                   power=power)
    
    # Once we have the masks, simply multiply them with the input spectrum
    # to separate the components
    
    S_foreground = mask_v * S_full
    S_background = mask_i * S_full
    
    # =============================================================================
    # Reducing dimensions as per size of audio in minutes
    # =============================================================================
    # Reducing the dimension of the background matrix
    reduced_dimention = np.add.reduce(S_background)
    
    # Converting matrix into minutes size array
    min_dur = dur_min
    size = len(reduced_dimention) # len of the current dimension
    in_mins = int(size / min_dur) 
    times = int(size / in_mins)
    
    x = [i * in_mins for i in range(0, times+1)]
    
    arr = []
    for j in range(0, times):
        values = np.mean(reduced_dimention[x[j]:x[j+1]])
        arr.append(values)
    
    
    return arr
    
    
    
    ######### Scaling both reach and background matrix  ###########################
    #import pandas as pd
    #df = pd.read_csv('Dataset\\reach.csv')
    #df['values'] = arr    
    
    #df2 = pd.DataFrame()
    #df2['Reach'] = df.Reach.iloc[:min_dur]
    #df2['values'] = arr
        
    #from sklearn.preprocessing import StandardScaler
    #scaler = StandardScaler()
    #tmp = scaler.fit_transform(df2)
    
    #tmp2 = pd.DataFrame(tmp)
    # Correlation matrix
    #corr_matrix = tmp2.corr()
