import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

#this module shows the difference between different types of threshold filtering for an image

imagename='ballimage.jpg' #Replace ballimage.jpg with the name of your image

img = cv.imread(imagename,0)
ret,thresh1 = cv.threshold(img,200,255,cv.THRESH_BINARY)
ret,thresh2 = cv.threshold(img,200,255,cv.THRESH_BINARY_INV)
ret,thresh3 = cv.threshold(img,200,255,cv.THRESH_TRUNC)
ret,thresh4 = cv.threshold(img,200,255,cv.THRESH_TOZERO)
ret,thresh5 = cv.threshold(img,200,255,cv.THRESH_TOZERO_INV)
thresh6 = cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_MEAN_C,\
            cv.THRESH_BINARY,11,2)
thresh7 = cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv.THRESH_BINARY,11,2)
ret,thresh8 = cv.threshold(img,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
titles = ['Original Image','BINARY','BINARY_INV','TRUNC','TOZERO','TOZERO_INV','Adaptive Mean', 'Adaptive Gaussian', 'Otsu']
images = [img, thresh1, thresh2, thresh3, thresh4, thresh5, thresh6, thresh7, thresh8]
for i in range(9):
    plt.subplot(3,3,i+1),plt.imshow(images[i],'gray')
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])
plt.show()