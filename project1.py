import cv2
import numpy as np
frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10,150)
myColors=[[4,181,48,150,255,255],
          [152,59,33,179,178,255]]
myColorValues=[
    [51,153,255], #BGR
    [127,0,255]
]
myPoints=[]
def findcolor(img,myColors,myColorValues):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count=0
    newPoints=[]
    for color in myColors:
        lower = np.array(color[:3])
        upper = np.array(color[3:])
        mask = cv2.inRange(imgHSV, lower, upper)
        #cv2.imshow("img",mask)
        x,y=getContours(mask)
        cv2.circle(imgResult,(x,y),10,myColorValues[count],cv2.FILLED)
        if x!=0 and y!=0:
            newPoints.append([x,y,count])
        count+=1
    return newPoints

def getContours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x,y,w,h=0,0,0,0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        #print(area)
        if area>500:
            #cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 3)#(copy of image , cnt, -1 for all points
            peri = cv2.arcLength(cnt, True) # give perimeter
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True) # tells corner point
            x, y, w, h = cv2.boundingRect(approx) #create bounding box around figure
    return x+w//2,y
def drawOnCanvas(myPoints,myColorValues):
    for point in myPoints:
        cv2.circle(imgResult, (point[0], point[1]), 10,myColorValues[point[2]] , cv2.FILLED)
while True:
    success, img = cap.read()
    imgResult = img.copy()
    newPoints=findcolor(img,myColors,myColorValues)
    if len(newPoints)!=0:
        for newP in newPoints:
            myPoints.append(newP)
    if len(myPoints)!=0:
        drawOnCanvas(myPoints,myColorValues)


    cv2.imshow("Result", imgResult)
    if cv2.waitKey(1) == ord('q'):
        break