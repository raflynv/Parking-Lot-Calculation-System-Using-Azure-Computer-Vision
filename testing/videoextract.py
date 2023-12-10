# import Library
import os
import cv2
import matplotlib.pyplot as plt
import os.path
import datetime
import moviepy
from moviepy.editor import *
import shutil


# Membuat Directory untuk menyimpan gambar
videodir = 'video'

def createdir(dirname):
    # Function to create directory if needed
    import os.path
    from os import path
    if path.os.path.isdir(dirname) :
        print("Directory:", dirname, "exists!")
    else:
        print("Creating directory:", dirname)
        os.mkdir(dirname)
        print("Done!")

outputfiledir = 'ekstrakvideo'
createdir(outputfiledir)

videofile = videodir + '/' + 'parking_sample.mp4'

# Menyimpan 
myvideo = VideoFileClip(videofile)

fps = myvideo.fps
w = myvideo.w
h = myvideo.h
duration = myvideo.duration
nbframes = int(fps * duration)

# Mengekstrak Video Menjadi Gambar
capture = cv2.VideoCapture(videofile)

i = j = 1

while(capture.isOpened()):
    ret, frame = capture.read()
    
    if ret == False:
        break

    if i%fps == 0: # So One frame each second
        if i <100:
            newi = '00' + str(i)
        if i>= 100 and i<1000:
            newi = '0' + str(i)
        
        outputfile = outputfiledir + '/parkingframe_' + str(newi) + '.jpg'
        print(j, "Saving frame", i, "to", outputfile)
        
        cv2.imwrite(outputfile,frame)
        j += 1
    i+=1

print("\nDone:", j-1, "frames were extracted.")
capture.release()