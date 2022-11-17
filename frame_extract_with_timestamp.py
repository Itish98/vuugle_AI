from moviepy.editor import VideoFileClip
import numpy as np
import pandas as pd
import os
from datetime import timedelta


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
    filename, _ = os.path.splitext(video_file)
    filename += "-moviepy"
    if not os.path.isdir(filename):
        os.mkdir(filename)

    # if the SAVING_FRAMES_PER_SECOND is above video FPS, then set it to FPS (as maximum)
    saving_frames_per_second = min(video_clip.fps, SAVING_FRAMES_PER_SECOND)
    # if SAVING_FRAMES_PER_SECOND is set to 0, step is 1/fps, else 1/SAVING_FRAMES_PER_SECOND
    step = 1 / video_clip.fps if saving_frames_per_second == 0 else 1 / saving_frames_per_second
    # iterate over each possible frame
    a1 = []
    a2 = []
    df1 = pd.read_csv('sample.csv')
    for current_duration in np.arange(0, video_clip.duration, step):
        # format the file name and save it
        frame_duration_formatted = format_timedelta(timedelta(seconds=current_duration)).replace(":", ":")
        name = video_file.split(' ')[0]+'_'
        v = frame_duration_formatted.split('.')[0]
#if v not in df1.values:
#continue
#else:
        isExist = os.path.exists('train'+'/'+name+v)
        if isExist is False:
        	os.makedirs('train'+'/'+name+v)
        frame_filename = os.path.join('train',name+v, f"{name}{frame_duration_formatted}.jpg")
        a1.append(f"{name}{frame_duration_formatted}.jpg")
        a2.append(frame_duration_formatted)
        # save the frame with the current duration
        video_clip.save_frame(frame_filename, current_duration)
    path = 'data.csv'
    isExist = os.path.exists(path)
    df = pd.DataFrame({'filename': pd.Series(dtype='str'),'ts': pd.Series(dtype='str')})
    df['filename'] = a1
    df['ts'] = a2
    if isExist == True:
        df.to_csv('data.csv',header=False,mode='a',index=False)
    else:
        df.to_csv('data.csv',index=False)
if __name__ == "__main__":
    import sys
    video_file = sys.argv[1]
    a = main(video_file)
    print(a)
