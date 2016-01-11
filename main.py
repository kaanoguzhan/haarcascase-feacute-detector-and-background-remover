#! /usr/bin/python

from cv2 import VideoCapture,imshow,destroyAllWindows,waitKey
from glasses import _putGlass_
from itertools import count

video_capture = VideoCapture(0)

if not video_capture.isOpened():
    exit('The Camera is not opened')

counter = count(1)

while True:
    print "Iteration %d" % counter.next()

    frame = _putGlass_(video_capture)

    # Display the resulting frame
    imshow("Video", frame)
    waitKey(5)

# When everything is done, release the capture
video_capture.release()
destroyAllWindows()

