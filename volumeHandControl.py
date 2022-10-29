import cv2
import numpy as np
import time
import math
import HandTrackingModule as htm
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


################################
wCam, hCam = 640, 480
handRangeMax = 350
handRangeMin = 60
################################

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = htm.HandDetector(detectionCon=0.7)
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
volBar = 400
volInit = volume.GetMasterVolumeLevel()
volPer = np.interp(volInit, [minVol, maxVol], [0, 100])
# volPer = volInit

while True:
    success, img = cap.read()
    detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1 + x2)//2, (y1 + y2)//2
        lenght = math.hypot(x2 - x1, y2 - y1)


        cv2.circle(img, (x1, y1), 12, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 12, (255, 0, 255), cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)
        cv2.circle(img, (cx, cy), 12, (255, 0, 255), cv2.FILLED)


        vol = np.interp(lenght, [handRangeMin, handRangeMax], [minVol, maxVol]) # map lenght to volume
        volPer = np.interp(lenght, [handRangeMin, handRangeMax], [0, 100]) # map lenght to volume
        volBar = np.interp(lenght, [handRangeMin, handRangeMax], [400, 150]) # map lenght to volume

        cv2.putText(img, 'len: ' + str(int(lenght)), (500, 30), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)
        volume.SetMasterVolumeLevel(vol, None)

    cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, f'Vol: {str(int(volPer))} %', (40, 450), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)



    # FPS viewer
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {str(int(fps))}', (10,30), cv2.FONT_HERSHEY_PLAIN, 2, (255,0,255), 3)


    cv2.imshow("Image", img)
    cv2.waitKey(1)