# import numpy as np
# import cv2
#
# cap = cv2.VideoCapture(0)
#
# kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
# fgbg = cv2.BackgroundSubtractorMOG()
#
# while True:
#     ret, frame = cap.read()
#
#     fgmask = fgbg.apply(frame)
#     fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
#
#     cv2.imshow('frame',fgmask)
#     k = cv2.waitKey(30) & 0xff
#     if k == 27:
#         break
#
# cap.release()
# cv2.destroyAllWindows()

import numpy as np
import cv2

cap = cv2.VideoCapture(0)

imgParis = cv2.imread('paris.png')

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
fgbg = cv2.BackgroundSubtractorMOG(history=3, nmixtures=5, backgroundRatio=0.0001)

while True:
    ret, frame = cap.read()

    fgmask = fgbg.apply(frame, learningRate=0.00000000000000000000000000001)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)

    cv2.imshow('frame',fgmask)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()