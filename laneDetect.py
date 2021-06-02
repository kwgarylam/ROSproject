import cv2
import numpy as np
import myUtlis

#####################################
frameWidth = 320
frameHeight = 240
fps = 20
#####################################

### For video only ###
frameCounter = 1
######################

def getLaneCurve(img):

    imgCopy = img.copy()

    ### STEP 1
    imgThres = myUtlis.thresholding(img)

    ### STEP 2
    h, w, c = img.shape
    points = myUtlis.valTrackbars()
    imgWarp = myUtlis.warpImg(imgThres, points, w, h)
    imgWarpPoints = myUtlis.drawPoints(imgCopy, points)

    # Debug
    cv2.imshow('Thres', imgThres)
    cv2.imshow('Warp', imgWarp)
    cv2.imshow('Warp Points', imgWarpPoints)

    return None

if __name__ == '__main__':
    cap = cv2.VideoCapture('lane1.mp4')

    # Initialization    ###############################
    initialTrackBarVals = [50, 60, 0, 240]
    myUtlis.initializeTrackbars(initialTrackBarVals, frameWidth, frameHeight)
    ###################################################

    while True:
        ### For video only ###
        frameCounter += 1
        if cap.get(cv2.CAP_PROP_FRAME_COUNT) == frameCounter:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            frameCounter = 1
        ######################

        success, img = cap.read()

        img = cv2.resize(img, (frameWidth, frameHeight))
        getLaneCurve(img)

        cv2.imshow('Vid', img)
        #cv2.waitKey(fps)
        cv2.waitKey(1)
