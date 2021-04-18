import cv2
from .script_color import colorzRGB
from multiprocessing.pool import ThreadPool

pool = ThreadPool(processes=7)


def summ(a, b):
    for i in range(len(a)):
        for j in range(len(a[i])):
            a[i][j] += b[i][j]
    return a


def lilAver(pic):
    r = 0
    g = 0
    b = 0
    c = len(pic)
    for i in range(c):
        r += pic[i][0]
        g += pic[i][1]
        b += pic[i][2]
    return [r / c, g / c, b / c]


def average(avr):
    first = []
    second = []
    third = []
    for i in range(len(avr)):
        first.append(avr[i][0])
        second.append(avr[i][1])
        third.append(avr[i][2])
    aver = [lilAver(first), lilAver(second), lilAver(third)]
    return aver


def madehtml(hexs):
    html = "<!DOCTYPE html>" \
           "<html>" \
           "<head>" \
           "</head>" \
           "<body>" \
           "<div>" \
           "<table>" \
           "<thead>" \
           "<tr><th>1</th><th>2</th><th>3</th>" \
           "</thead>" \
           "<tbody>"
    for h in hexs:
        # h.sort()
        html += f'<tr><th style="width: 60px; height: 60px; background-color:rgb({h[0][0]}, {h[0][1]}, {h[0][2]})"></th><th style="width: 60px; height: 60px; background-color:rgb({h[1][0]}, {h[1][1]}, {h[1][2]})"></th><th style="width: 60px; height: 60px; background-color:rgb({h[2][0]}, {h[2][1]}, {h[2][2]})"></th></tr>'
    html += '</tbody>' \
            '</table>' \
            '</body>'
    return html


def rgbError(rgb):
    rmin = rgb[0] - 50
    gmin = rgb[1] - 50
    bmin = rgb[2] - 50
    rmax = rgb[0] + 50
    gmax = rgb[1] + 50
    bmax = rgb[2] + 50
    min = [rmin, gmin, bmin]
    max = [rmax, gmax, bmax]
    return [min, max]


def compareOne(rgb, frgb):
    com = True
    if not (rgbError(rgb)[0][0] <= frgb[0] <= rgbError(rgb)[1][0]):
        com = False
    if not (rgbError(rgb)[0][1] <= frgb[1] <= rgbError(rgb)[1][1]):
        com = False
    if not (rgbError(rgb)[0][2] <= frgb[2] <= rgbError(rgb)[1][2]):
        com = False
    else:
        return com


def compare(rgbs):
    if len(rgbs) <= 1:
        return True
    if len(rgbs) >= 3:
        rgbs.pop(1)
    if (compareOne(rgbs[1][0], rgbs[0][0]) and compareOne(rgbs[1][1], rgbs[0][1]) and compareOne(rgbs[1][2],
                                                                                                 rgbs[0][2])):
        return True
    else:
        return False

def start():
    cap = cv2.VideoCapture(0)
    rgbs = []
    avr = []
    for i in range(10):
        ret, img = cap.read()
        cv2.imwrite('img.png', img)
        async_result = pool.apply_async(colorzRGB, ('img.png',))
        rgba = async_result.get()
        print('123')
        rgba.sort()
        avr.append(rgba)
    aver = average(avr)

    while (compare(rgbs)):
        ret, img = cap.read()
        cv2.imwrite('img.png', img)
        async_result = pool.apply_async(colorzRGB, ('img.png',))
        rgba = async_result.get()
        rgba.sort()
        avr.append(rgba)
        aver = average(avr)
        rgbs = [aver, rgba]
        flag = True
        if not compare(rgbs):
            flag = False
            return False
            # ctypes.windll.user32.LockWorkStation()

    cap.release()
    cv2.destroyAllWindows()
    file = open('html.html', 'w')
    html = madehtml(rgbs)
    file.write(html)
    file.close()
    # file = open('html2.html', 'w')
    # html = madehtml(rgbTest)
    # file.write(html)
    # file.close()
