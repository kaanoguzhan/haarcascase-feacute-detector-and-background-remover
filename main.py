#! /usr/bin/python

from cv2 import VideoCapture,imshow,destroyAllWindows,waitKey,pyrDown,imread
from glasses import _putglass_
from moustache import _putmoustache_
from itertools import count

backgroundTreshold = 20

beach = imread('manzara.png', -1)

video_capture = VideoCapture(0)

if not video_capture.isOpened():
    exit('The Camera is not opened')

counter = count(1)

ret, background = video_capture.read()
background = pyrDown(background)
imshow("back",background)
waitKey()
ret, background = video_capture.read()
background = pyrDown(background)
background = pyrDown(background)
imshow("back",background)

while True:
    print "Iteration %d" % counter.next()

    ret, temp = video_capture.read()
    temp = pyrDown(temp)
    frame = pyrDown(temp)
    frame2 = _putmoustache_(frame)
    frame3 = _putglass_(frame2)


    # Display the resulting frame
    height, width = frame3.shape[:2]
    for i in range(0, height ):
        for j in range(0, width):
            if background[i][j][0] - backgroundTreshold <= frame3[i][j][0] <= background[i][j][0] + backgroundTreshold:
                frame3[i][j][0] = beach[i][j][0]
                frame3[i][j][1] = beach[i][j][1]
                frame3[i][j][2] = beach[i][j][2]
                if background[i][j][0] - backgroundTreshold <= frame3[i][j][1] <= background[i][j][1] + backgroundTreshold:
                    frame3[i][j][0] = beach[i][j][0]
                    frame3[i][j][1] = beach[i][j][1]
                    frame3[i][j][2] = beach[i][j][2]
                    if background[i][j][0] - backgroundTreshold <= frame3[i][j][2] <= background[i][j][2] + backgroundTreshold:
                        frame3[i][j][0] = beach[i][j][0]
                        frame3[i][j][1] = beach[i][j][1]
                        frame3[i][j][2] = beach[i][j][2]
    imshow("Video", frame3)
    waitKey(5)

# When everything is done, release the capture
video_capture.release()
destroyAllWindows()


