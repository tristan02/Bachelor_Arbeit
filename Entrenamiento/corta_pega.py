'''Eliges el tamanyo de la seccion que quieres cortar y la pegas donde quieres.
 Hay que tocar una tecla para que se recarge la imagen'''

import cv2
import numpy as np

mariposa = []
t = 80

def nothing(x):
    pass  

def corta_pega(event,x,y,flags,param):
    global t,mariposa
    if event == cv2.EVENT_LBUTTONDOWN:
        mariposa = img[y:y+t, x:x+t]
    elif event == cv2.EVENT_LBUTTONUP:
        img[y:y+t, x:x+t] = mariposa

img = cv2.imread('contornocont.jpg')
cv2.namedWindow('Ventana')
cv2.setMouseCallback('Ventana', corta_pega)
cv2.createTrackbar('Tamanyo', 'Ventana', 80, 150, nothing)

while(1):
    t = cv2.getTrackbarPos('Tamanyo', 'Ventana')
    cv2.imshow('Ventana', img)
    k = cv2.waitKey(0)
    if k == 27:
        break

#cv2.imwrite('Colag.jpg', img)    
cv2.destroyAllWindows()
