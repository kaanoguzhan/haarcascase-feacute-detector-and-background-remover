#! /usr/bin/python

import cv2
from itertools import count

#Read Haarcascades
face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')
if face_cascade.empty():
    exit("! Missing: haarcascade_frontalface_default.xml !\nYou need to run the main.py from the project directory")
eye_cascade = cv2.CascadeClassifier('haarcascades/haarcascades/frontalEyes.xml')
if eye_cascade.empty():
    exit("! Missing: haarcascade_eye.xml !\nYou need to run the main.py from the project directory")

#Read Image
imgGlasses = cv2.imread('images/moustache.png', -1)
if imgGlasses is None:
    exit("Could not open the image")

noseHeight = 65
noseWidth = 55



# Check if the files opened
if imgGlasses is None:
    exit("Could not open the image")
if face_cascade.empty():
    exit("Missing: haarcascade_frontalface_default.xml")
if eye_cascade.empty():
    exit("Missing: haarcascade_eye.xml")

# Create the mask for the glasses
imgGlassesGray = cv2.cvtColor(imgGlasses, cv2.COLOR_BGR2GRAY)
ret, orig_mask = cv2.threshold(imgGlassesGray, 10, 255, cv2.THRESH_BINARY)

orig_mask = imgGlasses[:, :, 3]

# Create the inverted mask for the glasses
orig_mask_inv = cv2.bitwise_not(orig_mask)

# Convert glasses image to BGR
# and save the original image size (used later when re-sizing the image)
imgGlasses = imgGlasses[:, :, 0:3]
origGlassesHeight, origGlassesWidth = imgGlasses.shape[:2]


counter = count(1)

def _putmoustache_(frame):


    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        #cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        drawNose = False
        for (ex, ey, ew, eh) in eyes:

            eyetemp = [10, 10, 10, 10]
            if ew > eyetemp[2] or eh > eyetemp[3]:
                #print 'ey:%i, y:%i, h:%i' % (ey, y, h,)
                if ey > (h*25/100):
                    drawNose = True
                    eyetemp[0] = ex
                    eyetemp[1] = ey
                    eyetemp[2] = ew
                    eyetemp[3] = eh
                    print("Nose Found")

            if eyetemp[0] == 10 or eyetemp[1] == 10 or eyetemp[2] == 10:
                drawNose = False

        if drawNose:
            #print 'X:%i, Y:%i, W:%i, H:%i' % (ex, ey, ew, eh)
            ex = eyetemp[0]
            ey = eyetemp[1]
            ew = eyetemp[2]
            eh = eyetemp[3]

            ##cv2.rectangle(roi_color, (ex+(ew/5), ey-(eh/5)), (ex + ew, ey + (eh*2/3)), (0, 255, 0), 2)

            glassesWidth = 3 * ew
            glassesHeight = glassesWidth * origGlassesHeight / origGlassesWidth

            x1 = int(ex - (glassesWidth / 6))
            x2 = int(ex + ew + (glassesWidth / 4))
            y1 = int(ey + 9*eh/10 - (glassesHeight / 2))
            y2 = int(ey + 70*eh/100 + (glassesHeight / 2))

            if x1 < 0:
                x1 = 0
            if y1 < 0:
                y1 = 0
            if x2 > w:
                x2 = w
            if y2 > h:
                y2 = h

            glassesWidth = x2 - x1
            glassesHeight = y2 - y1
            if glassesWidth < 0:
                glassesWidth = 0
            if glassesHeight < 0:
                glassesHeight = 0

            imgGlasses2 = cv2.GaussianBlur(imgGlasses, (9 ,9),0)
            glasses = cv2.resize(imgGlasses2, (glassesWidth, glassesHeight), interpolation=cv2.INTER_AREA)
            mask = cv2.resize(orig_mask, (glassesWidth, glassesHeight), interpolation=cv2.INTER_AREA)
            mask_inv = cv2.resize(orig_mask_inv, (glassesWidth, glassesHeight), interpolation=cv2.INTER_AREA)

            roi = roi_color[y1:y2, x1:x2]

            roi_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)

            roi_fg = cv2.bitwise_and(glasses, glasses, mask=mask)

            dst = cv2.add(roi_bg, roi_fg)

            roi_color[y1:y2, x1:x2] = dst
    # break
    # Display the resulting frame
    return frame


