# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 16:26:32 2019

@author: sdorle
"""
# =============================================================================
# Concatenating all segments
# =============================================================================
from moviepy.editor import VideoFileClip, clips_array, concatenate_videoclips
# creating array for storing all the segments
all_video_clips = []
import glob, os
#os.chdir("/Output") # To change directory
for file in glob.glob("*.mpg"):
    print(file)
    print(type(file))
    all_video_clips.append(VideoFileClip(file))

# Full movie after combining all segments    
concatenated_clip = concatenate_videoclips(all_video_clips)
#final_clip.write_videofile("my_concatenation_demo.mp4")

# Importing mp4 file of graph animation
graph_clip = VideoFileClip(r"Output\\Phobia_mp4.mp4")

# Combining Movie file and Graph file in split screen
final_clip = clips_array([[concatenated_clip, graph_clip]])

# Exporting file in mp4 format
final_clip.write_videofile("Output\\Movie_graph_4.mp4")#, fps = 30)

# For saving specific frame as image 
np_frame = final_clip.get_frame(2) # get the frame at t=2 seconds

final_clip.save_frame('my_image.png', t=400)

'''
# =============================================================================
# Concatenating clips one after other
# =============================================================================
from moviepy.editor import VideoFileClip, concatenate_videoclips
clip1 = VideoFileClip("demo2.mp4") # Importing 1st video file
clip2 = VideoFileClip("518059_11_1.mpg") # importing second video file
final_clip = concatenate_videoclips([clip1,clip2]) # concatenating both vi
final_clip.write_videofile("my_concatenation.mp4") # Exporting results to mp4 file


# =============================================================================
# Screen Split example
# =============================================================================

from moviepy.editor import VideoFileClip, clips_array, vfx

clip1 = VideoFileClip("517695_01.mpg").subclip(50,80)# 
clip2 = VideoFileClip(r"517695_02.mpg").subclip(50,80)

# Concatenating both video files
final_clip = clips_array([[clip1, clip2]])
#final_clip.resize(width=480).write_videofile("my_stack_2.mp4")

# Writing/exporting video file
final_clip.write_videofile("my_stack_5.mp4")
'''

