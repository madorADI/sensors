import cv2
import os
from classifier.ClassificationImg import *
from ID_MODULES.id_extractor import *
from ID_MODULES.id_auth import *
from license_palte_verifier.readlp import *
from connection import *
from utils.removeDuplicatets import *
import polygons.borderCheckPolygon as borderCheckPolygon
from shapely.geometry.polygon import Polygon
from shapely.geometry import Point
import connection
def read_multicast(port):
    cap = cv2.VideoCapture('udp://localhost:'+str(port)+'?overrun_nonfatal=1&fifo_size=50000000',cv2.CAP_FFMPEG)

    if not cap.isOpened():
        print('VideoCapture not opened')
        exit(-1)
    # counter = 0
    # path = "C:/Users/u9092788/Downloads/smaller_photos/new_photos"
    curr_point = Point(33, 32)
    while True:
        ret, frame = cap.read()

        if not ret:
            print('frame empty')
            # print(counter)
            break
        else:
            img = frame
            imgGrayScale = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            clas = getClassificationImg(imgGrayScale)
            data ={}
            curr_point = borderCheckPolygon.generateAllInfoAndApplyToPolygon(Polygon([[29,29],[29,38],[38,38],[38,29]]),0,10,curr_point)
            data["keepAlive"] = True
            if clas == "ID":
                data["is_id"]= True
                scan = scan_id(img)["id_number"]
                if not is_valid_id(scan):
                    data["keepAlive"] = False
                data["number"]=scan
            if clas == "License Plate":
                data["is_id"]= False
                scan = isValidLicensePlate(img)
                if scan == "":
                    data["keepAlive"] = False
                data["number"]=scan
            data["location_x"] = curr_point.x
            data["location_y"] = curr_point.y
            timestamp  = time.time()
            data["timestamp"] = timestamp
            data["keepAlive"] = not data["keepAlive"]
            data["sensor_type"] = port%9990
            data["sensor_id"] = port%9990
            connection.run_socket(data)
            # frame = cv2.resize(frame, (400, 400))
            # cv2.imshow('image', frame)
            # imgDir = str(str(path) + '/' + str(counter) + '.jpg')

            # if not(os.path.exists(imgDir)):
                # cv2.imwrite(imgDir, frame)

            # counter += 1

            # if cv2.waitKey(1)&0XFF == ord('q'):
                # break

    # cap.release()
    # cv2.destroyAllWindows()