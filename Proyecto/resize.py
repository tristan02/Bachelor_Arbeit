''' 
Created on 3/12/2014

@author: Tristan
'''
import cv2
import sys
import numpy as np

#Le llega una imagen y busca el 0 y el 3 de la regla que escala las imagenes y devuelve la distancia en pixeles que los separan
def find_0_3(img_o):
    img = img_o
    h,w = img.shape[:2]
    mask = np.zeros((h,w,3), np.uint8)
    v0 = [h,w]
    v3 = [0,0]
    
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    gray = np.float32(gray)
    #Detecta "perfectamente" el zero y el tres
    dst = cv2.cornerHarris(gray,15,21,0.22)   
    
    #result is dilated for marking the corners
    dst = cv2.dilate(dst,None)   

    # Threshold for an optimal value, it may vary depending on the image.
    mask[dst>0.005*dst.max()]=[0,0,255]        
    
    #Como sabemos que la metrica esta en la mitad de abajo de todas la imagenes acotamos para reducir el coste en tiempo
    for x in range(w):
        for y in range(h/2,h):
            px = mask[y,x]
            #Si el pixel es rojo mejoramos el valor para seguir bajando                       
            if px[0] == 0 and px[1] == 0 and px[2] == 255:
                if v3[0] < y or v3[1] < y:                    
                    #print 'Valor mejorado. Antes:(' + str(v0[0]) +',' + str(v0[1]) + ') ahora:(' + str(x) +',' + str(y) + ')'
                    v3 = [x,y]
                if v0[0] > x or v0[1] < y:
                    v0 = [x,y]
    #print str(v0[0]) + '---->' + str(v0[1])
    cv2.circle(img,(v3[0],v3[1]), 10, (0,0,255), -1)
    cv2.circle(img,(v0[0],v0[1]), 10, (0,0,255), -1)
    sol = v3[0]-v0[0]
    
    img = img_o    
    return sol,img

    