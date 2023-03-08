import video
import psycopg2
import cv2
import json
import threading
def main():
    print("started the sensors system!")
    ports = [99990,9991,9992,9993,9994,9995,9996,9997]
    for port in ports:
        t = threading.Thread(target=video.read_multicast, args=(port,))
        t.start()

if __name__ == '__main__':
    main()