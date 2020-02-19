import sys
from functions import *
from glob import glob
from os import path
import cProfile, pstats, io
from pstats import SortKey

profiling = False
if profiling:
    pr = cProfile.Profile()
    pr.enable()

resolution = "1600"
marks = ["e7/top.jpg", "e7/mark.png"]
coords = COORDS[resolution]
mark = cv2.imread(coords['MARKS']['TOP'], 0)
dir = './screenshots/'
temp_bot = cv2.imread(coords['MARKS']['BOTTOM'], 0)

counter = 0
counterA = 0
counterB = 0
counterZ = 0
counterZZ = 0
listA = []
listB = []
listZ = []


def hello(img, part, debug=False):
    id = path.basename(img).replace('.png', '')
    img = cv2.imread(img)
    res = cv2.matchTemplate(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), mark, cv2.TM_CCOEFF_NORMED)
    minv, maxv, min_loc, max_loc = cv2.minMaxLoc(res)
    if maxv < 0.9:
        print("Top Mark Not found for", img)
        exit()
    TB_H = coords["TOP_BOX"]["HEIGHT"]
    TB_W = coords["TOP_BOX"]["WIDTH"]
    y1 = max_loc[1]
    y2 = max_loc[1] + TB_H
    x1 = max_loc[0] - TB_W
    x2 = max_loc[0]
    top_box = img[y1:y2, x1:x2]
    top_box_g = cv2.cvtColor(top_box, cv2.COLOR_BGR2GRAY)
    top_coords = coords["TOP"]
    BOTTOM_X = x2 - coords["TOP_BOX"]["WIDTH"]
    _, _, _, max_loc = cv2.minMaxLoc(
        cv2.matchTemplate(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), temp_bot, cv2.TM_CCOEFF_NORMED))

    BB = coords["BOTTOM_BOX"]
    bottom_box = img[max_loc[1] + BB['SHIFT']:max_loc[1] + BB['HEIGHT'] + BB['SHIFT'], BOTTOM_X:BOTTOM_X + BB['WIDTH']]
    bottom_box_g = cv2.cvtColor(bottom_box, cv2.COLOR_BGR2GRAY)
    bottom_coords = coords["BOTTOM"]

    k = part.upper()

    if k in top_coords.keys():
        crds = top_coords[k]
        img1 = top_box_g
        img2 = top_box
    else:
        crds = bottom_coords[k]
        img1 = bottom_box_g
        img2 = bottom_box

    data = process(k, img1[crds[0][0]:crds[0][1], crds[1][0]:crds[1][1]],
                   img2[crds[0][0]:crds[0][1], crds[1][0]:crds[1][1]], debug)
    if debug: print(data)

    gear = inv[int(id) - 1]

    if k == 'LVL':
        y = gear['ilvl']
        x = digit_filter(data.replace('S', '5').replace('B', '8').replace('a', '8'))
        if y != x:
            print(id, y, x)

    if k == 'PLUS':
        global counter, counterA, counterB, counterZ, counterZZ
        # global xyz
        # try:
        #     if xyz:
        #         None
        # except NameError:
        #     print('id\tinv\tnew\told')
        #     xyz = True

        y = gear['enhance']
        # print('processing', id)
        # print('inventory enhance: %i' % y)
        # print('data:', data)
        if y == 0:
            return

        counter += 1
        z = digit_filter(
            data.replace('S', '5').replace('B', '8').replace('a', '8').replace('+h', '4').replace('1g', '14'))#.replace('19', '15'))
        # print('Z:', z)
        if y == z:
            counterB += 1
        else:
            listB.append(id)

    if k == 'TYPE':
        grade = char_filter(data.split(' ')[0])
        slot = char_filter(data.split(' ')[1].split('\n')[0])
        if gear['grade'] != grade:
            print('Grade for (%s) %s vs %s' % (id, gear['grade'], grade))
        if gear['slot'] != slot:
            print('Slot for (%s) %s vs %s' % (id, gear['slot'], slot))

    if k == 'MAIN':
        stat = stat_converter(data)
        value = digit_filter(data)
        main = gear['main']

        if main['stat'] != stat:
            print('Main Stat for (%s) %s vs %s' % (id, main['stat'], stat))
        if main['value'] != value:
            print('Main Stat Value for (%s) %s vs %s' % (id, main['value'], value))


    if k == 'SUBS':
        subs = gear['subs']
        stats = [i['stat'] for i in subs]
        for n, entry in enumerate(data.split('\n')):
            stat = stat_converter(entry)
            value = digit_filter(entry.replace('T%', '7%'))

            obj = next((x for x in subs if x['stat'] == stat), None)

            if not obj:
                print('Unknown Substat [%s] for (%s) in %s' % (stat, id, ' '.join(stats)))
            else:
                if obj['value'] != value:
                    print('Substat Value for (%s) %i vs %i' % (id, obj['value'], value))

    if k == 'SET':
        set = char_filter(data.split(' Set')[0])
        if gear['set'] != set:
            print('Set for (%s) %s vs %s' % (id, gear['set'], set))

if __file__ == sys.argv[0]:
    args = sys.argv
    part = None
    which = None
    debug = None
    if len(args) > 1:
        part = args[1]
    if len(args) > 2:
        which = args[2]
        which = dir + str(which) + '.png'
    if len(args) > 3:
        debug = True if args[3] == 'true' else False

    if part and part in ['lvl', 'plus', 'type', 'main', 'subs', 'set']:
        if which and glob(which):
            hello(which, part, debug)
        else:
            files = sorted(glob(dir + '*.png'))
            for file in files:
                hello(file, part)
                # id = int(path.basename(file).replace('.png', ''))
                # if id in [6, 33]:
                #     hello(file, part)
            if part == 'plus':
                print('Accuracy B is', round(counterB/counter*100, 2))
                if listB:
                    print(', '.join(listB))

                if profiling:
                    pr.disable()
                    s = io.StringIO()
                    sortby = SortKey.CUMULATIVE
                    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
                    ps.print_stats()
                    print(s.getvalue())


    # check = True if len(sys.argv) > 1 and sys.argv[1] == 'check' else False
    # if len(sys.argv) == 3 and glob(dir + str(sys.argv[2]) + '.png'):
    #     single = dir + str(sys.argv[2]) + '.png'
    # else:
    #     single = False
    #
    # if single:
    #     hello(single)
    # else:
    #     for file in glob.glob('./screenshots/*.png'):
    #         hello(file)
    #
