from msrest.authentication import ApiKeyCredentials
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
import datetime
import cv2

# Mengatur konfigurasi Azure Custom Vision
PREDICTION_KEY = "ee4cd0db4c434a1eaaa9470fc713ed02"
ENDPOINT = "https://customvisionfly-prediction.cognitiveservices.azure.com/"
PROJECT_ID = "39b34e7d-e766-470c-91cb-a2c96a7c4a2e"
ITERATION_NAME = "test"
credentials = ApiKeyCredentials(in_headers={"Prediction-key": PREDICTION_KEY })
predictor = CustomVisionPredictionClient(ENDPOINT, credentials)

# Ukuran Video
w, h = 1100, 720

# Kordinat Untuk Lahan Parkir dan Konfigurasi Warna
zone1_x1 = 60
zone1_x2 = 1000
zone1_y1 = 180
zone1_y2 = 580

color_lime = (0, 255, 0)
color_cyan = (255, 255, 0)
color_red = (0, 0, 255)
color_orange = (0, 140, 255)

# Model
def callingcvmodel(imagefilename, minconf):
    
    print("Analysing:", imagefilename, '\n')
        
    global image 
    image = cv2.imread(imagefilename)
  
    with open(imagefilename, mode="rb") as captured_image:
        results = predictor.detect_image(PROJECT_ID, ITERATION_NAME, captured_image)

    i = 1 
    nb_vehicles_zone1 = nb_vehicles_NA = 0
    location_vehicle = ''

    now = str(datetime.datetime.today().strftime ('%d-%b-%Y %H:%M:%S'))
    msg_now = '[CCTV 1] ' + str(now)
    cv2.putText(image, msg_now, (30, 40), cv2.FONT_HERSHEY_PLAIN, 2, color_lime, 2, cv2.LINE_AA)

    cv2.rectangle(image, (zone1_x1, zone1_y1), (zone1_x2, zone1_y2), color_orange, 4)

    for prediction in results.predictions:
        if prediction.tag_name == 'Vehicle' and prediction.probability >= minconf:

            bbox = prediction.bounding_box
            print(i, '\t', str.upper(prediction.tag_name), 
                  '\t', round(prediction.probability, 5))
        
            x_center = int((bbox.width * w) / 2 + (bbox.left  * w))
            y_center = int((bbox.height * h) / 2 + (bbox.top * h))
            
            cv2.rectangle(image, (int(bbox.left * w), int(bbox.top * h)),
                          (int((bbox.left + bbox.width) * w), int((bbox.top + bbox.height) * h)), color_lime, 2)            
            
            if (x_center >= zone1_x1 and x_center <= zone1_x2) and (y_center >= zone1_y1 and y_center <= zone1_y2):
                location_vehicle = "zone1"
                nb_vehicles_zone1 += 1
                cv2.rectangle(image, (int(bbox.left * w), int(bbox.top * h)), 
                              (int((bbox.left + bbox.width) * w), int((bbox.top + bbox.height) * h)), color_red, 3)
            
            if (x_center < zone1_x1) or (x_center > zone1_x2) or (y_center < zone1_y1) or (y_center > zone1_y2):
                location_vehicle = 'Masuk/Keluar'
                cv2.putText(image, location_vehicle, (x_center + 25, y_center), 
                            cv2.FONT_HERSHEY_PLAIN, 2, color_lime, 2, cv2.LINE_AA)
                nb_vehicles_NA += 1
                cv2.circle(image, (x_center, y_center), radius=5, color=color_lime, thickness=4)
                cv2.circle(image, (x_center, y_center), radius=10, color=color_red, thickness=4)
            
            i+=1

        nb_vehicles = i - 1

    msg_nb_vehicules = 'Jumlah Kendaraan = ' + str(nb_vehicles)
    cv2.putText(image, msg_nb_vehicules, (30, 80), cv2.FONT_HERSHEY_PLAIN, 2, color_lime, 2, cv2.LINE_AA)
    print()
    print('Kendaraan yang terbaca dalam gambar = ', nb_vehicles)

    totalplaces_zone1 = 23
    totalvehicles_in_zones = nb_vehicles_zone1 
    totalplaces = totalplaces_zone1 
    freeplaces = totalplaces - totalvehicles_in_zones

    msgfree = 'Lahan Parkir yang Tersedia = ' + str(freeplaces)
    cv2.putText(image, msgfree, (450, 80), cv2.FONT_HERSHEY_PLAIN, 2, color_lime, 2, cv2.LINE_AA)
    
    free_zone1 = totalplaces_zone1 - nb_vehicles_zone1
    nb_parked_vehicles = nb_vehicles - nb_vehicles_NA

    print("Lahan Parkir yang Tersedia =", freeplaces)
    print("Jumlah Kendaraan yang Parkir", nb_parked_vehicles)
    print("Jumlah Lahan Parkir yang Tersedia =", free_zone1)
    print("Jumlah Kendaraan yang Tidak Parkir =", nb_vehicles_NA)
    print()

    return now, nb_parked_vehicles, freeplaces, nb_vehicles_NA