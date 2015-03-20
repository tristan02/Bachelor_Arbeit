import cv2
import numpy as np

def nothing(x):
    pass    

#Creamos una imagen negra y una imagen
img = np.zeros((512,512,3), np.uint8)
cv2.namedWindow('Trackbar')

#Creamos los trackbar para el cambio de color
cv2.createTrackbar('R', 'Trackbar', 0, 255, nothing)
cv2.createTrackbar('G', 'Trackbar', 0, 255, nothing)
cv2.createTrackbar('B', 'Trackbar', 0, 255, nothing)

#creamos el switch para activar el interruptor
switch = '0 : OFF \n1 : ON'
cv2.createTrackbar(switch, 'Trackbar', 0, 1, nothing)

while(1):
    cv2.imshow('Trackbar', img)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break
    
    r = cv2.getTrackbarPos('R','Trackbar')
    g = cv2.getTrackbarPos('G','Trackbar')
    b = cv2.getTrackbarPos('B','Trackbar')
    s = cv2.getTrackbarPos(switch,'Trackbar')
    
    if s == 0:
        img[:] = 0
    else:
        img[:] = [b,g,r]

cv2.destroyAllWindows()