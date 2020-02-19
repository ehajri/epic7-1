import cv2
from pytesseract import image_to_string
from PIL import Image
import numpy as np

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
plus_mark = cv2.imread('./e7/plus.png')

def plus_mode1(img):
    test = cv2.bitwise_not(img)
    test = cv2.resize(test, (0, 0), fx=0.5, fy=0.5)

    data = image_to_string(Image.fromarray(test), lang='eng', config='--psm 7')
    return data

def lvl_mode1(img):
    test = cv2.bitwise_not(img)
    test = cv2.resize(test, (0, 0), fx=0.5, fy=0.5)
    data = image_to_string(Image.fromarray(test), lang='eng', config='--psm 7')
    return data

def process(k, imgg, img):
    if not(k in ['LVL', 'PLUS', 'TYPE']):
        thresh = cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU
        low = 0
        proc = cv2.medianBlur(
            cv2.threshold(cv2.resize(imgg, (0, 0), fx=2, fy=2), low, 255, thresh)[1],
            3)

        data = image_to_string(Image.fromarray(proc), lang='eng', config='--psm 6')
        return data
    if k == 'TYPE':
        img[np.where((img <= [40, 40, 40]).all(axis=2))] = [255, 255, 255]
        x = image_to_string(Image.fromarray(img), lang='eng', config='--psm 6')
        return x.replace('delmet', 'Helmet')

    if k == 'PLUS':
        res = cv2.matchTemplate(img, plus_mark, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        if np.amax(res) <= threshold:
            return '0'

        data = plus_mode1(img)

        return data

    # LVL
    return lvl_mode1(img)

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
