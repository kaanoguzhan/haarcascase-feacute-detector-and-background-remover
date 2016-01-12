#! /usr/bin/python

from cv2 import VideoCapture,imshow,destroyAllWindows,waitKey,pyrDown,imread,pyrUp,GaussianBlur
from glasses import _putglass_
from moustache import _putmoustache_
from itertools import count

backgroundTreshold = 20

beach = imread('manzara640.png', -1)

video_capture = VideoCapture(0)

if not video_capture.isOpened():
    exit('The Camera is not opened')

counter = count(1)

for i in range(0, 50):
    ret, background = video_capture.read()
    imshow("Video", background)
    waitKey(10)
    print "!!! Step out of the frame !!!"
    print "Background will be detected in %d seconds" % (7 - i)
ret, background = video_capture.read()
background = pyrDown(background)
#background = pyrDown(background)

while True:
    print "Iteration %d" % counter.next()

    ret, temp = video_capture.read()
    temp = pyrDown(temp)
    frame2 = _putmoustache_(temp)
    frame3 = _putglass_(frame2)

    #frame3 = pyrDown(frame3)
    #Display the resulting frame
    height, width = frame3.shape[:2]
    for i in range(1, height, 4):
        for j in range(1, width, 4):
            if background[i][j][0] - backgroundTreshold <= frame3[i][j][0] <= background[i][j][0] + backgroundTreshold:
                if background[i][j][0] - backgroundTreshold <= frame3[i][j][1] <= background[i][j][1] + backgroundTreshold:
                    if background[i][j][0] - backgroundTreshold <= frame3[i][j][2] <= background[i][j][2] + backgroundTreshold:
                        for x in range(-2, 2):
                            for y in range(-2, 2):
                                frame3[i+x][j+y][0] = beach[i+x][j+y][0]
                                frame3[i+x][j+y][1] = beach[i+x][j+y][1]
                                frame3[i+x][j+y][2] = beach[i+x][j+y][2]

    #frame3 = pyrUp(frame3)
    frame3 = pyrUp(frame3)
    imshow("Video", frame3)
    waitKey(250)

# When everything is done, release the capture
video_capture.release()
destroyAllWindows()


