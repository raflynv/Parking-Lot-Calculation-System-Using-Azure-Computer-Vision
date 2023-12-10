import createdirectory
import datetime
import os

#Membuat Direktori dan konfigurasi
results_path = 'results' 
video_output = 'hasil_video.mp4' 
output_path = 'web' 
createdirectory.createdir(output_path) 
import moviepy.video.io.ImageSequenceClip
image_folder = 'results' 
fps = 24
fps_output = fps 
video_outputfilename = output_path + '/' + video_output 

# Pembuatan Hasil Video
t1 = datetime.datetime.now()
print(t1, "Building video file:", video_outputfilename, '\n')
image_files = [os.path.join(image_folder, img)
for img in os.listdir(image_folder) if img.endswith(".jpg")]

clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files, fps = fps_output)
print(datetime.datetime.now(), "Writing video file...")
clip.write_videofile(video_outputfilename)

print('\nDone in', datetime.datetime.now() - t1)