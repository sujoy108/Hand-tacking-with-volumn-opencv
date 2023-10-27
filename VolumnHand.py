import cv2
import time
import numpy as np
import handTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


wCam,hCam=1024,768


cap=cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
pTime=0

detector=htm.handDetector(detectionCon=0.7,maxHands=1)

devices=AudioUtilities.GetSpeakers()
interface=devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL,None)
volumn= cast(interface,POINTER(IAudioEndpointVolume))
volRange=volumn.GetVolumeRange()
minVol=volRange[0]
maxVol=volRange[1]
vol=0
volBar=400
volPer=0
colorV=(255,0,0)
while True:
    sucess,img=cap.read()
    img=detector.findHands(img)
    lmList, bbox=detector.findPosition(img,draw=True)
    if len(lmList)!=0:

        area=(bbox[2]-bbox[0])* (bbox[3]-bbox[1])//100
        #print(area)

        if 250<area<2000:
            #print("yes")
            length,img,lineInfo = detector.findDistance(4,8,img)

            #vol=np.interp(length,[50,300],[minVol,maxVol])
            volBar=np.interp(length,[50,300],[400,150])
            volPer=np.interp(length,[50,300],[0,100])
            #print(int(length),vol)
            #print(int(volBar))
            #volumn.SetMasterVolumeLevel(vol,None)
            smooth=5
            volPer=smooth*round(volPer/smooth)
            

            fingers=detector.fingersUp()
            
            if not fingers[4]:
                volumn.SetMasterVolumeLevelScalar(volPer/100,None)
                cv2.circle(img,(lineInfo[4],lineInfo[5]),5,(0,255,0),cv2.FILLED)
                colorV=(125,159,0)
            elif not fingers[2]:
                cv2.waitKey(1)
                break

            else:
                colorV=(255,0,0)
            
                
        
    cv2.rectangle(img,(50,150),(75,400),(255,1,2),2)
    cv2.rectangle(img,(50,int(volBar)),(75,400),(255,0,0),cv2.FILLED)
    cv2.putText(img,f'{int(volPer)} %',(40,450),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,255),2)
    cVol=int(volumn.GetMasterVolumeLevelScalar()*100)
    cv2.putText(img,f'Vol Set : {int(cVol)} %',(650,40),cv2.FONT_HERSHEY_COMPLEX,1,colorV,2)



    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime

    cv2.putText(img,f'{int(fps)}',(30,50),cv2.FONT_HERSHEY_COMPLEX,1,(124,255,0),2)
    cv2.imshow("Image",img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()


