import cv2
import numpy as np
import pyautogui
import time

# Check for the Screen size
#print(pyautogui.size())

# define the codec
fourcc = cv2.VideoWriter_fourcc(*"XVID")

# create the video write object
# Set the width and height of the capturing region
###########################################################
cap_Topleft_x = 65
cap_Topleft_y = 110
SCREEN_SIZE = (840, 380)
###########################################################

out = cv2.VideoWriter("output.avi", fourcc, 20.0, (SCREEN_SIZE))

cv2.namedWindow("Recording", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Recording", round(SCREEN_SIZE[0]/4), round(SCREEN_SIZE[1]/4))
cv2.moveWindow("Recording", round(cap_Topleft_x+SCREEN_SIZE[0]+100),0)
#frame = np.zeros(SCREEN_SIZE)
#cv2.imshow("Recording", frame)
#cv2.waitKey(1)
time.sleep(3)

print("Start capture...")
while True:
    # make a screenshot
    # -- top, left, width, height
    img = pyautogui.screenshot(region=(cap_Topleft_x, cap_Topleft_y, SCREEN_SIZE[0], SCREEN_SIZE[1]))
    # convert these pixels to a proper numpy array to work with OpenCV
    frame = np.array(img)
    # convert colors from BGR to RGB
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # write the frame
    out.write(frame)
    # show the frame
    cv2.imshow("Recording", frame)
    # if the user clicks q, it exits
    if cv2.waitKey(1) == ord("q"):
        break

# make sure everything is closed when exited
cv2.destroyAllWindows()
out.release()

