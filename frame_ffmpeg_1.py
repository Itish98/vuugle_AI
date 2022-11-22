from moviepy.editor import VideoFileClip
import numpy as np
import pandas as pd
import os
from datetime import timedelta
import csv

def format_timedelta(td):
    """Utility function to format timedelta objects in a cool way (e.g 00:00:20.05) 
    omitting microseconds and retaining milliseconds"""
    result = str(td)
    try:
        result, ms = result.split(".")
    except ValueError:
        return result + ".00".replace(":", ":")
    ms = int(ms)
    ms = round(ms / 1e4)
    return f"{result}.{ms:02}".replace(":", ":")
    print(f"{result}.{ms:02}".replace(":", ":"))
def main(video_file):
    # load the video clip
    video_clip = VideoFileClip(video_file)
    SAVING_FRAMES_PER_SECOND = video_clip.fps
    print(SAVING_FRAMES_PER_SECOND)
    # make a folder by the name of the video file
    # if the SAVING_FRAMES_PER_SECOND is above video FPS, then set it to FPS (as maximum)
    saving_frames_per_second = min(video_clip.fps, SAVING_FRAMES_PER_SECOND)
    # if SAVING_FRAMES_PER_SECOND is set to 0, step is 1/fps, else 1/SAVING_FRAMES_PER_SECOND
    step = 1 / video_clip.fps if saving_frames_per_second == 0 else 1 / saving_frames_per_second
    # iterate over each possible frame
    a1 = []
    a2 = []
    classes = []
    meta = input('path to metadata :')
    df1 = pd.read_csv(meta)
    name = video_file.split(' ')[0]+'_'
    for i,r in df1.iterrows():
        t = r['time']
        it = r['item']
        directory = 'train'+'/'+name+'_'+t+'_'+it
        classes.append(name+'_'+t+'_'+it)
        isExist = os.path.exists(directory)
        if isExist is False:
            os.makedirs(directory)
        os.system('ffmpeg -i '+'"'+video_file+'"'+' -ss '+t+' -vframes '+str(SAVING_FRAMES_PER_SECOND)+' '+directory+'/output_%d.jpg')
    with open('labels.txt', 'w+') as f:
    	for items in classes:
    		f.write('%s\n' %items)


if __name__ == "__main__":
    import sys
    video_file = input('input video file name :') #sys.argv[1]
    a = main(video_file)
