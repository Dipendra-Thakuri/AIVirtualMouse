import cv2
import numpy as np
import time
import HandTracking as ht
import pyautogui as pag

# Variables Declaration
pTime = 0               # Used to calculate frame rate
width = 640             # Width of Camera
height = 480            # Height of Camera
frameR = 100            # Frame Rate
smoothening = 8         # Smoothening Factor
prev_x, prev_y = 0, 0   # Previous coordinates
curr_x, curr_y = 0, 0   # Current coordinates

cap = cv2.VideoCapture(0)   # Getting video feed from the webcam
cap.set(3, width)           # Adjusting size
cap.set(4, height)

detector = ht.handDetector(maxHands=1)                  # Detecting one hand at max
screen_width, screen_height = 2120, 1280     # Getting the screen size
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img)                       # Finding the hand
    lmlist, bbox = detector.findPosition(img)           # Getting position of hand

    if len(lmlist)!=0:
        x1, y1 = lmlist[8][1:]         # index
        x2, y2 = lmlist[12][1:]        # middle
        x4, y4 = lmlist[16][1:]        # ring
        x5, y5 = lmlist[20][1:]        # little

        fingers = detector.fingersUp()      # Checking if fingers are upwards
        # Creating boundary box
        if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0:      # If fore finger is up and middle finger is down
            x3 = np.interp(x2, (frameR,width-frameR), (0,screen_width))
            y3 = np.interp(y2, (frameR, height-frameR), (0, screen_height))

            curr_x = prev_x + (x3 - prev_x)/smoothening
            curr_y = prev_y + (y3 - prev_y) / smoothening

            pag.moveTo(curr_x, curr_y)    # Moving the cursor
            cv2.circle(img, (x2, y2), 7, (255, 0, 255), cv2.FILLED)
            prev_x, prev_y = curr_x, curr_y

        if fingers[1] == 0 and fingers[2] == 1:     # If fore finger & middle finger both are up
            pag.click()    # Perform Click
            pag.sleep(1)

        if fingers[1] == 1 and fingers[2] == 0:
            pag.click(button='right')
            pag.sleep(1)

        if fingers[1] == 1 and fingers[2] == 1:
            length, img, lineInfo = detector.findDistance(8, 12, img)

            if length < 15:
                pag.doubleClick()
                pag.sleep(1)

        if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 0:
            pag.scroll(100)
            pag.sleep(0.5)

        if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 1:
            pag.scroll(-100)
            pag.sleep(0.5)

        if fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
            pag.mouseDown()
            pag.sleep(0.5)
            x3 = np.interp(x1, (frameR, width - frameR), (0, screen_width))
            y3 = np.interp(y1, (frameR, height - frameR), (0, screen_height))

            curr_x = prev_x + (x3 - prev_x) / smoothening
            curr_y = prev_y + (y3 - prev_y) / smoothening

            pag.moveTo(curr_x, curr_y)  # Moving the cursor
            prev_x, prev_y = curr_x, curr_y

        if fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 1:
            pag.mouseUp()
            pag.sleep(0.5)


    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)