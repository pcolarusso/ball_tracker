import cv2 as cv
import numpy as np

imagename = 'ballimage.jpg'

#read image
img = cv.imread(imagename,cv.IMREAD_COLOR)

#Copy of image to put into result
result = img

#Convert to hsv colorspace because that works better
hsvimg = cv.cvtColor(img, cv.COLOR_BGR2HSV)

#Define thresholds
#True value for white in HSV is (0-255,0-255, 255) only Value matters for white
white_lower = np.array([0,0,127])
white_upper = np.array([180,255,255])

#Threshold the HSV image to get only white colors
#Image is a mask of only colors in the threshold values
mask = cv.inRange(hsvimg, white_lower, white_upper)

#Create color image for mask to draw circles on
cimg = cv.cvtColor(mask,cv.COLOR_GRAY2BGR)

#Find circles in the masked image
circles = cv.HoughCircles(mask,cv.HOUGH_GRADIENT,1,20,
                            param1=50,param2=30,minRadius=0,maxRadius=0)
if circles is None:
    #This displays text if no ball is detected
    text = 'no ball detected'
    textsize = cv.getTextSize(text, cv.FONT_HERSHEY_SIMPLEX, 2, 2)
    rows, columns, channels = img.shape
    
    #Finds origin to center text
    textorigin = ((columns//2)-(textsize[0][0]//2), textsize[0][1]+10)

    #Draw a Rectangle to help text stand out
    bottomleftvertex = (textorigin[0]-5, textorigin[1]+5)
    toprightvertex = (textorigin[0]+textsize[0][0]+5, 5)
    cv.rectangle(result, bottomleftvertex, toprightvertex, [255,255,255], cv.FILLED)
    
    #Draw text
    cv.putText(result, text, textorigin, cv.FONT_HERSHEY_SIMPLEX, 2, [0,0,0], 2, cv.FILLED, False)
    print('No ball detected')
    
else: #Ball is detected
    #Round number to whole numbers
    circles = np.uint16(np.around(circles))
    print(circles)
    
    #Draw circles on colored masked image
    for i in circles[0,:]:
        # draw the outer circle
        cv.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
        # draw the center of the circle
        cv.circle(cimg,(i[0],i[1]),2,(0,0,255),3)
    
    #Draw circle around the image
    #The "best" circle is the first one in the array so that one is used
    cv.circle(result, (circles[0][0][0],circles[0][0][1]),circles[0][0][2],(0,255,0),2)

#Show images
cv.imshow('Original', img)
cv.imshow('Mask',mask)
cv.imshow('Circles', cimg)
cv.imshow('Result', result)

k = cv.waitKey(0)
cv.destroyAllWindows()
