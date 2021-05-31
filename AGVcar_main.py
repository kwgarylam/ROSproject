import numpy as np
import cv2

# Capturing video through webcam
webcam = cv2.VideoCapture('ColorDetection.mp4')

### For video only ###
frameCounter = 1
######################

# Image size

frameWidth = 320
frameHeight = 240

# ROI for traffic sign
roi_x = 0
roi_y = 0
roi_w = round(frameWidth/2)
roi_h = round(frameHeight/2)


# Start a while loop
while (1):
    ### For video only ###
    frameCounter += 1
    if webcam.get(cv2.CAP_PROP_FRAME_COUNT) == frameCounter:
        webcam.set(cv2.CAP_PROP_POS_FRAMES, 0)
        frameCounter = 1
    ######################

    # Reading the video from the
    # webcam in image frames
    _, imageFrame = webcam.read()
    imageFrame = cv2.resize(imageFrame, (frameWidth, frameHeight))

    # Crop the ROI for Sign Color Detection
    # The top right conner is cropped
    imageFrame = imageFrame[roi_y : roi_y+roi_h, roi_x+roi_w:frameWidth]

    # Convert the imageFrame in BGR(RGB color space) to
    # HSV(hue-saturation-value) color space
    hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)

    # Set range for red color and define mask
    red_lower = np.array([0, 0, 165], np.uint8)
    red_upper = np.array([54, 255, 255], np.uint8)
    red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)

    # Set range for green color and define mask
    green_lower = np.array([54, 39, 82], np.uint8)
    green_upper = np.array([64, 255, 215], np.uint8)
    green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)


    # Morphological Transform, Dilation for each color and bitwise_and operator
    # between imageFrame and mask determines to detect only that particular color
    kernal = np.ones((5, 5), "uint8")

    # For red color
    red_mask = cv2.dilate(red_mask, kernal)
    res_red = cv2.bitwise_and(imageFrame, imageFrame, mask=red_mask)
    # For green color
    green_mask = cv2.dilate(green_mask, kernal)
    res_green = cv2.bitwise_and(imageFrame, imageFrame, mask=green_mask)

    # Creating contour to track red color
    contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        area = cv2.contourArea(contour)
        if ((area > 50) and (area < 150)):
            x, y, w, h = cv2.boundingRect(contour)
            imageFrame = cv2.rectangle(imageFrame, (x, y), (x + w, y + h), (0, 0, 255), 2)

            cv2.putText(imageFrame, "Red Colour", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))

    # Creating contour to track green color
    contours, hierarchy = cv2.findContours(green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # Creating contour to track Green color
    for contour in contours:
        area = cv2.contourArea(contour)
        if ((area > 50) and (area < 150)):
            x, y, w, h = cv2.boundingRect(contour)
            imageFrame = cv2.rectangle(imageFrame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(imageFrame, "Green Colour", (x - 100, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))

    # Program Termination
    cv2.imshow("Multiple Color Detection in Real-TIme", imageFrame)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        webcam.release()
        cv2.destroyAllWindows()
        break
