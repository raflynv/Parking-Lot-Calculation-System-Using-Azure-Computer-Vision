import azuremlconfig
import createdirectory
import moviepy
from moviepy.editor import *
import datetime

# Membuat Direktori
DIR1 = 'results'
DIR2 = 'results/captures'
OUTPUTDIR = 'output'
createdirectory.createdir(DIR1)
createdirectory.createdir(DIR2)
createdirectory.createdir(OUTPUTDIR)
createdirectory.nbfiles(DIR1)
createdirectory.nbfiles(DIR2)
createdirectory.nbfiles(OUTPUTDIR)

# Konfigurasi dan Informasi Video
VIDEOFILE = 'video/parking_sample.mp4'
startvideo = 1 
endvideo = 28  
from moviepy.editor import VideoFileClip
import moviepy.editor as mp
MYVIDEOFILE = mp.VideoFileClip(VIDEOFILE)
MYCLIP = MYVIDEOFILE.subclip(startvideo,endvideo)
clipduration = MYCLIP.duration # Compute the duration in secs
print("\nClip duration =", clipduration, 'seconds\n')
MYCLIPNAME = OUTPUTDIR + "/sample.mp4"
MYCLIP.write_videofile(MYCLIPNAME)
sampling_frames = 1 
minpctprob = 40
MYVIDEOFILE = VideoFileClip(MYCLIPNAME)
w = MYVIDEOFILE.w
h = MYVIDEOFILE.h
fps = MYVIDEOFILE.fps
duration = MYVIDEOFILE.duration
nbframes = int(fps * duration)
duration_sec = duration
nbprocessedframes = nbframes / sampling_frames
nbframespersec = sampling_frames / fps

print("\nVideo Clip:", MYCLIPNAME)
print("- Video input size: width =", w, "height =", h)
print("- FPS =", round(fps))
print("- Duration in seconds =", duration_sec)
print("- Number of frames =", nbframes)
print("Setting: Min confidence in % =", minpctprob)
print("Output:")
print("- Sampling Frames =", sampling_frames)
print("- Number of frames to analyse =", int(nbprocessedframes))
print("- Video will be processed each", round(nbframespersec, 2), "seconds")

# Menjalankan Program
import customvisionmodel
import cv2
WEBCAM = OUTPUTDIR + "/sample.mp4" 
if os.path.exists(WEBCAM) == True :
    print("File", WEBCAM, "exists")
    for item in os.scandir(OUTPUTDIR):
         print(createdirectory.datetimeformat(item.stat().st_atime), item.stat().st_size, item.name)

if os.path.exists(WEBCAM) == False :
    print("File", WEBCAM, "did not exist!")
minconfidence = 0.90

# Menjalankan Azure ML
run = azuremlconfig.experiment.start_logging(snapshot_directory = None)
cam = cv2.VideoCapture(WEBCAM)
framenumber = 1
print('Processing the video: ', WEBCAM, 'for every', sampling_frames, "frame(s)", '\n')

if cam.isOpened():
    while True:
        ret, frame = cam.read()
        
        if ret:
            
            t1 = datetime.datetime.now() 
            
            if framenumber%sampling_frames == 0:
                if len(str(framenumber)) == 1:
                    framenumberstr = '00000000' + str(framenumber)
                if len(str(framenumber)) == 2:
                    framenumberstr = '0000000' + str(framenumber)
                if len(str(framenumber)) == 3:
                    framenumberstr = '000000' + str(framenumber)
                if len(str(framenumber)) == 4:
                    framenumberstr = '00000' + str(framenumber)
                if len(str(framenumber)) == 5:
                    framenumberstr = '0000' + str(framenumber)
                if len(str(framenumber)) == 6:
                    framenumberstr = '000' + str(framenumber)
                if len(str(framenumber)) == 7:
                    framenumberstr = '00' + str(framenumber)
                if len(str(framenumber)) == 8:
                    framenumberstr = '0' + str(framenumber)
        
                print("\nProcessing frame:", framenumberstr, '/', nbframes)
                print("Remaining frames:", nbframes - framenumber, ' | Percent:', 
                      round((nbframes - framenumber) / nbframes, 2) * 100, '\n')
            
                capturedframe = 'results/captures/frame_' + framenumberstr + '.jpg'    
                cv2.imwrite(capturedframe, frame)
                
                metrics = customvisionmodel.callingcvmodel(capturedframe, minconfidence)
                run.log('Date', metrics[0])
                
                run.log('Number_of_parked_vehicles', metrics[1])
                run.log('Spaces_available', metrics[2])
                run.log('Entering_or_leaving', metrics[3])
                outputframe = 'results/processed_frame_' + str(framenumberstr) + '.jpg'
                cv2.imwrite(outputframe, customvisionmodel.image, [int(cv2.IMWRITE_JPEG_QUALITY), 100] )

        if framenumber == nbprocessedframes:
            run.complete() 
            print('\n', "-" * 20, "End of job", "-" * 20)
            print(datetime.datetime.now(), 'Done in', datetime.datetime.now() - t1, '\n')
            exit 
        
        framenumber += 1    
        
exit
cam.release()

