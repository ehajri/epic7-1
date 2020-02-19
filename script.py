#!/usr/bin/python
import sys
import time
from functions import *
from PIL import ImageGrab
import numpy as np
resolution = "1600"
coords = COORDS[resolution]

def analyze(img):
    mark = cv2.imread(coords['MARKS']['TOP'], 0)
    res = cv2.matchTemplate(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), mark, cv2.TM_CCOEFF_NORMED)
    cv2.imshow('', res)
    cv2.imshow('i', img)

    cv2.waitKey()
    cv2.destroyAllWindows()
    minv, maxv, min_loc, max_loc = cv2.minMaxLoc(res)
    if maxv < 0.9:
        print('invalid screen')
        return None
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
    for k in top_coords:
        if k != 'PLUS': continue
        crds = top_coords[k]
        data = process(k, top_box_g[crds[0][0]:crds[0][1], crds[1][0]:crds[1][1]], top_box[crds[0][0]:crds[0][1], crds[1][0]:crds[1][1]])
        if k == 'LVL':
            export["ilvl"] = digit_filter(data.replace('S', '5').replace('B', '8').replace('a', '8'))

        if k == 'PLUS':
            export["enhance"] = digit_filter(
                data.replace('S', '5').replace('B', '8').replace('a', '8').replace('+h', '4').replace('1g', '14'))

        if k == 'TYPE':
            export["grade"] = char_filter(data.split(' ')[0])
            export["slot"] = char_filter(data.split(' ')[1].split('\n')[0])
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

def main_loop():
    while 1:
        time.sleep(5)
        wtf = ImageGrab.grab()
        wtf = cv2.cvtColor(np.array(wtf), cv2.COLOR_RGB2BGR)
        d = analyze(wtf)
        if d != None:
            print(d)

if __name__ == "__main__":
    try:
        main_loop()
    except KeyboardInterrupt:
        sys.stderr.write('\nExiting by user request.\n')
        sys.exit(0)