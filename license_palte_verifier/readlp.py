import cv2
from pytesseract import pytesseract
import re
import glob

def isValidLicensePlate(img):
    pytesseract.tesseract_cmd = r'/bin/tesseract' #FIXME: change to tesseract path on the linux machine
    cropped = img[0:80, 12:150]
    denoised = cv2.fastNlMeansDenoising( cropped, None, 60, 5, 23)  
    denoised = cv2.cvtColor(denoised, cv2.COLOR_BGR2GRAY)
    denoised = cv2.inRange(denoised, 0, 50)
    cv2.imwrite("cleaned.png", denoised)
    cv2.imshow("image", img)
    cv2.imshow("denoised", denoised)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    imgString = pytesseract.image_to_string(denoised)
    print(imgString.replace(" ", "-"))

    if re.match("^[A-Za-z0-9 ]*$", imgString) and len(imgString) == 10:
        return imgString
    else:
        return ""
    


# for path in glob.glob('C:/Users/u9092788/Downloads/someimages/*.png'):
#     img = cv2.imread(path)
#     if(isValidLicensePlate(img)):
#         print("valid license plate")
#     else:
#         print("invalid license plate")