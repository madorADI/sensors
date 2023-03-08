import pickle
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression
import numpy as np
import cv2
import os
from tqdm import tqdm
import matplotlib.pyplot as plt
from PIL import Image
from sklearn.model_selection import train_test_split
from keras.models import load_model
import tensorflow

train_license_plates = 'licensePlates'
train_ids = 'ids'
test_license_plates = "testLicensePlates"
test_ids = "testIds"
image_size = 128

for image in tqdm(os.listdir(train_license_plates)):
    path = os.path.join(train_license_plates, image)
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (image_size, image_size)).flatten()
    np_img = np.asarray(img)

for image2 in tqdm(os.listdir(train_ids)):
    path = os.path.join(train_ids, image2)
    img2 = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.resize(img2, (image_size, image_size)).flatten()
    np_img2 = np.asarray(img2)

plt.figure(figsize=(10, 10))
plt.subplot(1, 2, 1)
plt.imshow(np_img.reshape(image_size, image_size))
plt.axis('off')
plt.subplot(1, 2, 2)
plt.imshow(np_img2.reshape(image_size, image_size))
plt.axis('off')
plt.title("Ids and License Plates in GrayScale")


def train_data():

    train_data_license_plates = []
    train_data_ids = []

    for image1 in tqdm(os.listdir(train_license_plates)):
        path = os.path.join(train_license_plates, image)
        img1 = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        img1 = cv2.resize(img1, (image_size, image_size))
        train_data_license_plates.append(img1)

    for image2 in tqdm(os.listdir(train_ids)):
        img_jpg = Image.open('ids\\' + image2)
        img_jpg.save('idsPNG\\' + image2.replace("jpg", "png"))
        path = os.path.join('idsPNG\\' + image2.replace("jpg", "png"))
        img2 = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        img2 = cv2.resize(img2, (image_size, image_size))
        train_data_ids.append(img2)

    train_data = np.concatenate(
        (np.asarray(train_data_license_plates), np.asarray(train_data_ids)), axis=0)

    return train_data


def test_data():

    test_data_license_plates = []
    test_data_ids = []

    for image1 in tqdm(os.listdir(test_license_plates)):
        path = os.path.join(test_license_plates, image1)
        img1 = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        img1 = cv2.resize(img1, (image_size, image_size))
        test_data_license_plates.append(img1)

    for image2 in tqdm(os.listdir(test_ids)):
        img_jpg = Image.open('testIds\\' + image2)
        img_jpg.save('testIdsPNG\\' + image2.replace("jpg", "png"))
        path = os.path.join('testIdsPNG\\' + image2.replace("jpg", "png"))
        img2 = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        img2 = cv2.resize(img2, (image_size, image_size))
        test_data_ids.append(img2)

    test_data = np.concatenate(
        (np.asarray(test_data_license_plates), np.asarray(test_data_ids)), axis=0)

    return test_data


train_data = train_data()
test_data = test_data()

x_data = np.concatenate((train_data, test_data), axis=0)
x_data = (x_data-np.min(x_data))/(np.max(x_data)-np.min(x_data))

z1 = np.zeros(314)
o1 = np.ones(114)
Y_train = np.concatenate((o1, z1), axis=0)
z = np.zeros(10)
o = np.ones(10)
Y_test = np.concatenate((o, z), axis=0)

y_data = np.concatenate((Y_train, Y_test), axis=0).reshape(x_data.shape[0], 1)

print("X shape: ", x_data.shape)
print("Y shape: ", y_data.shape)

x_train, x_test, y_train, y_test = train_test_split(
    x_data, y_data, test_size=0.15, random_state=42)
number_of_train = x_train.shape[0]
number_of_test = x_test.shape[0]

x_train_flatten = x_train.reshape(
    number_of_train, x_train.shape[1]*x_train.shape[2])
x_test_flatten = x_test .reshape(
    number_of_test, x_test.shape[1]*x_test.shape[2])
print("X train flatten", x_train_flatten.shape)
print("X test flatten", x_test_flatten.shape)

x_train = x_train_flatten.T
x_test = x_test_flatten.T
y_test = y_test.T
y_train = y_train.T
print("x train: ", x_train.shape)
print("x test: ", x_test.shape)
print("y train: ", y_train.shape)
print("y test: ", y_test.shape)


def initialize_weights_and_bias(dimension):
    w = np.full((dimension, 1), 0.01)
    b = 0.0

    return (w, b)


def sigmoid(z):
    y_head = 1/(1+np.exp(-z))

    return y_head


def forward_backward_propagation(w, b, x_train, y_train):
    # forward propagation
    z = np.dot(w.T, x_train) + b
    y_head = sigmoid(z)
    loss = -y_train*np.log(y_head)-(1-y_train)*np.log(1-y_head)
    cost = (np.sum(loss))/x_train.shape[1]
    # backward propagation
    derivative_weight = (
        np.dot(x_train, ((y_head-y_train).T)))/x_train.shape[1]
    derivative_bias = np.sum(y_head-y_train)/x_train.shape[1]
    gradients = {"derivative_weight": derivative_weight,
                 "derivative_bias": derivative_bias}

    return cost, gradients


def update(w, b, x_train, y_train, learning_rate, number_of_iterarion):
    cost_list = []
    cost_list2 = []
    index = []

    for i in range(number_of_iterarion):

        cost, gradients = forward_backward_propagation(w, b, x_train, y_train)
        cost_list.append(cost)

        w = w - learning_rate * gradients["derivative_weight"]
        b = b - learning_rate * gradients["derivative_bias"]
        if i % 100 == 0:
            cost_list2.append(cost)
            index.append(i)
            print("Cost after iteration %i: %f" % (i, cost))

    parameters = {"weight": w, "bias": b}
    plt.plot(index, cost_list2)
    plt.xticks(index, rotation='vertical')
    plt.xlabel("Number of Iterarion")
    plt.ylabel("Cost")

    return parameters, gradients, cost_list


def predict(w, b, x_test):

    z = sigmoid(np.dot(w.T, x_test)+b)
    Y_prediction = np.zeros((1, x_test.shape[1]))

    for i in range(z.shape[1]):
        if z[0, i] <= 0.5:
            Y_prediction[0, i] = 0
        else:
            Y_prediction[0, i] = 1

    return Y_prediction


def logistic_regression(x_train, y_train, x_test, y_test, learning_rate,  num_iterations):

    dimension = x_train.shape[0]
    w, b = initialize_weights_and_bias(dimension)

    parameters, gradients, cost_list = update(
        w, b, x_train, y_train, learning_rate, num_iterations)

    y_prediction_test = predict(
        parameters["weight"], parameters["bias"], x_test)
    y_prediction_train = predict(
        parameters["weight"], parameters["bias"], x_train)

    print("Test Accuracy: {} %".format(
        round(100 - np.mean(np.abs(y_prediction_test - y_test)) * 100, 2)))
    print("Train Accuracy: {} %".format(
        round(100 - np.mean(np.abs(y_prediction_train - y_train)) * 100, 2)))


logistic_regression(x_train, y_train, x_test, y_test,
                    learning_rate=0.01, num_iterations=1500)

grid = {"C": np.logspace(-3, 3, 7), "penalty": ["l1", "l2"]},
logistic_regression = LogisticRegression(random_state=42)
log_reg_cv = GridSearchCV(logistic_regression, grid, cv=10)
log_reg_cv.fit(x_train.T, y_train.T)

print("best hyperparameters: ", log_reg_cv.best_params_)
print("accuracy: ", log_reg_cv.best_score_)

log_reg = LogisticRegression(C=1, penalty="l2")
log_reg.fit(x_train.T, y_train.T)
print("test accuracy: {} ".format(log_reg.fit(
    x_test.T, y_test.T).score(x_test.T, y_test.T)))
print("train accuracy: {} ".format(log_reg.fit(
    x_train.T, y_train.T).score(x_train.T, y_train.T)))

# log_reg.save('logistic_regression_model.h5')

filename = "my_model.pickle"

# save model
pickle.dump(log_reg, open(filename, "wb"))
