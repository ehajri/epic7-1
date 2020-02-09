from opencvtest.funcs import *
from matplotlib import pyplot as plt
from pytesseract import image_to_string
from PIL import Image

img = cv2.imread("screenshots/ss14.png")

# 1385, 412
# w: 412
# h: 199
# 1797, 611
gear_type = img[400:510, 1385:1797]

def draw(img):
    plt.subplot(1,1,1), plt.imshow(img), plt.show()
def draw2(img, img2):
    plt.subplot(1,2,1), plt.imshow(img)
    plt.subplot(1, 2, 2), plt.imshow(img2)
    plt.show()
def apply_threshold(img, argument):
    switcher = {
        1: cv2.threshold(cv2.GaussianBlur(img, (9, 9), 0), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1],
        2: cv2.threshold(cv2.GaussianBlur(img, (7, 7), 0), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1],
        3: cv2.threshold(cv2.GaussianBlur(img, (5, 5), 0), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1],
        4: cv2.threshold(cv2.medianBlur(img, 5), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1],
        5: cv2.threshold(cv2.medianBlur(img, 3), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1],
        6: cv2.adaptiveThreshold(cv2.GaussianBlur(img, (5, 5), 0), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2),
        7: cv2.adaptiveThreshold(cv2.medianBlur(img, 3), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2),
    }
    return switcher.get(argument, "Invalid method")

def read(img):
    return image_to_string(Image.fromarray(img), lang='eng', config='--psm 6')

brown_lo=np.array([54,54,54])
brown_hi=np.array([255,255,255])

# Mask image to only select browns
hsv = cv2.cvtColor(gear_type, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv,brown_lo,brown_hi)
gear_type[mask!=0]=(0,0,0)

#[[60, 60, 60], [206, 206, 206], [115, 115, 115]]
#image[np.where((image >= [x,x,x]).all(axis=2))] = [0,0,0]

draw(gear_type)
print(read(gear_type))