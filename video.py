import cv2
import os
        
cap = cv2.VideoCapture('udp://172.16.31.73:9999?overrun_nonfatal=1&fifo_size=50000000',cv2.CAP_FFMPEG)

if not cap.isOpened():
    print('VideoCapture not opened')
    exit(-1)

counter = 0
path = "C:/Users/u9092788/Downloads/smaller_photos/new_photos"

while True:
    ret, frame = cap.read()

    if not ret:
        print('frame empty')
        print(counter)
        break
    else:    
        frame = cv2.resize(frame, (400, 400))
        cv2.imshow('image', frame)
        imgDir = str(str(path) + '/' + str(counter) + '.jpg')

        if not(os.path.exists(imgDir)):
            cv2.imwrite(imgDir, frame)

        counter += 1

        if cv2.waitKey(1)&0XFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()