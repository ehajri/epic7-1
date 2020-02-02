from PIL import Image
from pytesseract import image_to_string
from string import ascii_lowercase, digits
import pytesseract
import imageio
import cv2
import numpy as np
import random
from functions_org import *

filenames = ["screenshots/ss1.jpg"]
# filenames = ["screenshots/Screenshot_20190327-090940.jpg"]
for name in filenames:
    # Because the height of the item boxes changes depending on the length of the item and set descriptions, we have to
    # crop the top and bottom info separately in order to ensure the OCR boxes within these areas stay fixed.

    img = cv2.imread(name)
    # print(name)

    # Top Box
    temp_top = cv2.imread(TOP_IMG, 0)
    _, _, _, max_loc = cv2.minMaxLoc(
        cv2.matchTemplate(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), temp_top, cv2.TM_CCOEFF_NORMED))
    # Fixed width, then crop TOPBOX_HEIGHT pixels from top triangle
    print(max_loc)
    print(max_loc[1], max_loc[1] + TOPBOX_HEIGHT, max_loc[0] - TOPBOX_WIDTH, max_loc[0])
    print(LVL_COORD)
    top_box = img[max_loc[1]:max_loc[1] + TOPBOX_HEIGHT, max_loc[0] - TOPBOX_WIDTH:max_loc[0]]
    # cv2.imwrite('e7/top_box_.jpg', top_box)
    BOTTOM_X = max_loc[0] - TOPBOX_WIDTH

    # Bottom Box
    temp_bot = cv2.imread(BOTTOM_IMG, 0)
    _, _, _, max_loc = cv2.minMaxLoc(
        cv2.matchTemplate(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), temp_bot, cv2.TM_CCOEFF_NORMED))
    # Fixed width, shift down BOTTOMBOX_SHIFT from divider, then crop 335 pixels deep
    bottom_box = img[max_loc[1] + BOTTOMBOX_SHIFT:max_loc[1] + BOTTOMBOX_HEIGHT + BOTTOMBOX_SHIFT, BOTTOM_X:BOTTOM_X + BOTTOMBOX_WIDTH]
    # cv2.imwrite('e7/bottom_box.jpg', bottom_box)

    # Setup item dictionary
    id_num = "jt" + "".join(random.choice(digits + ascii_lowercase) for _ in range(6))
    item = {"locked": False, "efficiency": 0, "id": id_num}

    # Process top image
    top_coords = {'type': TYPE_COORD,
                  'level': LVL_COORD,
                  'plus': PLUS_COORD}
    for k in top_coords.keys():

        data = process(k, top_box[top_coords[k][0][0]:top_coords[k][0][1], top_coords[k][1][0]:top_coords[k][1][1]])
        # print(data)
        if k == 'type':
            item["rarity"] = char_filter(data.split(' ')[0])
            item["slot"] = char_filter(data.split(' ')[1].split('\n')[0])
        if k == 'level':
            item["level"] = digit_filter(data.replace('S', '5').replace('B', '8').replace('a', '8'))
        if k == 'plus':
            item["ability"] = digit_filter(data.replace('S', '5').replace('B', '8').replace('a', '8'))

    # Process bottom image
    bot_coords = {'main': MAIN_COORD,
                  'subs': SUBS_COORD,
                  'set': SET_COORD}
    for k in bot_coords.keys():
        data = process(k, bottom_box[bot_coords[k][0][0]:bot_coords[k][0][1], bot_coords[k][1][0]:bot_coords[k][1][1]])
        if k == 'main':
            # print(data)
            stat = stat_converter(data)
            val = digit_filter(data)
            item["mainStat"] = [stat, val]
        if k == 'subs':
            # print(data.split('\n'))
            for n, entry in enumerate(data.split('\n')):
                stat = stat_converter(entry)
                val = digit_filter(entry.replace('T%', '7%'))
                item['subStat' + str(n + 1)] = [stat, val]
        if k == 'set':
            # print(data)
            item["set"] = char_filter(data.split(' Set')[0])
    export["items"].append(item)
    # print(item)
    # print(item)
    # print(export)