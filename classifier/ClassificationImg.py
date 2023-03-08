import pickle
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


def prepare_img_for_model(img_classification):
    image_size = 128
    img = cv2.resize(img_classification, (image_size, image_size)).flatten()
    np_img = np.asarray(img)

    plt.figure(figsize=(10, 10))
    plt.subplot(1, 2, 1)
    plt.imshow(np_img.reshape(image_size, image_size))
    plt.axis('off')

    img_classification_data = []
    img1 = cv2.resize(img_classification, (image_size, image_size))
    img_classification_data.append(img1)

    img_classification_data_res = np.concatenate(
        (np.asarray(img_classification_data)), axis=0)

    x_data = np.concatenate((img_classification_data_res), axis=0)
    x_data = (x_data-np.min(x_data))/(np.max(x_data)-np.min(x_data))

    return x_data

# RES: 0 - ID, 1 - License Plates


def getClassificationImg(img_classification):
    pickled_model = pickle.load(open('my_model.pickle', 'rb'))

    return "ID" if pickled_model.predict([prepare_img_for_model(img_classification)]) == [0.] else "License Plates"


imgOrigin = cv2.imread(
    "C:\\Users\\u9276439\\Desktop\\SensorsTeam\\inj\\40196.jpg")

# convert to GRAY SCALE
imgGrayScale = cv2.cvtColor(imgOrigin, cv2.COLOR_RGB2GRAY)

ans = getClassificationImg(imgGrayScale)
print(ans)

# if Id{} if LIC {}
