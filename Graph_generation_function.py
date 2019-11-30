# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 16:29:57 2019

@author: sdorle
"""


########################## Importing Libraries ################################
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D

############################ Variable declaration #############################
frame_value = 147 # Total number of minutes in the movie
interval_value = 60000 # 1 minute
movie_dur = 147 # Total number of minutes in the movie
movie_name = 'Haider_graph' # Name of the Movie
movie_segments = [14, 29, 42, 55, 65, 75, 85, 98, 113, 125, 138] # Minutes where new segments are started, 
                                                                 # Take these values from 'segment_cuts.csv' file

############################### Importing dataset #############################
# Import the data having both reach and background_score
data = pd.read_csv("reach_background_score.csv")
data2 = data.head(movie_dur)

######## Setting Values ############
y = data2.Background_score.values
y2 = data2.Reach.values
x = np.arange(1,movie_dur+1,1)

# Set figure size
fig, ax = plt.subplots(1, 1, figsize=(14,6))
fig.set_facecolor("0.25") # Set outside graph background color
ax.set_facecolor("0.90") # Set inside graph color


########################### Animate function ##################################
def update_line(num, data, line):
    line.set_data(data[..., :num])   
    line.set_label("Backhround_score")
    # PLotting segment cuts
    xcoords = movie_segments#[24, 51, 75, 98, 117, 136, 159, 180, 201]
    for xc in xcoords:
        plt.axvline(x=xc, color = '0.50')
    # Plotting Reach
    ax2 = ax.twinx()
    ax2.plot(y2, 'g')
    ax2.set_ylabel("Reach",fontsize=15) 
    return line, 

data = np.vstack((x,y))
l, = plt.plot([], [], 'r-')
plt.xlim(1, movie_dur+1)
plt.ylim(1, 2000)

# Call animation function and execute update line
line_ani = animation.FuncAnimation(fig, update_line, frames = frame_value+2,
                           fargs=(data, l), interval = interval_value, blit=False)


######################## Setting Graph title and axis name ####################
# Assigning labels and Title
plt.style.use('dark_background')
plt.ylabel('Hz', fontsize=15)
plt.xlabel('Time', fontsize=15)
plt.title('Background_Score_Analysis',fontsize=20)
# PLotting legends
colors = ['red', 'green', '0.50']
lines = [Line2D([0], [0], color=c, linewidth=3, linestyle='-') for c in colors]
labels = ['Background_score', 'Reach', 'Segments']
plt.legend(lines, labels, bbox_to_anchor=(1.05, 1.17), loc='upper right')
# Show graph
plt.show()

############################# Saving Files ####################################

# Saving Animation file in GIF format
line_ani.save(movie_name + '_gif.gif', writer='imagemagick')
# Saving Animation file in mp4 format
line_ani.save(movie_name + '_mp4.mp4')





