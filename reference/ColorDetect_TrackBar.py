import cv2
import numpy as np

frameWidth = 320
frameHeight = 240

cap = cv2.VideoCapture('v2.mp4')
cap.set(3, frameWidth)
cap.set(4, frameHeight)

print("Program started")

#Callback function when the track bar is sliding
def empty(a):
    pass

# Track Bar to calibrate the parameters
cv2.namedWindow("HSV")
cv2.resizeWindow("HSV", 640, 320)
cv2.createTrackbar("Hue Min", "HSV", 0, 179, empty)
cv2.createTrackbar("Hue Max", "HSV", 179, 179, empty)
cv2.createTrackbar("Sat Min", "HSV", 0, 255, empty)
cv2.createTrackbar("Sat Max", "HSV", 255, 255, empty)
cv2.createTrackbar("Value Min", "HSV", 0, 255, empty)
cv2.createTrackbar("Value Max", "HSV", 255, 255, empty)

### For video only ###
frameCounter = 1
######################

while True:

    ### For video only ###
    frameCounter += 1
    print(frameCounter)
    if cap.get(cv2.CAP_PROP_FRAME_COUNT) == frameCounter:
        print("In")
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        frameCounter = 1
    ######################

    _, img = cap.read()
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Get the values from
    h_min = cv2.getTrackbarPos("Hue Min", "HSV")
    h_max = cv2.getTrackbarPos("Hue Max", "HSV")
    s_min = cv2.getTrackbarPos("Sat Min", "HSV")
    s_max = cv2.getTrackbarPos("Sat Max", "HSV")
    v_min = cv2.getTrackbarPos("Value Min", "HSV")
    v_max = cv2.getTrackbarPos("Value Max", "HSV")

    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    mask = cv2.inRange(imgHSV, lower, upper)

    result = cv2.bitwise_and(img, img, mask = mask)

    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)

    #cv2.imshow('Original', img)
    #cv2.imshow('HSV Color Space', imgHSV)
    #cv2.imshow('Mask', mask)
    cv2.imshow('Result', result)

    #hstack = np.hstack([img, mask, result])
    #cv2.imshow('HStack', hstack)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
