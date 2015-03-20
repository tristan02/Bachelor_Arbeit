import cv2
import numpy as np

i1 = 70.0
i2 = 30.0 
z = 0 

def nothing(x):
    pass  

img1 = cv2.imread('Colag.jpg')
img2 = cv2.imread('Colage.jpg')
cv2.namedWindow('valores')
cv2.createTrackbar('Img1', 'valores', 70, 100, nothing)
cv2.createTrackbar('Img2', 'valores', 30, 100, nothing)
cv2.createTrackbar('Brillo', 'valores', 30, 250, nothing)

while(1):
    x = i1/100
    y = i2/100
    dst = cv2.addWeighted(img1,x,img2,y,z)
    cv2.imshow('dst',dst)
    
    i1 = float(cv2.getTrackbarPos('Img1', 'valores'))
    i2 = float(cv2.getTrackbarPos('Img2', 'valores'))
    z = cv2.getTrackbarPos('Brillo','valores')

    k = cv2.waitKey(0)
    if k==27:
        break
#cv2.imwrite('mezcla.jpg', dst)    
cv2.destroyAllWindows()