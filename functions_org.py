import cv2
from pytesseract import image_to_string
from PIL import Image
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

export = {"processVersion": "1", "heroes": [], "items": []}

def process(k, img):
    if k == 'level' or k == 'plus':
        thresh = cv2.THRESH_BINARY
        low = 50
        proc = cv2.cvtColor(cv2.medianBlur(
            cv2.threshold(~cv2.cvtColor(cv2.resize(img, (0, 0), fx=5, fy=5), cv2.COLOR_BGR2GRAY), low, 255, thresh)[1],
            3), cv2.COLOR_GRAY2RGB)
        data = image_to_string(Image.fromarray(proc), lang='eng', config='--psm 7')
        if not any(i.isdigit() for i in data):
            low = 100
            proc = cv2.cvtColor(cv2.medianBlur(
                cv2.threshold(~cv2.cvtColor(cv2.resize(img, (0, 0), fx=5, fy=5), cv2.COLOR_BGR2GRAY), low, 255, thresh)[
                    1], 3), cv2.COLOR_GRAY2RGB)
            data = image_to_string(Image.fromarray(proc), lang='eng', config='--psm 7')
            if not any(i.isdigit() for i in data):
                low = 125
                proc = cv2.cvtColor(cv2.medianBlur(
                    cv2.threshold(~cv2.cvtColor(cv2.resize(img, (0, 0), fx=5, fy=5), cv2.COLOR_BGR2GRAY), low, 255,
                                  thresh)[1], 3), cv2.COLOR_GRAY2RGB)
                data = image_to_string(Image.fromarray(proc), lang='eng', config='--psm 7')
    else:
        thresh = cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU
        low = 0
        proc = cv2.cvtColor(cv2.medianBlur(
            cv2.threshold(cv2.cvtColor(cv2.resize(img, (0, 0), fx=5, fy=5), cv2.COLOR_BGR2GRAY), low, 255, thresh)[1],
            3), cv2.COLOR_GRAY2RGB)
        data = image_to_string(Image.fromarray(proc), lang='eng', config='--psm 6')
    return data


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
    return int(''.join(filter(str.isdigit, val)))


def char_filter(val):
    return ''.join(filter(str.isalpha, val)).capitalize()
