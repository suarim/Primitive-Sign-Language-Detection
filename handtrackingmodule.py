import cv2
import mediapipe as mp
import time
import math


class handdetect():
    def __init__(self, mode=False, maxHands=2, deco=.5):
        self.mode = mode
        self.maxHands = maxHands
        # self.moc = moc
        self.deco = deco
        # self.trackcon = trackcon
        self.mphands = mp.solutions.hands
        self.hands = self.mphands.Hands(
            self.mode, self.maxHands,)
        self.mpDraw = mp.solutions.drawing_utils

    def findhands(self, f, draw=True):
        imgRGB = cv2.cvtColor(f, cv2.COLOR_BGR2RGB)
        self.result = self.hands.process(imgRGB)
        # print(result.multi_hand_landmarks)
        if self.result.multi_hand_landmarks:
            for hl in self.result.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(
                        f, hl, self.mphands.HAND_CONNECTIONS)
        return f

    def getpos(self, f, handno=0, draw=True):
        self.lmlist = []
        if self.result.multi_hand_landmarks:
            myhand = self.result.multi_hand_landmarks[handno]
            for id, lm in enumerate(myhand.landmark):
                h, w, c = f.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                # print(id, cx, cy)
                self.lmlist.append([id, cx, cy])

        return self.lmlist

    def findangle(self, f, p1, p2, p3, draw=True):
        if (len(self.lmlist)) != 0:
            x1, y1 = self.lmlist[p1][1], self.lmlist[p1][2]
            x2, y2 = self.lmlist[p2][1], self.lmlist[p2][2]
            x3, y3 = self.lmlist[p3][1], self.lmlist[p3][2]
            angle = math.degrees(math.atan2(
                (y3-y2), (x3-x2))-math.atan2(y1-y2, x1-x2))
            print(angle)
        if draw:
            cv2.circle(f, (x1, y1), 10, (225, 140, 0), cv2.FILLED)
            cv2.circle(f, (x2, y2), 10, (225, 140, 0), cv2.FILLED)
            cv2.circle(f, (x3, y3), 10, (225, 140, 0), cv2.FILLED)


def main():
    ptime = 0
    ctime = 0
    cam = cv2.VideoCapture(0)
    detector = handdetect()

    while True:
        suc, f = cam.read()
        f = detector.findhands(f)
        # lmlist=detector.getpos(f)
        lmlist = detector.getpos(f)
        # if len(lmlist) != 0:
        #     print(lmlist[0])
        ctime = time.time()
        fps = 1/(ctime-ptime)
        ptime = ctime
        cv2.putText(f, str(int(fps)), (10, 70),
                    cv2.FONT_HERSHEY_COMPLEX, 3, (255, 0, 255), 3)
        cv2.imshow("image", f)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
