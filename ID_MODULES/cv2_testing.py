# importing modules
import cv2
import pytesseract
from pytesseract import Output
import numpy as np


def zoom_center(img, zoom_factor=1.5):
    y_size = img.shape[0]
    x_size = img.shape[1]

    # define new boundaries
    x1 = int(0.5 * x_size * (1 - 1 / zoom_factor))
    x2 = int(x_size - 0.5 * x_size * (1 - 1 / zoom_factor))
    y1 = int(0.5 * y_size * (1 - 1 / zoom_factor))
    y2 = int(y_size - 0.5 * y_size * (1 - 1 / zoom_factor))

    # first crop image then scale
    img_cropped = img[y1:y2, x1:x2]
    return cv2.resize(img_cropped, None, fx=zoom_factor, fy=zoom_factor)


picture_path = "./images/id.jpg"

# reading image using opencv
image = cv2.imread(picture_path)
image = zoom_center(image)

# kernal = np.ones((4, 4), np.uint8)
# image = cv2.dilate(image, kernal, iterations= 1)

#image = cv2.resize(image, None, fx = 2, fy = 1, interpolation = cv2.INTER_CUBIC)
image = cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 15)

# kernal = np.ones((2, 2), np.uint8)
# image = cv2.erode(image, kernal, iterations= 1)

# converting image into gray scale images
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#gray_image = cv2.blur(gray_image,(3,3))


se = cv2.getStructuringElement(cv2.MORPH_RECT, (8, 8))
bg = cv2.morphologyEx(gray_image, cv2.MORPH_DILATE, se)
out_gray = cv2.divide(gray_image, bg, scale=255)
out_binary = cv2.threshold(out_gray, 0, 255, cv2.THRESH_OTSU)[1]

kernal = np.ones((3, 3), np.uint8)
out_binary = cv2.dilate(out_binary, kernal, iterations= 2)

# kernal = np.ones((3, 3), np.uint8)
# out_binary = cv2.erode(out_binary, kernal, iterations= 1)

kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])

out_binary = cv2.filter2D(src=out_binary, ddepth=-1, kernel=kernel)

# out_binary = cv2.dilate(out_binary, np.ones((2, 2)), iterations=1)
cv2.imshow("5", out_binary)

# configuring parameters for tesseract
custom_config = r"--psm 3"  # 3
pytesseract.pytesseract.tesseract_cmd = r"/bin/tesseract"

# now feeding image to tesseract
details = pytesseract.image_to_data(
    out_binary, output_type=Output.DICT, config=custom_config, lang="heb"
)

total_boxes = len(details["text"])

for sequence_number in range(total_boxes):
    if int(details["conf"][sequence_number]) > 30:
        (x, y, w, h) = (
            details["left"][sequence_number],
            details["top"][sequence_number],
            details["width"][sequence_number],
            details["height"][sequence_number],
        )
        out_binary = cv2.rectangle(out_binary, (x, y), (x + w, y + h), (0, 255, 0), 2)

# display image

cv2.imshow("captured text", out_binary)

# Maintain output window until user presses a key

cv2.waitKey(0)

# Destroying present windows on screen

cv2.destroyAllWindows()

parse_text = []

word_list = []

last_word = ""

for word in details["text"]:
    if word != "":
        word_list.append(word)
        last_word = word

    if (last_word != "" and word == "") or (word == details["text"][-1]):
        parse_text.append(word_list)
        word_list = []

print(parse_text)
