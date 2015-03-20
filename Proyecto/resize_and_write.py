#! /usr/bin/python
# opencv 2.3.1

import cv2
import sys
import numpy as np
import datetime
#import floodfillgray

def find_rectangle(contours):
    final_rect = [0,0,0,0]
    rectangles = []
    for contour in contours:
        minrect = cv2.boundingRect(contour)        
        area = minrect[2]*minrect[3]  
        if area < 100800-100 and minrect[2]>minrect[3]*2 and area>10000 and minrect[2]/minrect[3]>2 and minrect[2]/minrect[3]< 4 :
            rectangles = rectangles + [minrect]
            final_rect = minrect
    if (len(rectangles)>1):
        dist = 5
        for i in range(len(rectangles)):
            if (dist > abs(rectangles[i][2]/rectangles[i][3]-3.5)):
                dist = abs(rectangles[i][2]/rectangles[i][3]-3.5)
                final_rect = rectangles[i] 
    return final_rect


def resize(img,final_rect,average):
        #102 y 349 es el valor medio de w y h, respectivamente, de todas las imagenes en las que detecta qp
        w =  img.shape[0]*(average[0])/final_rect[3]
        h = img.shape[1]*(average[1])/final_rect[2]
        imgResize = cv2.resize(img,(h,w), None, 1, 1, cv2.INTER_CUBIC)
        
        return imgResize

def findRect(img):
        #search the area where it's more probably to find the scale image
        template = cv2.imread('tmp.jpg')
        imgfound = cv2.matchTemplate(img, template, cv2.TM_SQDIFF_NORMED)
        minVal,maxVal,minLoc,maxLoc = cv2.minMaxLoc(imgfound)

        #reduces the image to the area most probably
        reduced_img = np.zeros(img.shape,np.uint8)+255
        reduced_img[minLoc[1]-40:img.shape[0],minLoc[0]-40:img.shape[1]] = img[minLoc[1]-40:img.shape[0],minLoc[0]-40:img.shape[1]]
        imgthres = flooded(reduced_img,27,255,51)
        cv2.imshow("1", reduced_img)
        cv2.imshow("2", imgthres)
        cv2.waitKey(0)

        #computes the contours
        imgcanny = imgthres.copy()
        imgcanny = cv2.Canny(cv2.cvtColor(imgcanny,cv2.cv.CV_RGB2GRAY), 147,600)
        contours, hierarchy = cv2.findContours(imgcanny.copy(),cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        contours = [cv2.approxPolyDP(contour, 1, True) for contour in contours];

        #computes the rectangle most similar with the qp card
        final_rect = find_rectangle(contours)
        return final_rect

       
def resizeAndWrite(img,name,fileName,write, average = [102,349]):
    final_rect = findRect(img)      
    cv2.rectangle(img,(final_rect[0],final_rect[1]),(final_rect[2]+final_rect[0],final_rect[3]+final_rect[1]),(0,0,255))
    #resize and write the image
    if final_rect != [0,0,0,0]:
        imgResize = resize(img,final_rect,average)
        cv2.imshow('image resize',imgResize)
        if write:
            print str(fileName)+'/resized'+name
            cv2.imwrite(str(fileName)+'/resized'+name,imgResize)
        return imgResize
    else:
        print 'not found color check'
        cv2.imshow('special images', img)
        return img
    
    
def flooded(img, epsilon, hi, lo):
    img2 = np.array(img,float)
    img2 = img2/3
    img3 = img2[:,:,0]+img2[:,:,1]+img2[:,:,2]
    m1 = np.ma.masked_less(img3,hi)
    m2 = np.ma.masked_greater(img3,lo)
    m1 = 1-m1.mask
    m2 = 1-m2.mask
    m3 = np.ma.mask_or(m1,m2)
    m3 = 1-m3
    m3 = 1-m3
    w, h = img.shape[:2]
    aa = np.zeros((w,h),float)

    b = cv2.split(img)[0]
    g = cv2.split(img)[1]
    r = cv2.split(img)[2]

    b = np.array(b,np.int16)
    g = np.array(g,np.int16)
    r = np.array(r,np.int16)

    cmax = (b+g+abs(b-g))/2
    ma = (cmax+r+abs(cmax-r))/2
    cmin = (b+g-abs(b-g))/2
    mi = (cmin+r-abs(cmin-r))/2
    a = ma - mi

    m = np.ma.masked_less(a,epsilon)
    m = 1 - m.mask
    
    M = np.ma.mask_or(m,m3)
    M = 1-M
    mas = np.zeros((M.shape[0],M.shape[1],3),np.uint8)
    mas[:,:,0]=M
    mas[:,:,1]=M
    mas[:,:,2]=M
    i = np.ma.array(img,mask=mas)
    i.set_fill_value(255)
    img = i.filled()
    
    return img

img = cv2.imread('img.jpg')
rect = findRect(img)
print rect
cv2.waitKey(0)
cv2.destroyAllWindows()

#if __name__ == '__main__':
'''print  resizeAndWrite.py <average=[102,349]> <True/False> <image> <image>....
  average -------> calculates width and high of color-check and resize with this data
  True/False-----> if True then write image after resize else not write


    if sys.argv[1]=='average':
        name_images = sys.argv[3:]
        write = sys.argv[2]
        wAver, hAver, num = 0,0,0
        for name in name_images:
            num = num+1
            img = cv2.imread(name)
            rect = findRect(img)
            wAver = wAver+rect[3]
            hAver = hAver+rect[2]
        average = [wAver/num, hAver/num]
        print average
    else:
        name_images = sys.argv[2:]
        write = sys.argv[1]
        average = [102, 349]

    for name in name_images:
        img = cv2.imread(name)
        cv2.imshow('image',img)
        resizeAndWrite(img,name,'butterflies_resized',write,average)
        k = cv2.waitKey(0)'''

