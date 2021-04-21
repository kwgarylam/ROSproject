import numpy as np
import cv2

# Read the image file
img_rgb = cv2.imread('myimg.jpg')

# Gray scale
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

# Matching temple
template = cv2.imread('template3.JPG',0)

# Read the size of the template
w, h = template.shape[::-1]

res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)

threshold = 0.6

# Find the location that matched
loc = np.where(res >= threshold)

for pt in zip(*loc[::-1]):
    cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,255,255), 2)


cv2.imshow('Result', img_rgb)
cv2.waitKey(0)
cv2.destroyWindow()

