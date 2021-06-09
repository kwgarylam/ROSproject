import cv2
import numpy as np

# Function to extract the line by the HSV color detection
def thresholding(img):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lowerWhite = np.array([47, 0, 0])
    upperWhite = np.array([140, 200, 200])
    maskWhite = cv2.inRange(imgHSV, lowerWhite, upperWhite)
    return maskWhite

# Function of affine transform
def warpImg(img, points, w, h, inv=False):
    pts1 = np.float32(points)
    pts2 = np.float32([[0,0], [w,0], [0,h], [w,h]])
    if inv:
        # Invert the image from transformation view to the original image
        matrix = cv2.getPerspectiveTransform(pts2, pts1)
    else:
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgWarp = cv2.warpPerspective(img, matrix, (w,h))
    return imgWarp

# Track Bar to calibrate the parameters
def empty(a):
    pass

def initializeTrackbars(initialTrackbarVals, wT=320, hT=240):
    cv2.namedWindow("Trackbars")
    cv2.resizeWindow("Trackbars", 360, 240)
    cv2.createTrackbar("Width Top", "Trackbars", initialTrackbarVals[0], wT//2, empty)
    cv2.createTrackbar("Height Top", "Trackbars", initialTrackbarVals[1], hT, empty)
    cv2.createTrackbar("Width Bottom", "Trackbars", initialTrackbarVals[2], wT//2, empty)
    cv2.createTrackbar("Height Bottom", "Trackbars", initialTrackbarVals[3], hT, empty)

# Get the values from the track bars
def valTrackbars(wT=320, hT=240):
    widthTop = cv2.getTrackbarPos("Width Top", "Trackbars")
    heightTop = cv2.getTrackbarPos("Height Top", "Trackbars")
    widthBottom = cv2.getTrackbarPos("Width Bottom", "Trackbars")
    heightBottom = cv2.getTrackbarPos("Height Bottom", "Trackbars")
    points = np.float32([(widthTop, heightTop), (wT - widthTop, heightTop),
                         (widthBottom, heightBottom), (wT - widthBottom, heightBottom)])

    return points

# Draw the points for calibrating the affine transform
def drawPoints(img, points):
    for x in range(4):
        cv2.circle(img, (int(points[x][0]), int(points[x][1])), 15, (0,0,255), cv2.FILLED)
    return img

# Calculate the histogram lane prediction
# interestedRegion range from 1(100%) to 0.1(10%)
def getHistogram(img, minPer=0.1, display=False, percentRegion=1, histColor=(255,0,255)):

    # Take all the pixels inside the input image for histogram
    if percentRegion == 1:
        histValues = np.sum(img, axis=0)
    else:
        # Image slicing: image[start_x:end_x, start_y:end_y]
        # % of the lane is used for histogram calculation
        percentRegion = 1 - percentRegion
        histValues = np.sum(img[round(img.shape[0]*percentRegion):,:], axis=0)

    #print(histValues)
    maxValue = np.max(histValues)
    minValue = minPer*maxValue
    #print(np.shape(histValues))

    # The minimum pixel is 10% of the maximum value
    # Ignore the column of histogram that is too small
    # The remaining array is the potential lane which has high pixel value
    indexArray = np.where(histValues >= minValue)
    #print(np.shape(indexArray))
    #print(indexArray)
    #print(type(indexArray))

    # Calculate the average of the pixel level in the lane
    basePoint = int(np.average(indexArray))
    #print(basePoint)
    #print(np.shape(basePoint))
    #print(type(basePoint))

    if display:
        imgHist = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
        for x, intensity in enumerate (histValues):
            cv2.line(imgHist, (x, img.shape[0]), (x, img.shape[0]-(intensity//255)), histColor, 1)
            cv2.circle(imgHist, (basePoint, img.shape[0]), 20, (0,255,255), cv2.FILLED)
        return basePoint, imgHist
    return basePoint

##################################################################
# External functions
##################################################################
def displayResult():
    pass

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
