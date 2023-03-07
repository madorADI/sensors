import cv2
from pytesseract import pytesseract
import re
import glob

def isValidLicensePlate(img):
    pytesseract.tesseract_cmd = r'C:/Users/u9092788/AppData/Local/Programs/Tesseract-OCR/tesseract.exe'
    img = cv2.imread(img)
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
        return True
    else:
        return False
    
assert isValidLicensePlate("C:/Users/u9092788/Downloads/someimages/75000.png") == True
assert isValidLicensePlate("C:/Users/u9092788/Desktop/75312.png") == False

for img in glob.glob('C:/Users/u9092788/Downloads/someimages/*.png'):
    if(isValidLicensePlate(img)):
        print("valid license plate")
    else:
        print("invalid license plate")