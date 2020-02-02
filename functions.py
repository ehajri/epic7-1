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
COORDS = {
    "1600": {
        "MARK": "e7/mark.png",
        "LVL": [[35, 82], [58, 116]],
        "PLUS": [[13, 65], [220, 270]],
        "TYPE": [[35, 95], [280, 650]],
        "BOTTOM": {
            "MAIN": [[25, 110], [105, 665]],
            "SUBS": [[150, 400], [25, 655]],
            "SET": [[460, 525], [120, 435]]
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

# refactor this function
def process(k, img):
    if not(k in ['level', 'plus']):
        thresh = cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU
        low = 0
        proc = cv2.cvtColor(cv2.medianBlur(
            cv2.threshold(cv2.cvtColor(cv2.resize(img, (0, 0), fx=10, fy=10), cv2.COLOR_BGR2GRAY), low, 255, thresh)[1],
            3), cv2.COLOR_GRAY2RGB)
        return image_to_string(Image.fromarray(proc), lang='eng', config='--psm 6')

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