#from MotorModule import Motor
import KeyPressModule as kp
import cv2
import colorDetectionModule as color
import laneDetectionModule as lane
import myUtlis
######################################
#motor = Motor(2, 3, 4, 17, 22, 27)
######################################

cap = cv2.VideoCapture(0)
# Parameters        ###############################
initialTrackBarVals = [50, 60, 0, 240]
frameWidth = 480
frameHeight = 340
curveList = []
avgValLength = 10
###################################################
# Initialization    ###############################
myUtlis.initializeTrackbars(initialTrackBarVals, frameWidth, frameHeight)
kp.init()
waiting = True
trafficSignColor = ""

def getImg(display = False, size = [480,340]):

    ret, img = cap.read()
    img = cv2.resize(img, (size[0], size[1]))

    if display:
        cv2.imshow('frame', img)
    return img

######################## STEP ONE #######################
################ Check the road condition ###############
# Stage 1:
# Check the status of traffic light
# If red light: stay; green light: start
# Input: VideoFrame
# Output: float speed
def getTrafficLight(img, display=True):

    global waiting
    global trafficSignColor

    # Stage 1.1
    # Color Detection Method ###########
    # Check the Color in the Region of Interest (ROI)
    # Input: VideoFrame
    # Output: String trafficColor, "Red" or "Green"
    trafficImageFrame, trafficSignColor = color.getTrafficColor(img)

    if display:
        cv2.imshow('Traffic Light', trafficImageFrame)

    ####################################

    # Stage 1.2
    # If the traffic light return is green, start running the robot
    #trafficSignColor = "green"

    if trafficSignColor == "green":
        waiting = False

    #print(trafficSignColor)

    return trafficImageFrame, trafficSignColor
# After stage 1, the robot start to move.
def run(img):
###############################################
### The main program of the project         ###
###############################################
    print("Running Program")
    # Stage 2:
    # Lane detection method
    # Calculate the difference of the basepoint and the mean point.
    # Return a value for turning
    # Input: Video Frame
    # Output: Lane Curve
    curve = lane.getLaneCurve(img, display=2)
    print(curve)


    # Stage 3:
    # Road sign detection method
    # Detection a hexagon which is a "STOP" sign
    # Input: Video Frame
    # Output: float speed


######################## STEP TWO #######################
###################### Run the Robot ####################

    #motor.move(speed, laneCurve, 0.1)




##############################################
if __name__ == '__main__':
    while True:

        myframe = getImg(display=True)

        if waiting:
            getTrafficLight(myframe, display=True)
        else:
            run(myframe)


        # Press 'q' to quite the program
        if cv2.waitKey(1) == ord('q'):
            break

    # Release program resources
cap.release()
cv2.destroyAllWindows()
