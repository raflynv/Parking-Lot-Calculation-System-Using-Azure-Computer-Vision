# import Library
import sys
import matplotlib.pyplot as plt
import cv2
import time
import datetime
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials

# Buka gambar untuk melihat gambar yang akan dianalisis
myimage = "gambar/test.jpg"

image = cv2.imread(myimage)
h, w, c = image.shape 

plt.figure(figsize=(18, 8))
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
plt.imshow(image_rgb)
# plt.show()

# Mengatur konfigurasi Azure Custom Vision
PREDICTION_KEY = "ee4cd0db4c434a1eaaa9470fc713ed02"
ENDPOINT = "https://customvisionfly-prediction.cognitiveservices.azure.com/"
PROJECT_ID = "39b34e7d-e766-470c-91cb-a2c96a7c4a2e"
ITERATION_NAME = "test"
credentials = ApiKeyCredentials(in_headers={"Prediction-key": PREDICTION_KEY })
predictor = CustomVisionPredictionClient(ENDPOINT, credentials)

# Kordinat Untuk Lahan Parkir dan Konfigurasi Warna
zone1_x1 = 60
zone1_x2 = 1000
zone1_y1 = 200
zone1_y2 = 600

color_lime = (0, 255, 0)
color_cyan = (255, 255, 0)
color_red = (0, 0, 255)
color_orange = (0, 140, 255)


# Cheking Model
with open(myimage, mode="rb") as captured_image:
    results = predictor.detect_image(PROJECT_ID, ITERATION_NAME, captured_image)
    resultoutputfile = "gambar/hasil.jpg" # output file

# Init
i=1
nb_vehicles_zone1 = nb_vehicles_NA = 0
location_vehicle = ''

now = str(datetime.datetime.today().strftime ('%d-%b-%Y %H:%M:%S'))
msg_now = '[CCTV] ' + str(now)
cv2.putText(image, msg_now, (30, 40), cv2.FONT_HERSHEY_PLAIN, 2, color_lime, 2, cv2.LINE_AA)

# Zone displays
result_image = cv2.rectangle(image, (zone1_x1, zone1_y1), (zone1_x2, zone1_y2), color_orange, 4)

for prediction in results.predictions:
    
    if prediction.probability >= 0.6:
        # Printing
        print(i, '\tObjek yang Terbaca =', str.upper(prediction.tag_name), 'with confidence =', 
              round(prediction.probability, 5))
        
        # Vehicles only
        if prediction.tag_name == 'Vehicle':  
            bbox = prediction.bounding_box
            
            # Average coordinates of each vehicles
            x_center = int((bbox.width * w) / 2 + (bbox.left  * w))
            y_center = int((bbox.height * h) / 2 + (bbox.top * h))
            
            # Drawing ROI for each vehicles
            result_image = cv2.rectangle(image, 
                                         (int(bbox.left * w), int(bbox.top * h)), 
                                         (int((bbox.left + bbox.width) * w), int((bbox.top + bbox.height) * h)), 
                                         color_lime, 3)
            
            # Testing if vehicles belong to a zone
            if (x_center >= zone1_x1 and x_center <= zone1_x2) and (y_center >= zone1_y1 and y_center <= zone1_y2):
                    location_vehicle = "zone1"
                    nb_vehicles_zone1 += 1
                    result_image = cv2.rectangle(image, 
                                         (int(bbox.left * w), int(bbox.top * h)), 
                                         (int((bbox.left + bbox.width) * w), int((bbox.top + bbox.height) * h)), 
                                         color_red, 3)
        
            
            if (x_center < zone1_x1) or (x_center > zone1_x2) or (y_center < zone1_y1) or (y_center > zone1_y2):
                location_vehicle = 'Entering/Leaving'
                cv2.putText(result_image, location_vehicle, (x_center + 25, y_center), cv2.FONT_HERSHEY_PLAIN, 
                            2, color_lime, 2, cv2.LINE_AA)
                nb_vehicles_NA += 1
                result_image = cv2.circle(image, (x_center, y_center), radius=5, color=color_lime, thickness=4)
                result_image = cv2.circle(image, (x_center, y_center), radius=10, color=color_red, thickness=4)
            
            i+=1

nb_vehicles = i - 1

# Display message on the image
msg_nb_vehicules = 'Jumlah Kendaraan = ' + str(nb_vehicles)
cv2.putText(result_image, msg_nb_vehicules, (30, 80), cv2.FONT_HERSHEY_PLAIN, 2, color_lime, 2, cv2.LINE_AA)

print("\nTerdapat", nb_vehicles, 'Kendaraan yang terbaca dalam gambar')

totalplaces_zone1 = 23
totalvehicles_in_zones = nb_vehicles_zone1
totalplaces = totalplaces_zone1 
freeplaces = totalplaces - totalvehicles_in_zones
pct_freeplaces = round((totalplaces - nb_vehicles) / totalplaces * 100)

msgfree = 'Lahan Parkir yang Tersedia = ' + str(freeplaces)
cv2.putText(result_image, msgfree, (450, 80), cv2.FONT_HERSHEY_PLAIN, 2, color_lime, 2, cv2.LINE_AA)

cv2.imwrite(resultoutputfile, result_image, [int(cv2.IMWRITE_JPEG_QUALITY), 100] )

free_zone1 = totalplaces_zone1 - nb_vehicles_zone1
nb_parked_vehicles = nb_vehicles - nb_vehicles_NA

print("\033[1;31;34m\nLahan Parkir Tersedia =", freeplaces, '(', pct_freeplaces, '% )')
print("\nJumlah Kendaraan yang Parkir =", nb_parked_vehicles)
print("Jumlah Lahan Parkir yang Tersedia =", free_zone1)
print("\nJumlah Kendaraan yang Tidak Parkir = ", nb_vehicles_NA)

from IPython.display import Image
sample_image = 'gambar/hasil.jpg'
Image(filename=sample_image) 

