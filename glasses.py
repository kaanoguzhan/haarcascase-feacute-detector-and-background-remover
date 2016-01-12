#! /usr/bin/python

import cv2

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
if face_cascade.empty():
    exit("Missing: haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier('haarcascades/frontalEyes.xml')
if eye_cascade.empty():
    exit("Missing: haarcascade_eye.xml")
imgGlasses = cv2.imread('rayban.png', -1)
if imgGlasses is None:
    exit("Could not open the image")

# Create the mask for the glasses
imgGlassesGray = cv2.cvtColor(imgGlasses, cv2.COLOR_BGR2GRAY)
ret, orig_mask = cv2.threshold(imgGlassesGray, 10, 255, cv2.THRESH_BINARY)

orig_mask = imgGlasses[:, :, 3]
imgGlasses = imgGlasses[:, :, 0:3]
origGlassesHeight, origGlassesWidth = imgGlasses.shape[:2]

# Create the inverted mask for the glasses
orig_mask_inv = cv2.bitwise_not(orig_mask)


def _putglass_(frame):


    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        #cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]
        eyes = eye_cascade.detectMultiScale(roi_gray)

        drawNose = False
        for (ex, ey, ew, eh) in eyes:
            eyetemp = [40, 40, 40, 40]
            if ew > eyetemp[2] or eh > eyetemp[3]:
                #print 'ey:%i, y:%i, h:%i' % (ey, y, h,)
                drawNose = True
                eyetemp[0] = ex
                eyetemp[1] = ey
                eyetemp[2] = ew
                eyetemp[3] = eh
                print "Nose Found"

        if drawNose:
            # print 'X:%i, Y:%i, W:%i, H:%i' % (x, y, w, h)
            ex = eyetemp[0]
            ey = eyetemp[1]
            ew = eyetemp[2]
            eh = eyetemp[3]

            #cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
            #print 'EX:%i, EY:%i, EW:%i, EH:%i' % (ex, ey, ew, eh)

            glassesWidth = ew
            glassesHeight = glassesWidth * origGlassesHeight / origGlassesWidth


            x1 = ex - (glassesWidth / 6)
            x2 = ex + ew + (glassesWidth / 6)
            y1 = ey + (45*eh/100) - (glassesHeight / 2)
            y2 = ey + 65*eh/100 + (glassesHeight / 2)

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

            # take region of interest from the image
            roi = roi_color[y1:y2, x1:x2]

            # where the glasses are not in the image
            roi_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)

            # only glasses
            roi_fg = cv2.bitwise_and(glasses, glasses, mask=mask)

            # joined together
            dst = cv2.add(roi_bg, roi_fg)

            # place the original image to the region of interest
            roi_color[y1:y2, x1:x2] = dst


    return frame
