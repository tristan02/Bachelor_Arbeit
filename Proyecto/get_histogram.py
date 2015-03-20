'''
Created on 4/2/2015

@author: Psilocibino
'''
import cv2
import numpy as np

def get_hist(img,msk):
    h = np.zeros((300,256,3))
    b,g,r = cv2.split(img)
    bins = np.arange(256).reshape(256,1)
    color = [(255,0,0),(0,255,0),(0,0,255)]
    
    for item,col in zip([b,g,r],color):
        hist_item = cv2.calcHist([item],[0],msk,[256],[0,255])
        cv2.normalize(hist_item,hist_item,0,255,cv2.NORM_MINMAX)
        hist=np.int32(np.around(hist_item))
        #print str(hist)
        pts = np.column_stack((bins,hist))
        cv2.polylines(h,[pts],False,col)
    
    h=np.flipud(h)
    return h

#Cuanto mas cercano a 0 mas parecido tendran
def compare_hist(h1,h2):
    r = cv2.compareHist(h1, h2, cv2.cv.CV_COMP_CHISQR)    
    #TODO    
    return r

