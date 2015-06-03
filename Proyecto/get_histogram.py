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
    hist_item = []
    
    for item,col in zip([b,g,r],color):
        hist_item = cv2.calcHist([item],[0],msk,[256],[0,255])
        cv2.normalize(hist_item,hist_item,0,255,cv2.NORM_MINMAX)
        hist=np.int32(np.around(hist_item))
        pts = np.column_stack((bins,hist))
        cv2.polylines(h,[pts],False,col)
    
    h=np.flipud(h)
    return h, hist_item

#Cuanto mas cercano a 0 mas parecido tendran
def compare_hist(img1,msk1,img2,msk2): 
    
    b,g,r = cv2.split(img1)
           
    histB = cv2.calcHist([b],[0],msk1,[256],[0,255])
    cv2.normalize(histB,histB,0,1,cv2.NORM_MINMAX)
    histG = cv2.calcHist([g],[0],msk1,[256],[0,255])
    cv2.normalize(histG,histG,0,1,cv2.NORM_MINMAX)
    histR = cv2.calcHist([r],[0],msk1,[256],[0,255])
    cv2.normalize(histR,histR,0,1,cv2.NORM_MINMAX) 
    
    #Calculos de los histogramas de la segunda img  
    b,g,r = cv2.split(img2)
    
    histB1 = cv2.calcHist([b],[0],msk2,[256],[0,255])
    cv2.normalize(histB1,histB1,0,1,cv2.NORM_MINMAX)
    histG1 = cv2.calcHist([g],[0],msk2,[256],[0,255])
    cv2.normalize(histG1,histG1,0,1,cv2.NORM_MINMAX)
    histR1 = cv2.calcHist([r],[0],msk2,[256],[0,255])
    cv2.normalize(histR1,histR1,0,1,cv2.NORM_MINMAX)
  
    
    v1 = cv2.compareHist(histB, histB1, cv2.cv.CV_COMP_CHISQR)
    v2 = cv2.compareHist(histG, histG1, cv2.cv.CV_COMP_CHISQR)
    v3 = cv2.compareHist(histR, histR1, cv2.cv.CV_COMP_CHISQR) 
    
    return v1, v2, v3
    

'''path1 = 'ima/img (18).jpg'
img1 = cv2.imread(path1)

path2 = 'ima/img (5).jpg'
img2 = cv2.imread(path2)

path3 = 'mask (3)'
msk = cv2.imread(path3)

v1, v2, v3 = compare_hist(img1,msk, img2, msk)
print str(v1)
print str(v2)
print str(v3)'''

