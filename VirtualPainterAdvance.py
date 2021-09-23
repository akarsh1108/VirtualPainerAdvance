import cv2
import numpy as np
import time
import os
import HandTrackingModule as htm

brushThickness=15
eraserThickness=50

folderPath= "resources"
myList= os.listdir(folderPath)
# print(myList)
overlayList = []
for imPath in myList:
    image=cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)
# print(len(overlayList))
header = overlayList[0]

cap=cv2.VideoCapture(0)
cap.set(3,1210)
cap.set(4,720)
drawColor=(255,0,255)

detector = htm.handDetector(detectionCon=0.75)
xp,yp=0,0
imgCanvas = np.zeros((720,1210,3),np.uint8)

def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver

while True:
    # 1.Import the image
    success,img=cap.read()
    img=cv2.flip(img,1)
    #2.Find Hand Landmarks
    img=detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList)!=0:

        # print(lmList)
        #Tip of Index and middle finger
        x1,y1=lmList[8][1:]
        x2,y2=lmList[12][1:]


        #3.Check which finger are up
        fingers = detector.fingersUp()
        # print(fingers)
    #4.If selection mode -Two fingers are up
        if fingers[1] and fingers[2]:
            xp, yp = 0, 0
            print("Selection Mode")
            if(y1<110):
                if 325<x1<450:
                    header = overlayList[0]
                    drawColor = (255, 0, 255)
                elif 530<x1<670:
                    header = overlayList[1]
                    drawColor = (255, 0, 0)
                elif 710<x1<840:
                    header = overlayList[2]
                    drawColor = (0, 255, 0)
                elif 860<x1<1030:
                    header = overlayList[3]
                    drawColor = (0, 0, 0)
            cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)


    #5.Drawing Mode -Index Finger is up
        if fingers[1] and fingers[2]==False:
            cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
            print("Drawing Mode")
            if(xp==0 and yp==0):
                xp,yp=x1,y1
            if drawColor==(0,0,0):
                cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)
            else:
                cv2.line(img,(xp,yp),(x1,y1),drawColor,brushThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)
                xp,yp=x1,y1
    # imgGray = cv2.cvtColor(imgCanvas,cv2.COLOR_BGR2GRAY)
    # _,imgInv = cv2.threshold(imgGray,50,255,cv2.THRESH_BINARY_INV)
    # imgInv = cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
    # img=cv2.bitwise_and(img,imgInv)
    # img=cv2.bitwise_or(img,imgCanvas)
    #setting the header image
    img[0:110,30:1230]=header
    # imgStack = stackImages(0.8, [[img],[imgCanvas]])

    # cv2.imshow("Image",imgStack)
    cv2.imshow("Image",img)
    cv2.imshow("Canvas",imgCanvas)
    cv2.waitKey(1)