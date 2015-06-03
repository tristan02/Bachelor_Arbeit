import cv2
from cv2 import cv
import ImageTk, Image
import numpy as np
 
template_name = "tmpp.jpg"
image_name = "img.jpg"
 
# Load
needle = cv2.imread(template_name)   
    
def match(num):     
    
    path = 'ima/img (' + str(num+1) + ').jpg'
    img = cv2.imread(path)
    # Convert to gray:
    needle_g = cv2.cvtColor(needle, cv2.CV_32FC1)
    img_g = cv2.cvtColor(img, cv2.CV_32FC1)
    # Attempt match
    d = cv2.matchTemplate(needle_g, img_g, cv2.cv.CV_TM_SQDIFF_NORMED)
    # we want the minimum squared difference
    mn,_,mnLoc,_ = cv2.minMaxLoc(d)
     
    # Print it, for comparison
    #print mn
     
    # Draw the rectangle
    MPx,MPy = mnLoc
     
    trows,tcols = needle_g.shape[:2]
     
    # Normed methods give better results, ie matchvalue = [1,3,5], others sometimes shows errors
    cv2.rectangle(img, (MPx,MPy),(MPx+tcols,MPy+trows),(0,0,255),2)
 
    cv2.imshow('output',img)
    cv2.waitKey()

'''for n in range(100):
    match(n)'''
match(1)
cv2.waitKey(0)
import sys
sys.exit(0)