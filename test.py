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

TOP_BOX_HEIGHT=245
TOP_BOX_WIDTH=670
TOP_BOX_HEIGHT_SHIFT=24
TOP_BOX_WIDTH_SHIFT=16

pic = imageio.imread(TOP_IMG)
gray = lambda rgb : np.dot(rgb[... , :3] , [0.299 , 0.587, 0.114])
gray2 = gray(pic)

files = [
    #"screenshots/ss2.png", "screenshots/ss3.png", "screenshots/ss4.png", "screenshots/ss1.jpg", "screenshots/ss5.png", "screenshots/ss6.png", "screenshots/ss7.png",
    "screenshots/ss8.png"]
marks = ["e7/top.jpg", "e7/mark.png"]

for f in files:
    for m in marks:
        mark = cv2.imread(m, 0)
        imgg = cv2.imread(f)
        res = cv2.matchTemplate(cv2.cvtColor(imgg, cv2.COLOR_BGR2GRAY), mark, cv2.TM_CCOEFF_NORMED)
        minv, maxv, min_loc, max_loc = cv2.minMaxLoc(res)
        if maxv < 0.9:
            print("Not found", m)
        else:
            coords = COORDS["1600"]
            # debugging
            lvl = coords["LVL"]
            plus = coords["PLUS"]
            _type = coords["TYPE"]
            TB_H = coords["TOP_BOX"]["HEIGHT"]
            TB_W = coords["TOP_BOX"]["WIDTH"]
            y1 = max_loc[1]
            y2 = max_loc[1] + TB_H
            x1 = max_loc[0] - TB_W
            x2 = max_loc[0]

            top_box = imgg[y1:y2, x1:x2]
            # print("top box", "(%d, %d) (%d, %d)" % (x1, y1, x2, y2))
            # print("lvl box", "(%d, %d) (%d, %d)" % (x1 + lvl[1][0], y1 + lvl[0][0], x1 + lvl[1][1], y1 + lvl[0][1]))

            # imgg2 = cv2.cvtColor(imgg, cv2.COLOR_BGR2BGRA)
            # cv2.rectangle(imgg2, (x1, y1), (x2, y2), (255, 0, 0), 2)
            # cv2.rectangle(imgg2, (x1 + lvl[1][0], y1 + lvl[0][0]), (x1 + lvl[1][1], y1 + lvl[0][1]), (255, 0, 0), 2)
            #
            # plt.subplot(111), plt.imshow(imgg2, cmap = 'gray')
            # plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
            # plt.suptitle("yo")
            #
            # plt.show()
            # a = Image.fromarray(np.divide(np.array(x), 2**8-1))
            #
            # gray3 = np.array([[np.uint8(round(b)) for b in a] for a in gray2])
            #
            # _, _, _, max_loc = cv2.minMaxLoc(
            #     cv2.matchTemplate(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), x, cv2.TM_CCOEFF_NORMED))

            # top_box = img[max_loc[1]:max_loc[1] + TOPBOX_HEIGHT, max_loc[0] - TOPBOX_WIDTH:max_loc[0]]
            # print("level dimensions", lvl[0][0], lvl[0][1], lvl[1][0], lvl[1][1])
            # lvlimg = top_box[lvl[0][0]:lvl[0][1], lvl[1][0]:lvl[1][1]]

            # cv2.rectangle(top_box, (lvl[1][0], lvl[0][0]), (lvl[1][1], lvl[0][1]), (255, 0, 0), 2)
            # cv2.rectangle(top_box, (plus[1][0], plus[0][0]), (plus[1][1], plus[0][1]), (255, 0, 0), 2)
            # cv2.rectangle(top_box, (_type[1][0], _type[0][0]), (_type[1][1], _type[0][1]), (255, 0, 0), 2)
            # plt.subplot(111), plt.imshow(top_box)
            # plt.show()
            top_coords = {'type': TYPE_COORD,
                          'level': LVL_COORD,
                          'plus': PLUS_COORD}
            data = process('level',
                           top_box[lvl[0][0]:lvl[0][1], lvl[1][0]:lvl[1][1]])
            result = digit_filter(data.replace('S', '5').replace('B', '8').replace('a', '8'))
            print("item level:", result)

            data = process('plus',
                           top_box[plus[0][0]:plus[0][1], plus[1][0]:plus[1][1]])
            result = digit_filter(data.replace('S', '5').replace('B', '8').replace('a', '8').replace('19', '15'))
            print("enhance:", result)

            data = process('type',
                           top_box[_type[0][0]:_type[0][1], _type[1][0]:_type[1][1]])
            type1 = char_filter(data.split(' ')[0])
            type2 = char_filter(data.split(' ')[1].split('\n')[0])
            print("type:", type1, type2)

            BOTTOM_X = max_loc[0] - coords["TOP_BOX"]["WIDTH"]

            temp_bot = cv2.imread("e7/bottom2.png", 0)
            _, _, _, max_loc = cv2.minMaxLoc(
                cv2.matchTemplate(cv2.cvtColor(imgg, cv2.COLOR_BGR2GRAY), temp_bot, cv2.TM_CCOEFF_NORMED))
            # Fixed width, shift down BOTTOMBOX_SHIFT from divider, then crop 335 pixels deep
            BB = coords["BOTTOM_BOX"]
            bottom_box = imgg[max_loc[1] + BB['SHIFT']:max_loc[1] + BB['HEIGHT'] + BB['SHIFT'],
                         BOTTOM_X:BOTTOM_X + BB['WIDTH']]

            btminfo = coords["BOTTOM"]
            main = btminfo["MAIN"]
            subs = btminfo["SUBS"]
            _set = btminfo["SET"]

            cv2.rectangle(bottom_box, (main[1][0], main[0][0]), (main[1][1], main[0][1]), (255, 0, 0), 2)
            cv2.rectangle(bottom_box, (subs[1][0], subs[0][0]), (subs[1][1], subs[0][1]), (255, 0, 0), 2)
            cv2.rectangle(bottom_box, (_set[1][0], _set[0][0]), (_set[1][1], _set[0][1]), (255, 0, 0), 2)
            plt.subplot(111), plt.imshow(bottom_box)
            plt.show()

            data = process("", bottom_box[main[0][0]:main[0][1], main[1][0]:main[1][1]])
            print("data", data)
            stat = stat_converter(data)
            val = digit_filter(data)
            print("main:", stat, val)
            data = process("", bottom_box[subs[0][0]:subs[0][1], subs[1][0]:subs[1][1]])
            for n, entry in enumerate(data.split('\n')):
                stat = stat_converter(entry)
                val = digit_filter(entry.replace('T%', '7%'))
                print("sub:", stat, val)
            data = process("", bottom_box[_set[0][0]:_set[0][1], _set[1][0]:_set[1][1]])
            iset = char_filter(data.split(' Set')[0])
            print("set:", iset)



            # Setup item dictionary
# id_num = "jt" + "".join(random.choice(digits + ascii_lowercase) for _ in range(6))
# item = {"locked": False, "efficiency": 0, "id": id_num}
# # Process top image
# top_coords = {'type': TYPE_COORD,
#               'level': LVL_COORD,
#               'plus': PLUS_COORD}

