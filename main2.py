#! /usr/bin/python

import cv2
from glasses import __test__
from itertools import count

video_capture = cv2.VideoCapture(0)

if not video_capture.isOpened():
    exit('The Camera is not opened')

counter = count(1)

while True:
    print "Iteration %d" % counter.next()

    frame = __test__(video_capture)

    # Display the resulting frame
    cv2.imshow('Video', frame)


# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
