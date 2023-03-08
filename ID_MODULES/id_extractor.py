# importing modules
import cv2
import pytesseract
from pytesseract import Output
import numpy as np


# def zoom_center(img, zoom_factor=1.01):
#     y_size = img.shape[0]
#     x_size = img.shape[1]

#     # define new boundaries
#     x1 = int(0.5 * x_size * (1 - 1 / zoom_factor))
#     x2 = int(x_size - 0.5 * x_size * (1 - 1 / zoom_factor))
#     y1 = int(0.5 * y_size * (1 - 1 / zoom_factor))
#     y2 = int(y_size - 0.5 * y_size * (1 - 1 / zoom_factor))

#     # first crop image then scale
#     img_cropped = img[y1:y2, x1:x2]
#     return cv2.resize(img_cropped, None, fx=zoom_factor, fy=zoom_factor)


def format_to_read(image):
    scale_percentage = 228
    width = int(image.shape[1] * scale_percentage / 100)
    height = int(image.shape[0] * scale_percentage / 100)
    dimentions = (width, height)

    image = cv2.resize(image, dimentions, interpolation=cv2.INTER_CUBIC)  # INTER_AREA
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    clash = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(4, 4))
    clahe_image = clash.apply(gray_image)

    blur = cv2.GaussianBlur(clahe_image, (3, 3), 0)
    mask = cv2.inRange(blur, 1, 20)
    mask = 255 - mask

    kernel = np.ones((3, 3), np.uint8)
    dilated_image = cv2.dilate(mask, kernel, iterations=1)

    kernel = np.ones((2, 2), np.uint8)
    eroded_image = cv2.erode(dilated_image, kernel, iterations=1)

    kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])

    return cv2.filter2D(src=eroded_image, ddepth=-1, kernel=kernel)


def captured_value(value):
    if len(value) == 0:
        return "captureError"
    return value


def image_to_data(img, single=False, rtl=False):
    custom_config = (
        r"--psm 3"#"  # tessedit_char_whitelist=0123456789אבגדהוזחטיכלמנסעפצקרשת"  # 3
    )
    pytesseract.pytesseract.tesseract_cmd = (
        r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    )
    read = pytesseract.image_to_string(img, config=custom_config, lang="eng+heb")
    if rtl:
        return captured_value(read[::-1])
    return captured_value(read)


id = [{"id_number": "X", "first_name": "X", "last_name": "X", "birthdate": "X"}]


def scan_id(image):

    # image[y:y+h, x:x+h]
    id_num_pic = image[94:118, 145:238]
    id_num_pic = format_to_read(id_num_pic)
    id_data = image_to_data(id_num_pic)

    first_name_pic = image[140:170, 140:260]
    first_name_pic = format_to_read(first_name_pic)
    first_name_data = image_to_data(first_name_pic, rtl=True)

    last_name_pic = image[210:240, 140:260]
    last_name_pic = format_to_read(last_name_pic)
    last_name_data = image_to_data(last_name_pic, rtl=True)

    birthdate_pic = image[252:272, 220:310]
    birthdate_pic = format_to_read(birthdate_pic)
    birthdate_data = image_to_data(birthdate_pic)

    return {
        "id_number": id_data,
        "first_name": first_name_data,
        "last_name": last_name_data,
        "birthdate": birthdate_data,
    }

# scan_id("some_ids/60004.jpg")