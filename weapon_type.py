import cv2
from pytesseract import image_to_string
from matplotlib import pyplot as plt
import numpy as np
from PIL import Image
def draw(img):
    plt.subplot(1,1,1), plt.imshow(img), plt.show()
def read(img):
    return image_to_string(Image.fromarray(img), lang='eng', config='--psm 6')
img = cv2.imread('type1.png')
img[np.where((img <= [40, 40, 40]).all(axis = 2))] = [255,255,255]


# cv2.imshow("Original", img)  # show windows
#
# #cv2.imshow("output", ret)  # show windows
#
# cv2.imshow("mask", mask)  # show windows
#
print(read(img))
draw(img)
