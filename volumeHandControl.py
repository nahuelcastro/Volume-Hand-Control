import cv2
import numpy as np
import time

import HandTrackingModule as htm

################################
wCam, hCam = 640, 480
################################


cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

while True:
    success, img = cap.read()

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {str(int(fps))}', (10,30), cv2.FONT_HERSHEY_PLAIN, 2, (255,0,255), 3)


    cv2.imshow("Image", img)
    cv2.waitKey(1)