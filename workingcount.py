
import math
import random
import handtrackingmodule as htm
import time
import numpy as np
import cv2
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from playsound import playsound
wCam, hCam = 1280, 640
cam = cv2.VideoCapture(0)
cam.set(2, wCam)
ptime = 0
detector = htm.handdetect(deco=.75)
tp = [4, 8, 12, 16, 20]
z = ['a', 'b', 'y', 'd', 'i']
sign = {'a': [0, 0, 0, 0, 0], 'b': [0, 1, 1, 1, 1], 'y': [
    1, 0, 0, 0, 1], 'd': [0, 1, 0, 0, 0], 'i': [0, 0, 0, 0, 1]}
x = 'a'
count = 0
while True:
    suc, f = cam.read()
    f = detector.findhands(f)
    lm = detector.getpos(f, draw=False)
    cv2.putText(f, str(x), (10, 70),
                cv2.FONT_HERSHEY_COMPLEX, 3, (255, 0, 255), 3)
    cv2.putText(f, str(count), (250, 70),
                cv2.FONT_HERSHEY_COMPLEX, 3, (255, 0, 255), 3)
    if len(lm) != 0:

        # cv2.putText(f, str(x), (10, 70),
        #             cv2.FONT_HERSHEY_COMPLEX, 3, (255, 0, 255), 3)
        fi = []
        if (lm[tp[0]][1] < lm[tp[0]-1][1]):
            fi.append(0)
        else:
            fi.append(1)
        for id in range(1, 5):
            if (lm[tp[id]][2] < lm[tp[id]-2][2]):
                fi.append(1)
            else:
                fi.append(0)

        print(fi)

        if fi != sign[x]:
            continue
        else:
            print("coorect")
            x = random.choice(z)
            # cv2.putText(f, str(x), (10, 70),
            #             cv2.FONT_HERSHEY_COMPLEX, 3, (255, 0, 255), 3)
            count += 1

    ctime = time.time()
    fps = 1/(ctime-ptime)
    ptime = ctime
    # cv2.putText(f, str(int(fps)), (10, 70),
    #             cv2.FONT_HERSHEY_COMPLEX, 3, (255, 0, 255), 3)
    cv2.imshow("image", f)
    cv2.waitKey(1)
