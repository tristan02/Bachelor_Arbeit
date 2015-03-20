import cv2
import numpy as np

#Carga de imagenes
img1 = cv2.imread('asdf.jpg')
img2 = cv2.imread('img.jpg')
img2 = cv2.bitwise_not(img2)

#creamos un roi (region de interes) de la img1 con la forma de la segunda que es mas pequenya
filas,cols,canales = img2.shape
roi = img1[0:filas,0:cols ]

#mascara e inversa de la img2 (No entiendo porque hay que pasarlo a escala de grises)
img2gray = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
mask_inv = cv2.bitwise_not(mask)

#AND con el roi y la mask_inv
img1_bg = cv2.bitwise_and(roi,roi,mask = mask_inv)

#Juntamos el logo
dst = cv2.add(img1_bg,img2)
img1[0:filas, 0:cols ] = dst

cv2.imshow('vetnana1',img1)
cv2.imshow('vetnana2',roi)
cv2.imshow('vetnana3',mask)
cv2.imshow('vetnana4',mask_inv)
cv2.imshow('vetnana5',img1_bg)
cv2.imshow('vetnana7',dst)
cv2.waitKey(0)
cv2.imwrite('Acoplada.jpg', img1)
cv2.destroyAllWindows()