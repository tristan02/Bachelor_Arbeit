import cv2
import numpy as np

img = cv2.imread('Acoplada.jpg')

#Medimos los ciclos desde e1 hasta e2 y lo dividimos entre la frecuencia para sacar el tiempo real
c1 = cv2.getTickCount()

for i in xrange(5,49,2):
    img = cv2.medianBlur(img,i)
c2 = cv2.getTickCount()
t = (c2 - c1)/cv2.getTickFrequency()
print t
cv2.imshow('Ventana', img)
cv2.waitKey(0)
cv2.destroyAllWindows()