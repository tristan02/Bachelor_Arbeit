import cv2
import numpy as np


def colorea_pixel(event,x,y,flags,param):
    if event == cv2.EVENT_FLAG_LBUTTON:
        print (img[x,y])
        img[x,y] = [255,255,255]
        print (img[x,y])
        
        
#Cargamos una imagen en escala de grises
img = cv2.imread('rgb.jpg',1)
cv2.namedWindow('Ventana')
cv2.setMouseCallback('Ventana', colorea_pixel)

while(1):
    cv2.imshow('Ventana', img)
    k = cv2.waitKey(0)
    if k == 27:
        break
    
    
cv2.destroyAllWindows()