import cv2
import numpy as np
import os
import time
import handtrackingmodule as htm
ptime = 0
drawColor = (255, 0, 255)
detector = htm.handdetect(deco=1)
cam = cv2.VideoCapture(0)
cam.set(3, 1280)
cam.set(4, 720)
imc = np.zeros((720, 1280, 3), np.uint8)
xp, yp = 0, 0
while True:
    suc, f = cam.read()
    f = cv2.flip(f, 1)
    f = detector.findhands(f)
    lm = detector.getpos(f, draw=False)
    fd = []
    tp = [4, 8, 12, 16, 20]

    if len(lm) != 0:
        x1, y1 = lm[8][1:]
        x2, y2 = lm[12][1:]
        if lm[tp[0]][1] < lm[tp[1]][1]:
            fd.append(1)
        else:
            fd.append(0)
        for id in range(1, 5):
            if (lm[tp[id]][2] < lm[tp[id]-2][2]):
                fd.append(1)
            else:
                fd.append(0)
        if fd[1] and fd[2]:
            xp, yp = 0, 0
            # print(“Selection Mode”)
            # # Checking for the click
            cv2.rectangle(f, (x1, y1 - 25), (x2, y2 + 25),
                          drawColor, cv2.FILLED)
            cv2.line(f, (x1, y1), (x2, y2), (255, 0, 255), 2)
            if y1 < 125:
                if 250 < x1 < 450:
                    # header = overlayList[0]
                    drawColor = (255, 0, 255)
                elif 550 < x1 < 750:
                    # header = overlayList[1]
                    drawColor = (255, 0, 0)
                elif 800 < x1 < 950:
                    # header = overlayList[2]
                    drawColor = (0, 255, 0)
                elif 1050 < x1 < 1200:
                    # header = overlayList[3]
                    drawColor = (0, 0, 0)
                # cv2.rectangle(img, (x1, y1 – 25), (x2, y2 + 25), drawColor, cv2.FILLED)
                #             cv2.line(f, (x1, y1), (x2, y2), (255, 0, 255), 2)

        elif fd[1] and fd[2] == 0:
            cv2.circle(f, (x1, y1), 10, drawColor, cv2.FILLED)
            if xp == 0 and yp == 0:
                xp, yp = x1, y1
            # cv2.line(imc, (xp, yp), (x1, y1), drawColor, 4)
            # xp, yp = x1, y1

            if drawColor == (0, 0, 0):
                cv2.line(f, (xp, yp), (x1, y1), drawColor, 100)
                cv2.line(imc, (xp, yp), (x1, y1), drawColor, 100)

            else:
                cv2.line(f, (xp, yp), (x1, y1), drawColor, 15)
                cv2.line(imc, (xp, yp), (x1, y1), drawColor, 15)

            xp, yp = x1, y1

        if all(x >= 1 for x in fd):
            imgCanvas = np.zeros((720, 1280, 3), np.uint8)

        # print(fd)
    imgGray = cv2.cvtColor(imc, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    f = cv2.bitwise_and(f, imgInv)
    f = cv2.bitwise_or(f, imc)

    ctime = time.time()
    fps = 1/(ctime-ptime)
    ptime = ctime
    cv2.putText(f, str(int(fps)), (10, 70),
                cv2.FONT_HERSHEY_COMPLEX, 3, (255, 0, 255), 3)
    cv2.imshow("image", f)
    cv2.imshow("draw", imc)
    cv2.waitKey(1)
