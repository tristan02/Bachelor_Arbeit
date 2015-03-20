import cv2
import numpy as np

img = cv2.imread('Imagen6.jpg',0)

laplacian = cv2.Laplacian(img,cv2.CV_64F)
sobelx = cv2.Sobel(img,cv2.CV_64F,1,0,ksize=5)
sobely = cv2.Sobel(img,cv2.CV_64F,0,1,ksize=5)

cv2.imshow("1",img)
cv2.imshow("2",laplacian)
cv2.imshow("3",sobelx)
cv2.imshow("4",sobely)

cv2.waitKey(0)
cv2.destroyAllWindows()