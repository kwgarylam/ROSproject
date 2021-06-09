import cv2
import numpy as np
import myUtlis

#####################################
frameWidth = 320
frameHeight = 240
fps = 20
curveList = []
avgValLength = 10
#####################################

### For video only ###
#frameCounter = 1
######################

#display = 0 (not display); display = 1 (display result); display = 2 (display everythings)
def getLaneCurve(img, display=2):

    imgCopy = img.copy()
    imgResult = img.copy()

    ### STEP 1
    imgThres = myUtlis.thresholding(img)

    ### STEP 2
    hT, wT, c = img.shape
    points = myUtlis.valTrackbars()
    imgWarp = myUtlis.warpImg(imgThres, points, wT, hT)
    imgWarpPoints = myUtlis.drawPoints(imgCopy, points)

    ### STEP 3

    # For a point that far away from the baseline, more black pixels are remove in the histogram
    # The higher the minPer, the more likely the lane located
    adveragePoint, imgHist = myUtlis.getHistogram(imgWarp, display=True, minPer=0.8, percentRegion=1,histColor=(0,255,0))
    #imgHistAP = imgHist

    # For a point that close to the baseline, the region in the bottom part is used.
    # More pixels are take into account, hence, the minPer should be small.
    baseline, imgHist = myUtlis.getHistogram(imgWarp, display=True, minPer=0.2, percentRegion=0.2)
    #imgHistBL = imgHist

    curveRaw = adveragePoint - baseline
    #print(curveRaw)

    ### STEP 4
    # Append the curve data to a list, smoothing the curve value to remove sudden changes
    curveList.append(curveRaw)

    # Remove the oldest data if the list is longer than the average value length
    if len(curveList) > avgValLength:
        curveList.pop(0)
    curve = int(sum(curveList)/len(curveList))

    ### STEP 5
    # Display the results based on the options
    if display != 0:
        imgInvWarp = myUtlis.warpImg(imgWarp, points, wT, hT, inv=True)
        imgInvWarp = cv2.cvtColor(imgInvWarp, cv2.COLOR_GRAY2BGR)
        imgInvWarp[0:hT // 3, 0:wT] = 0, 0, 0
        imgLaneColor = np.zeros_like(img)
        imgLaneColor[:] = 0, 255, 0
        imgLaneColor = cv2.bitwise_and(imgInvWarp, imgLaneColor)
        # Blend the imgResult and imgLaneColor, gamma is 0 (Intensity is remained)
        imgResult = cv2.addWeighted(imgResult, 1, imgLaneColor, 1, 0)
        midY = 450
        cv2.putText(imgResult, str(curve), (wT // 2 - 80, 85), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 3)
        cv2.line(imgResult, (wT // 2, midY), (wT // 2 + (curve * 3), midY), (255, 0, 255), 5)
        cv2.line(imgResult, ((wT // 2 + (curve * 3)), midY - 25), (wT // 2 + (curve * 3), midY + 25), (0, 255, 0), 5)
        for x in range(-30, 30):
            w = wT // 20
            cv2.line(imgResult, (w * x + int(curve // 50), midY - 10),
                     (w * x + int(curve // 50), midY + 10), (0, 0, 255), 2)

    if display == 2:
        imgStacked = myUtlis.stackImages(0.7, ([img, imgWarpPoints, imgWarp],
                                             [imgHist, imgLaneColor, imgResult]))
        cv2.imshow('ImageStack', imgStacked)
    elif display == 1:
        cv2.imshow('Result', imgResult)


    # Debug
    #cv2.imshow('Thres', imgThres)
    #cv2.imshow('Warp', imgWarp)
    #cv2.imshow('Warp Points', imgWarpPoints)
    #cv2.imshow('Histogram1', imgHist1)
    #cv2.imshow('Histogram2', imgHist2)

    #### NORMALIZATION
    curve = curve / 100
    if curve > 1: curve == 1
    if curve < -1: curve == -1

    return curve

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
        curve = getLaneCurve(img, display=2)
        print(curve)

        #cv2.imshow('Vid', img)
        cv2.waitKey(fps)
        #cv2.waitKey(1)
