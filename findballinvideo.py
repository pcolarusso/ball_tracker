import cv2 as cv
import numpy as np

#Needed for createTrackbar function
def doNothing(x):
    pass

#Opens Video Camera
cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

#Add trackbars to change settings to adjust to different lighting conditions and ball sizes
cv.namedWindow('Adjustments')
cv.createTrackbar('White Lower Threshold','Adjustments',0,255,doNothing)
cv.createTrackbar('White Upper Threshold','Adjustments',0,255,doNothing)
cv.createTrackbar('Min Radius','Adjustments',0,255,doNothing)
cv.createTrackbar('Max Radius','Adjustments',0,255,doNothing)

while True:
    isframeread, frame = cap.read()
    
    #If frame is read correctly ret is True
    if not isframeread:
        print("Can't receive frame. Exiting ...")
        break
    
    #Grab Values from trackbars
    low_thresh = cv.getTrackbarPos('White Lower Threshold','Adjustments')
    high_thresh = cv.getTrackbarPos('White Upper Threshold','Adjustments')
    minradius = cv.getTrackbarPos('Min Radius','Adjustments')
    maxradius = cv.getTrackbarPos('Max Radius','Adjustments')
    
    #Convert to hsv colorspace because that works better
    hsvimg = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    
    #Define thresholds
    #True value for white in HSV is (0-180,0-255, 255) only Value matters for white
    white_lower = np.array([0,0,low_thresh])
    white_upper = np.array([180,255,high_thresh])
    
    #Threshold the HSV image to get only white colors
    #Image is a mask of only colors in the threshold values
    mask = cv.inRange(hsvimg, white_lower, white_upper)
    
    #Find circles in the masked image
    circles = cv.HoughCircles(mask,cv.HOUGH_GRADIENT,1,20,
                                param1=50,param2=30,minRadius=minradius,maxRadius=maxradius)
    
    if circles is None:
        #This displays text if no ball is detected
        text = 'no ball detected'
        textsize = cv.getTextSize(text, cv.FONT_HERSHEY_SIMPLEX, 2, 2)
        rows, columns, channels = frame.shape
        
        #Finds origin to center text
        textorigin = ((columns//2)-(textsize[0][0]//2), textsize[0][1]+10)
    
        #Draw a Rectangle to help text stand out
        bottomleftvertex = (textorigin[0]-5, textorigin[1]+5)
        toprightvertex = (textorigin[0]+textsize[0][0]+5, 5)
        cv.rectangle(frame, bottomleftvertex, toprightvertex, [255,255,255], cv.FILLED)
        
        #Draw text
        cv.putText(frame, text, textorigin, cv.FONT_HERSHEY_SIMPLEX, 2, [0,0,0], 2, cv.FILLED, False)
        
    else: #Ball is detected
        #Round number to whole numbers
        circles = np.uint16(np.around(circles))
        print(circles)
        
        #Draw circle around the image
        #The "best" circle is the first one in the array so that one is used
        cv.circle(frame, (circles[0][0][0],circles[0][0][1]),circles[0][0][2],(0,255,0),2)
    
    #Show image
    cv.imshow('Result', frame)
    
    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows() 
