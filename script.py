from PIL import Image
from pytesseract import image_to_string
from string import ascii_lowercase, digits
import pytesseract
import imageio
import cv2
import imageio
import numpy as np
import random
from functions import *
from matplotlib import pyplot as plt
#from verification import gear

resolution = "1600"
files = [
    #"screenshots/ss2.png", "screenshots/ss3.png", "screenshots/ss4.png", "screenshots/ss1.jpg", "screenshots/ss5.png", "screenshots/ss6.png", "screenshots/ss7.png",
    "screenshots/ss10.png"]
marks = ["e7/top.jpg", "e7/mark.png"]
coords = COORDS[resolution]

# for debugging
def draw(img, xy=None):
    if xy != None:
        img = img.copy()
        cv2.rectangle(img, (xy[1][0], xy[0][0]), (xy[1][1], xy[0][1]), (255, 0, 0), 2)
    plt.subplot(1,1,1), plt.imshow(img), plt.show()



def analyze(img, debug=False):
    # img is an array
    mark = cv2.imread(coords['MARKS']['TOP'], 0)
    res = cv2.matchTemplate(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), mark, cv2.TM_CCOEFF_NORMED)
    minv, maxv, min_loc, max_loc = cv2.minMaxLoc(res)
    if maxv < 0.9:
        print("Not found")
        return
    TB_H = coords["TOP_BOX"]["HEIGHT"]
    TB_W = coords["TOP_BOX"]["WIDTH"]
    y1 = max_loc[1]
    y2 = max_loc[1] + TB_H
    x1 = max_loc[0] - TB_W
    x2 = max_loc[0]

    top_box = img[y1:y2, x1:x2]
    top_box_g = cv2.cvtColor(top_box, cv2.COLOR_BGR2GRAY)
    top_coords = coords["TOP"]


    export = {}
    # for k in top_coords:
    #     crds = top_coords[k]
    #     data = process(k, top_box_g[crds[0][0]:crds[0][1], crds[1][0]:crds[1][1]], top_box[crds[0][0]:crds[0][1], crds[1][0]:crds[1][1]])
    #     if k == 'LVL':
    #         export["ilvl"] = digit_filter(data.replace('S', '5').replace('B', '8').replace('a', '8'))
    #
    #     if k == 'PLUS':
    #         export["enhance"] = digit_filter(
    #             data.replace('S', '5').replace('B', '8').replace('a', '8').replace('19', '15'))
    #
    #     if k == 'TYPE':
    #         export["grade"] = char_filter(data.split(' ')[0])
    #         export["slot"] = char_filter(data.split(' ')[1].split('\n')[0])

    BOTTOM_X = x2 - coords["TOP_BOX"]["WIDTH"]

    temp_bot = cv2.imread(coords['MARKS']['BOTTOM'], 0)
    _, _, _, max_loc = cv2.minMaxLoc(
        cv2.matchTemplate(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), temp_bot, cv2.TM_CCOEFF_NORMED))

    BB = coords["BOTTOM_BOX"]
    bottom_box = img[max_loc[1] + BB['SHIFT']:max_loc[1] + BB['HEIGHT'] + BB['SHIFT'], BOTTOM_X:BOTTOM_X + BB['WIDTH']]
    bottom_box_g = cv2.cvtColor(bottom_box, cv2.COLOR_BGR2GRAY)



    bottom_coords = coords["BOTTOM"]

    for k in bottom_coords:
        crds = bottom_coords[k]
        sss = bottom_box[crds[0][0]:crds[0][1], crds[1][0]:crds[1][1]]
        if k == "SET":
            draw(sss)
            exit()
        else:
            continue
        data = process(k, bottom_box_g[crds[0][0]:crds[0][1], crds[1][0]:crds[1][1]], bottom_box[crds[0][0]:crds[0][1], crds[1][0]:crds[1][1]])
        if k == 'MAIN':
            export["main"] = {'stat': stat_converter(data), 'value': digit_filter(data)}
        if k == 'SUBS':
            export["subs"] = []
            for n, entry in enumerate(data.split('\n')):
                export['subs'].append({'stat': stat_converter(entry), 'value': digit_filter(entry.replace('T%', '7%'))})
        if k == 'SET':
            export['set'] = char_filter(data.split(' Set')[0])
    return export

from jsondiff import diff
for file in range(1, 35):
    # xx = 5
    # if file != xx: continue
    # if file == xx:
    #     e = analyze(cv2.imread("screenshots/"+str(file)+".png"), True)
    e = analyze(cv2.imread("screenshots/" + str(file) + ".png"))
    print(e)
    # v = gear[file]
    # r = e == v
    # if r:
    #     print(file, e==v)
    # else:
    #     print(file, "diff:", e)

# for f in files:
#     for m in marks:
#         mark = cv2.imread(m, 0)
#         imgg = cv2.imread(f)
#         res = cv2.matchTemplate(cv2.cvtColor(imgg, cv2.COLOR_BGR2GRAY), mark, cv2.TM_CCOEFF_NORMED)
#         minv, maxv, min_loc, max_loc = cv2.minMaxLoc(res)
#         if maxv < 0.9:
#             print("Not found", m)
#         else:
#             # debugging
#             analyze(cv2.imread(f))

