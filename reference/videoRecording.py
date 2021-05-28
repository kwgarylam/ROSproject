import cv2
import numpy as np
import pyautogui
import time

print(pyautogui.size())

# define the codec
fourcc = cv2.VideoWriter_fourcc(*"XVID")

# create the video write object
# display screen resolution, get it from your OS settings
SCREEN_SIZE = (100, 100)

out = cv2.VideoWriter("output.avi", fourcc, 20.0, (SCREEN_SIZE))

time.sleep(2)

cv2.namedWindow("Recording", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Recording", 480, 270)

while True:
    # make a screenshot
    img = pyautogui.screenshot(region=(0, 0, SCREEN_SIZE[0], SCREEN_SIZE[1]))
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

