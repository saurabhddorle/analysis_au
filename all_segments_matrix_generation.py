# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 14:00:49 2019

@author: sdorle
"""

# =============================================================================
# For generating the background score matrix of all the segments of movie
# =============================================================================

####################################
# Standard imports
from __future__ import print_function
import warnings
warnings.filterwarnings("ignore")
import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display
import math
import os    
import pandas as pd         
import glob

# 1 #
# =============================================================================
# Background Score Matrix Generation Function
# =============================================================================

def background_music_matrix(audio, dur_min):
    
    #audio = y
    # computing the spectrogram magnitude and phase
    S_full, phase = librosa.magphase(librosa.stft(audio))
    
    #==========================================================================
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


# 2 #
# =============================================================================
# Generating matrix for the movie
# =============================================================================
# List all files from directory with .mpg extension
all_files = glob.glob('./*.mpg')
# print total number of segments in the movie
print("\n Total Segments ", len(all_files))

background_score = [] # To store the background score values of all the segments
segments_dur = [] # To store the duration of segments
total_dur_sec = 0
total_dur_min = 0

# Take all the segment files from the directory, to genrate the background score
for i in all_files:
    print("\n Processing segment:" ,i)
    y, sr = librosa.load(str(i), sr = 1200)
    # Getting duratoin of file and convertoing to minutes
    duration_sec = librosa.get_duration(y=y, sr=sr)
    
    total_dur_sec = total_dur_sec + duration_sec
    
    #duration_min = math.floor(duration_sec/60)
    duration_min = round(duration_sec/60)
    segments_dur.append(duration_min)
    
    total_dur_min = total_dur_min + duration_min
    # Calling background matrix function
    print("\n Generating Matrix....")
    arr = background_music_matrix(y, duration_min)
    background_score.append(arr)
    background_score.append([0])
    print("\n Matrix generated successfully")

# Getting background_scores of all segments in one list    
flat_list = [item for sublist in background_score for item in sublist]

# Final_baclground_score (removing the segment cuts)
background_score = [score for score in flat_list if score != 0]

########################### Graph Plotting ##############################

# Getting minutes for segment ends
indexes = [i for i,x in enumerate(flat_list) if x == 0]
del indexes[-1]

# Creating list to store the segment cuts minute number
segment_cuts = []
cnt = 0
for j in indexes:
    segment_cuts.append(j-cnt)
    cnt += 1
 
# Storing background values with segments cuts    
np.savetxt("Output\\Background_score.csv", flat_list, delimiter=",", fmt='%s', header='Background_Score')
# Storing segment duration values
np.savetxt("Output\\Segments_duration.csv", segments_dur, delimiter=",", fmt='%s', header='Segments_duration')
# Storing minute number where new segment is started
np.savetxt("Output\\Segments_cuts.csv", segment_cuts, delimiter=",", fmt='%s', header='Segments_cuts')
# Storing background values without segments cuts
np.savetxt("Output\\Segments_score_without_cuts.csv", background_score, delimiter=",", fmt='%s', header='Background_score')
