from cv2 import COLOR_BGR2GRAY, THRESH_BINARY_INV, VideoCapture, bitwise_or, cvtColor, flip, threshold, waitKey, imshow, imread, IMREAD_UNCHANGED, resize, INTER_AREA, line, circle, FILLED
from cv2 import cvtColor, bitwise_or, bitwise_and, COLOR_GRAY2BGR, THRESH_BINARY_INV, COLOR_GRAY2BGR, threshold, rectangle
from cvzone import HandTrackingModule, overlayPNG
import numpy as np

cap = VideoCapture(0)
detector = HandTrackingModule.HandDetector(maxHands=1, detectionCon=0.5)

sqr_img = imread("img/sqr (2).png", IMREAD_UNCHANGED)

sqr_img = resize(sqr_img, (270, 230), interpolation=INTER_AREA)

sqrW, sqrH = 318, 318
pox, poy = int(sqrW / 2), 60 # position of your image/sqr_img
b, g, r = 27, 74, 114


prevX, prevY = 0, 0
finishX, finishY = 0, 0

isStarted = False
gameOver = False

smoothX, smoothY = 0, 0

# Draw Canvas to test
canvas = np.zeros((480, 640, 3), np.uint8)

smoothing = 3

corners = [0, 0, 0, 0]

# mistakes
mistakes = 0


while True:
    _, img = cap.read()
    img = flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)


    h, w, _= sqr_img.shape
    
    # White Background
    # img = rectangle(img, (0, 0), (640, 480), (255, 255, 255), FILLED)

    img = overlayPNG(img, sqr_img, [pox, poy])

    if hands:
        lmList = hands[0]['lmList']

        cursor = lmList[8]
        smoothX = int(prevX + (cursor[0] - prevX) / smoothing)
        smoothY = int(prevY + (cursor[1] - prevY) / smoothing)
        
        if detector.fingersUp(hands[0]) == [0, 1, 0, 0, 0]:
            # check if inside image
            if pox < smoothX < pox + w and poy < smoothY < poy + h:
                cb, cg, cr = img[smoothY, smoothX, 0], img[smoothY, smoothX, 1], img[smoothY, smoothX, 2]
                if cb == b and cg == g and cr == r: # check if insied the cutter line
                    isStarted = True

                    if prevX != cursor[0] and prevY != cursor[1]:
                        if prevX == 0 and prevY == 0:
                            prevX, prevY = cursor[0], cursor[1]
                        if finishX == 0 and finishY == 0:
                            finishX, finishY = cursor[0], cursor[1]

                        
                        line(canvas, (prevX, prevY), (smoothX, smoothY), (255, 255, 0), thickness=9) # Draw Line if he is inside

                        if (smoothX-10 <= finishX <= smoothX+10 and smoothY-10 <= finishY <= smoothY+10):
                            if corners == [1, 1, 1, 1]:
                                print("Finished!!!") # WIN


                elif cb == 26 and cg == g and cr == r:
                    corners[0] = 1
                    line(canvas, (prevX, prevY), (smoothX, smoothY),
                         (255, 255, 0), thickness=9)

                elif cb == 28 and cg == g and cr == r:
                    corners[1] = 1
                    line(canvas, (prevX, prevY), (smoothX, smoothY), (255, 255, 0), thickness=9)

                elif cb == 29 and cg == g and cr == r:
                    corners[2] = 1
                    line(canvas, (prevX, prevY), (smoothX, smoothY), (255, 255, 0), thickness=9)

                elif cb == 30 and cg == g and cr == r:
                    corners[3] = 1
                    line(canvas, (prevX, prevY), (smoothX, smoothY), (255, 255, 0), thickness=9)



                elif isStarted: # LOSE
                    mistakes += 1
                    if mistakes == 10:
                        corners = [0, 0, 0, 0]
                        canvas = np.zeros((480, 640, 3), np.uint8) # remove green lines
                        finishX, finishY = 0, 0
                        prevX, prevY = 0, 0
                        c = 0
                        mistakes = 0
                        gameOver = True
                circle(img, (smoothX, smoothY), 5, (255, 255, 0), FILLED)
            #circle(img, (smoothX, smoothY), 3, (0, 0, 0), FILLED)

        else:
            prevX, prevY = 0, 0
            circle(img, (smoothX, smoothY), 5, (255, 255, 0), FILLED)

      

        prevX, prevY = smoothX, smoothY

        



    imgGray = cvtColor(canvas, COLOR_BGR2GRAY)
    _, imgInv = threshold(imgGray, 50, 255, THRESH_BINARY_INV)
    imgInv = cvtColor(imgInv, COLOR_GRAY2BGR)
    img = bitwise_and(img, imgInv)
    img = bitwise_or(img, canvas)

    imshow('Image', img)
    #imshow('Canvas', canvas)
    waitKey(1)
