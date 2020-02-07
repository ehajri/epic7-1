from opencvtest.funcs import *
from matplotlib import pyplot as plt
from pytesseract import image_to_string
from PIL import Image

img = cv2.imread("screenshots/ss12.png")

# 1385, 412
# w: 412
# h: 199
# 1797, 611
gear_type = img[412:611, 1385:1797]

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

g = gear_type.copy()
image = g
white = [[60, 60, 60], [206, 206, 206], [115, 115, 115]]
x = 30
#image[np.where((image >= [x,x,x]).all(axis=2))] = [0,0,0]
data = image_to_string(Image.fromarray(image), lang='eng', config='--psm 6')
#draw(image)
a = data.split("\n")
print(a[0])
print(len(a))
print(repr(data))
# draw(g)
# draw(cv2.subtract(100, g))
g = get_grayscale(g)
# kernel = np.ones((1, 1), np.uint8)
# img = cv2.dilate(g, kernel, iterations=1)
# img = cv2.erode(img, kernel, iterations=1)
#
# for i in range(1, 8):
#     print(i)
#     img = apply_threshold(img.copy(), i)
#     draw(img)