'''
Created on 29/1/2015

@author: Psilocibino
'''
import cv2
import numpy as np

def get_contour(contours,w,h):

    max1 = 0
    i = 0
    centroide = False
    for c in contours:
        if cv2.arcLength(c, True) > max1:
            max1 = cv2.arcLength(c, True)
            cnt = contours[i]
        i = i + 1 
           
    i = 0
    max2 = 0
    for c in contours:
        #Sacamos el centroide para ver si es contorno de mariposa
        M = cv2.moments(c) 
        if M['m00'] != 0:
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            if cy < 280 and cy > 180 and cx < 400 and cx > 300:
                centro = True
        if cv2.arcLength(c, True) > max2 and cv2.arcLength(c, True) != max1 and centro:
            max2 = cv2.arcLength(c, True)
            cnt = contours[i]
            centroide = (cx,cy)
            area = cv2.contourArea(cnt)
        i = i + 1
        centro = False     
    #El contorno en las mariposas pequenyas no es el 2 mas grande por lo que tenemos que comprobar tambien la posicion del centroide.   
    '''for c in contours:   '''      
    
    M = cv2.moments(cnt)   
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    
    '''cv2.circle(gray,(cx,cy), 10, (0,255,0), -1)
    
    txt = str(cx) + ',' + str(cy)
    cv2.putText(gray, txt , (30,30), cv2.FONT_HERSHEY_PLAIN, 2, (0,255,0))'''
    
    return cnt,centroide,area

def get_mask(img):
    t1 = 230
    t2 = 255
    t3 = 0
    m1 = 20
    m2 = 255
    
    #Carga de imagenes
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray,550,300)
    h,w = img.shape[:2]
    ret,thresh = cv2.threshold(gray,t1,t2,t3)
    '''cv2.imshow("thresh",thresh)
    cv2.waitKey()'''
    
    #Seleccionamos el contorno que nos interesa El mas grande es el recuadro de la foto. Asi que probablemente el 2 mas
    #grande sea el de la mariposa.
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cnt,centroide,area = get_contour(contours,w,h)
    
    cv2.drawContours(image=gray,contours=[cnt], contourIdx=0, color=(0,255,0),thickness=-1)         
  
    
    ret, mask = cv2.threshold(gray, m1, m2, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)
    #TODO aplicar filtro para quitar ruidos
    #blur = cv2.bilateralFilter(mask,10,150,150)
    return mask_inv,centroide,area

#cv2.imwrite('mezcla.jpg', dst)
'''
for i in range(100):
    path = 'ima/img (' + str(i+1) + ').jpg'
    #path = 'ima/img (14).jpg'
    img = cv2.imread(path)
    
    #edges = cv2.Canny(img,270,500)    
    #cv2.imwrite('canny.jpg', edges)
    
    #img = cv2.imread('canny.jpg')
    #img_g = cv2.cvtColor(img, cv2.CV_32FC1)
    
    #x,y,mn = match(img_g)
    
    img_z,centroide = get_mask(img)
    cv2.imshow('output',img_z)   
    cv2.waitKey()
    

cv2.destroyAllWindows()'''