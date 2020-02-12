import cv2
from pytesseract import image_to_string
from PIL import Image
from matplotlib import pyplot as plt
import numpy as np
TOP_IMG = 'e7/top.jpg'
BOTTOM_IMG = 'e7/bottom.jpg'

TOPBOX_HEIGHT = 160
TOPBOX_WIDTH = 450
BOTTOMBOX_HEIGHT = 335
BOTTOMBOX_WIDTH = 450
BOTTOMBOX_SHIFT = 25
LVL_COORD = [[19, 44], [37, 66]]
PLUS_COORD = [[11, 34], [139, 168]]
TYPE_COORD = [[20, 70], [172, 432]]
MAIN_COORD = [[8, 70], [65, 435]]
SUBS_COORD = [[98, 255], [25, 435]]
SET_COORD = [[280, 340], [76, 435]]
COORDS = {
    "1600": {
        "MARKS": {
            "TOP": "e7/mark.png",
            "BOTTOM": "e7/bottom2.png"
        },
        "TOP": {
            "LVL": [[35, 82], [78, 136]],
            "PLUS": [[13, 65], [220, 280]],
            "TYPE": [[35, 155], [287, 650]]
        },
        "BOTTOM": {
            "MAIN": [[25, 110], [125, 665]],
            "SUBS": [[150, 400], [45, 665]],
            "SET": [[440, 505], [120, 435]]
        },
        "TOP_BOX": {
            "HEIGHT": 246,
            "WIDTH": 706
        },
        "BOTTOM_BOX": {
            "HEIGHT": 535,
            "WIDTH": 670,
            "SHIFT": 25
        }
    }
}
export = {"processVersion": "1", "heroes": [], "items": []}

# for debugging
def draw(img, xy=None):
    if xy != None:
        img = img.copy()
        cv2.rectangle(img, (xy[1][0], xy[0][0]), (xy[1][1], xy[0][1]), (255, 0, 0), 2)
    plt.subplot(1,1,1), plt.imshow(img), plt.show()

# refactor this function
def process(k, imgg, img):
    if not(k in ['LVL', 'PLUS', 'TYPE']):
        thresh = cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU
        low = 0
        proc = cv2.medianBlur(
            cv2.threshold(cv2.resize(imgg, (0, 0), fx=5, fy=5), low, 255, thresh)[1],
            3)
        return image_to_string(Image.fromarray(proc), lang='eng', config='--psm 6')
    if k == 'TYPE':
        # proc = cv2.medianBlur(
        #     cv2.threshold(cv2.resize(img, (0, 0), fx=5, fy=5),0, 155, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1],
        #     3)
        img[np.where((img <= [40, 40, 40]).all(axis=2))] = [255, 255, 255]
        x = image_to_string(Image.fromarray(img), lang='eng', config='--psm 6')
        return x.replace('delmet', 'Helmet')

    thresh = cv2.THRESH_BINARY
    low = 50
    while low <= 125:
        # proc = cv2.cvtColor(cv2.medianBlur(
        #     cv2.threshold(cv2.resize(imgg, (0, 0), fx=5, fy=5), low, 255, thresh)[1],
        #     3), cv2.COLOR_GRAY2RGB)
        proc = cv2.cvtColor(cv2.medianBlur(
            cv2.threshold(~cv2.cvtColor(cv2.resize(img, (0, 0), fx=5, fy=5), cv2.COLOR_BGR2GRAY), low, 200, thresh)[1],
            3), cv2.COLOR_GRAY2RGB)
        # plt.subplot(1,1,1), plt.imshow(proc), plt.show()
        data = image_to_string(Image.fromarray(proc), lang='eng', config='--psm 7')
        if not any(i.isdigit() for i in data):
            if low == 50:
                low = 100
            elif low == 100:
                low = 125
            else:
                break
        else:
            break
    return data

    # proc = cv2.cvtColor(cv2.medianBlur(
    #     cv2.threshold(cv2.resize(imgg, (0, 0), fx=5, fy=5), low, 255, thresh)[1],
    #     3), cv2.COLOR_GRAY2RGB)
    # plt.subplot(1, 1, 1), plt.imshow(proc), plt.show()
    # data = image_to_string(Image.fromarray(proc), lang='eng', config='--psm 7')
    # if not any(i.isdigit() for i in data):
    #     low = 100
    #     proc = cv2.cvtColor(cv2.medianBlur(
    #         cv2.threshold(cv2.resize(imgg, (0, 0), fx=5, fy=5), low, 255, thresh)[
    #             1], 3), cv2.COLOR_GRAY2RGB)
    #     plt.subplot(1,1,1), plt.imshow(proc), plt.show()
    #     data = image_to_string(Image.fromarray(proc), lang='eng', config='--psm 7')
    #     if not any(i.isdigit() for i in data):
    #         low = 125
    #         proc = cv2.cvtColor(cv2.medianBlur(
    #             cv2.threshold(cv2.resize(imgg, (0, 0), fx=5, fy=5), low, 255,
    #                           thresh)[1], 3), cv2.COLOR_GRAY2RGB)
    #         plt.subplot(1, 1, 1), plt.imshow(proc), plt.show()
    #         data = image_to_string(Image.fromarray(proc), lang='eng', config='--psm 7')


def stat_converter(stat):
    result = ''
    if 'attack' in stat.lower():
        result = 'Atk'
        if '%' in stat:
            result += 'P'
    if 'health' in stat.lower():
        result = 'HP'
        if '%' in stat:
            result += 'P'
    if 'defense' in stat.lower():
        result = 'Def'
        if '%' in stat:
            result += 'P'
    if 'speed' in stat.lower():
        result = 'Spd'
    if 'chance' in stat.lower():
        result = 'CChance'
    if 'damage' in stat.lower():
        result = 'CDmg'
    if 'effectiveness' in stat.lower():
        result = 'Eff'
    if 'resistance' in stat.lower():
        result = 'Res'
    return result


def digit_filter(val):
    try:
        return int(''.join(filter(str.isdigit, val)))
    except:
        return 0


def char_filter(val):
    return ''.join(filter(str.isalpha, val)).capitalize()


def fetch_data(k, top_coords, item, top_box, bottom_box):
    for k in top_coords.keys():
        data = process(k, top_box[top_coords[k][0][0]:top_coords[k][0][1], top_coords[k][1][0]:top_coords[k][1][1]])
        if k == 'type':
            item["rarity"] = char_filter(data.split(' ')[0])
            item["slot"] = char_filter(data.split(' ')[1].split('\n')[0])
        if k == 'level':
            item["level"] = digit_filter(data.replace('S', '5').replace('B', '8').replace('a', '8'))
        if k == 'plus':
            item["ability"] = digit_filter(data.replace('S', '5').replace('B', '8').replace('a', '8'))

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
