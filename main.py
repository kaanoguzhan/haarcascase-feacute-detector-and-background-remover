#! /usr/bin/python

from cv2 import VideoCapture,imshow,destroyAllWindows,waitKey,pyrDown
from glasses import _putglass_
from moustache import _putmoustache_
from itertools import count

video_capture = VideoCapture(0)

if not video_capture.isOpened():
    exit('The Camera is not opened')

counter = count(1)

while True:
    print "Iteration %d" % counter.next()

    ret, temp = video_capture.read()
    frame = pyrDown(temp)

    frame2 = _putmoustache_(frame)
    frame3 = _putglass_(frame2)

    # Display the resulting frame
    imshow("Video", frame3)
    waitKey(5)

# When everything is done, release the capture
video_capture.release()
destroyAllWindows()


