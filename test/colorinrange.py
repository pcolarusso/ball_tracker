import cv2 as cv
import numpy as np

imagename = 'ballimagelowres.jpg'

img = cv.imread(imagename,cv.IMREAD_COLOR)
#Convert to hsv colorspace because that works better
hsvimg = cv.cvtColor(img, cv.COLOR_BGR2HSV)
#define thresholds
#True value for white is (0-255,0-255, 255) only Value matters for white
white_lower = np.array([0,0,127])
white_upper = np.array([255,255,255])

# Threshold the HSV image to get only white colors
mask = cv.inRange(hsvimg, white_lower, white_upper)

cv.imshow('original', img)
cv.imshow('mask',mask)
cv.imshow('hsvimg',hsvimg)

k = cv.waitKey(0)
cv.destroyAllWindows()