import cv2
import numpy as np

def nothing(x):
    pass    

def pinta(event,x,y,flags,param):
    global r,g,b,t,f
    if event == cv2.EVENT_FLAG_LBUTTON:
        if f == 0:
            cv2.circle(img,(x,y),t,(r,g,b),5)
        else:
            cv2.rectangle(img,(x,y),(x+t,y+t),(r,g,b),5)
    elif event == cv2.EVENT_FLAG_RBUTTON:
        cv2.circle(img,(250,250),1000,(0,0,0),-1)

#Creamos una imagen negra y una imagen
img = np.zeros((512,512,3), np.uint8)
cv2.namedWindow('Paint')
cv2.setMouseCallback('Paint', pinta)

#Creamos los trackbar para el cambio de color
cv2.createTrackbar('R', 'Paint', 0, 255, nothing)
cv2.createTrackbar('G', 'Paint', 0, 255, nothing)
cv2.createTrackbar('B', 'Paint', 0, 255, nothing)

#Creamos el trackbar para el tamanyo de la brocha
cv2.createTrackbar('Grosor', 'Paint', 0, 100, nothing)
# Trackbar para circulo o cuadrado
fig = '0 : Circulo \n1 : Rectangulo'
cv2.createTrackbar(fig, 'Paint', 0, 1, nothing)


while(1):
    cv2.imshow('Paint', img)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        cv2.imwrite('Paint.jpg', img)
        break
    
    r = cv2.getTrackbarPos('R','Paint')
    g = cv2.getTrackbarPos('G','Paint')
    b = cv2.getTrackbarPos('B','Paint')
    t = cv2.getTrackbarPos('Grosor','Paint')
    f = cv2.getTrackbarPos(fig,'Paint')
    

cv2.destroyAllWindows()